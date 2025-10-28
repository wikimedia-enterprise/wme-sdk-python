"""Integration tests for the `api_client` module.

This test suite performs end-to-end tests against the live
Wikimedia Enterprise API. It is designed to validate the client's
behavior, including authentication,
API schema validation, and binary download workflows.

These tests are not mocked and require a live internet connection
and valid credentials. To run this suite, set the following
environment variables on .env:
    - WME_USERNAME
    - WME_PASSWORD
"""

# pylint: disable=W0719, W0718

import unittest
import os
import io
from datetime import datetime
from modules.api.api_client import Client, Request, Filter
from modules.auth.auth_client import AuthClient
from modules.auth.helper import Helper

WME_USERNAME = os.environ.get("WME_USERNAME")
WME_PASSWORD = os.environ.get("WME_PASSWORD")

@unittest.skipUnless(
    WME_USERNAME and WME_USERNAME,
    "Set the WME_USERNAME and WME_PASSWORD env variables to run integration tests"
)
class TestClientIntegration(unittest.TestCase):
    """Performs end-to-end integration tests for the Client.

    This test class verifies the Client's functionality by making
    real network calls to the Wikimedia Enterprise API. It uses the
    `setUpClass` method to perform a single, real authentication
    handshake, obtaining a live access token that is used for all
    tests within the class.

    Tests cover:
    - Basic connectivity and authentication ("smoke test").
    - Fetching a single entity by its ID.
    - Filtering a list of entities using nested fields.
    - The complete binary download workflow (HEAD and GET).
    """
    client: Client
    helper: Helper

    @classmethod
    def setUpClass(cls):
        """
        Set up a real client instance by performing the
        full authentication flow once for the entire test class.
        """
        print("\nSetting up integration test client...")
        print("Attempting authentication...")

        try:
            auth_client = AuthClient()
            cls.helper = Helper(auth_client)
            token = cls.helper.get_access_token()

            cls.client = Client()
            cls.client.set_access_token(token)

            print("Authentication successful. Client is ready.")
        except Exception as e:
            raise Exception(f"Failed to authenticate during setUpClass: {e}") from e

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests are done"""
        print("\nTearing down integration test client...")
        if hasattr(cls, 'client'):
            cls.client.http_client.close()

        if hasattr(cls, 'helper') and hasattr(cls.helper, 'stop'):
            print("Stopping auth helper thread...")
            cls.helper.stop()

    def test_get_projects_smoke_test(self):
        """
        A simple "smoke test" to ensure we can authenticate, connect,
        and receive a list of projects.
        """
        print("Running test_get_projects_smoke_test...")

        req = Request()

        try:
            projects = self.client.get_projects(req)
        except Exception as e:
            self.fail(f"client.get_projects() raised an unexpected exception: {e}")

        self.assertIsInstance(projects, list)
        self.assertGreater(len(projects), 0)

        print(f"... Received {len(projects)} projects. Checking first one.")
        first_project = projects[0]
        self.assertIn("code", first_project)
        self.assertIn("name", first_project)
        self.assertIsInstance(first_project["code"], str)

    def test_get_snapshot_by_id(self):
        """
        Tests fetching a single, known entity by its ID.
        This validates that path parameters are working correctly.
        """
        print("Running test_get_snapshot_by_id....")

        snapshot_id = "enwiki_namespace_0"
        req = Request()

        try:
            snapshot = self.client.get_snapshot(idr=snapshot_id, req=req)
        except Exception as e:
            self.fail(f"client.get_snapshot() raised an unexpected exception: {e}")

        self.assertIsInstance(snapshot, dict)

        self.assertIn("identifier", snapshot)
        self.assertEqual(snapshot["identifier"], snapshot_id)

        self.assertIn("is_part_of", snapshot)
        self.assertIsInstance(snapshot["is_part_of"], dict)
        self.assertEqual(snapshot["is_part_of"]["identifier"], "enwiki")

        self.assertIn("namespace", snapshot)
        self.assertEqual(snapshot["namespace"]["identifier"], 0)

        self.assertIn("size", snapshot)
        self.assertGreater(snapshot["size"]["value"], 0)

        print(f"  ... Successfully fetched snapshot {snapshot['identifier']}.")

    def test_get_snapshots_with_filter(self):
        """Tests fetching snapshots, with a nested filter."""
        print("Running test_get_snapshots_with_filter...")

        my_filter = Filter(field="is_part_of.identifier", value="enwiki")

        req = Request(filters=[my_filter])

        try:
            snapshots = self.client.get_snapshots(req)
        except Exception as e:
            self.fail(f"client.get_snapshots() raised an unexpected exception: {e}")

        self.assertIsInstance(snapshots, list)

        self.assertGreater(len(snapshots), 0)

        print(f"  ... Received {len(snapshots)} snapshots. Verifying filter...")
        for snapshot in snapshots:
            self.assertIn("is_part_of", snapshot)
            self.assertEqual(snapshot["is_part_of"]["identifier"], "enwiki")

        print("  ... Filter verified successfully.")

    def test_head_and_download_batch(self):
        """
        Tests the full binary download workflow on a (much smaller)
        hourly batch file.
        """
        print("Running test_head_and_download_batch...")

        # This date gets a recent batch.
        # Should you see a 404 due to age,
        # you can update this date.
        batch_time = datetime(2025, 10, 26, 12) # YYYY, M, D, H
        req = Request(limit=1)

        print(f"  ... Finding a batch from {batch_time}...")
        try:
            batches = self.client.get_batches(timestamp=batch_time, req=req)
        except Exception as e:
            self.fail(f"client.get_batches() failed, cannot proceed: {e}")

        self.assertGreater(len(batches), 0, f"No batches found for {batch_time}, cannot run download test.")

        batch_to_test = batches[0]
        batch_id = batch_to_test['identifier']
        print(f"  ... Found batch to test: {batch_id}")

        download_buffer = io.BytesIO()

        print(f"  ... Sending HEAD request for batch {batch_id}...")
        try:
            headers = self.client.head_batch(timestamp=batch_time, idr=batch_id)
        except Exception as e:
            self.fail(f"client.head_batch() raised an unexpected exception: {e}")

        self.assertIsInstance(headers, dict)
        self.assertIn("Content-Length", headers)

        size_from_head = headers['Content-Length']
        self.assertIsInstance(size_from_head, int)
        self.assertGreater(size_from_head, 0)
        print(f"  ... HEAD success. Expected size: {size_from_head} bytes.")

        print("  ... Downloading file...")
        try:
            self.client.download_batch(timestamp=batch_time, idr=batch_id, writer=download_buffer)
        except Exception as e:
            self.fail(f"client.download_batch() raised an unexpected exception: {e}")

        size_from_download = download_buffer.getbuffer().nbytes
        print(f"  ... Download success. Received size: {size_from_download} bytes.")

        self.assertEqual(size_from_head, size_from_download)
        print("  ... Success! Head size matches downloaded size.")
