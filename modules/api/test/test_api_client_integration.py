# pylint: disable=W0719, W0718, R0904

"""Integration tests for the `api_client` module.
"""

import unittest
import os
import io
from datetime import datetime, timedelta, timezone
from modules.api.api_client import Client, Request
from modules.auth.auth_client import AuthClient
from modules.auth.helper import Helper
from modules.api.snapshot import Snapshot
from modules.api.project import Project
from modules.api.namespace import Namespace

WME_USERNAME = os.environ.get("WME_USERNAME")
WME_PASSWORD = os.environ.get("WME_PASSWORD")

@unittest.skipUnless(
    WME_USERNAME and WME_PASSWORD,
    "Set the WME_USERNAME and WME_PASSWORD env variables to run integration tests"
)
class TestClientIntegration(unittest.TestCase):
    """Performs end-to-end integration tests for the Client.
    """
    client: Client
    auth_client: AuthClient
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
            cls.auth_client = AuthClient()
            cls.helper = Helper(cls.auth_client)
            token = cls.helper.get_access_token()

            cls.client = Client()
            cls.client.set_access_token(token)

            print("Authentication successful. Client is ready.")
        except Exception as e:
            if hasattr(cls, 'auth_client'):
                cls.auth_client.close()
            raise Exception(f"Failed to authenticate during setUpClass: {e}") from e

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests are done."""
        print("\nTearing down integration test client...")
        try:
            if hasattr(cls, 'client'):
                cls.client.http_client.close()
                print(" - API client closed.")
        except Exception as e:
            print(f" - Warning: Failed to close api_client's http_client: {e}")

        try:
            if hasattr(cls, 'helper') and hasattr(cls.helper, 'stop'):
                print(" - Stopping auth helper thread...")
                cls.helper.stop()
        except Exception as e:
            print(f"   - Warning: Failed to stop auth helper (e.g., token revoke failed): {e}")

        try:
            if hasattr(cls, 'auth_client'):
                cls.auth_client.close()
                print(" - Auth client closed.")
        except Exception as e:
            print(f"   - Warning: Failed to close auth_client's http_client: {e}")

    def test_get_projects_smoke_test(self):
        """
        A simple "smoke test" to ensure we can authenticate, connect,
        and receive a list of projects.
        """
        print("Running test_get_projects_smoke_test...")

        req = Request(fields=["code", "name"])

        try:
            projects = self.client.get_projects(req)
        except Exception as e:
            self.fail(f"client.get_projects() raised an unexpected exception: {e}")

        self.assertIsInstance(projects, list)
        self.assertGreater(len(projects), 0)

        print(f"... Received {len(projects)} projects. Checking first one.")
        first_project = projects[0]
        self.assertTrue(hasattr(first_project, 'code'))
        self.assertTrue(hasattr(first_project, 'name'))
        self.assertIsInstance(first_project.code, str)

    def test_get_snapshot_by_id(self):
        """
        Tests fetching a single, known entity by its ID.
        This validates that path parameters are working correctly.
        """
        print("Running test_get_snapshot_by_id....")

        snapshot_id = "enwiki_namespace_0"

        req = Request(fields=["identifier", "is_part_of", "namespace", "size"])

        try:
            snapshot = self.client.get_snapshot(idr=snapshot_id, req=req)
        except Exception as e:
            self.fail(f"client.get_snapshot() raised an unexpected exception: {e}")

        self.assertIsInstance(snapshot, Snapshot)

        self.assertTrue(hasattr(snapshot, 'identifier'))
        self.assertEqual(snapshot.identifier, snapshot_id)

        self.assertTrue(hasattr(snapshot, 'is_part_of'))
        if snapshot.is_part_of is None:
            self.fail(f"snapshot.is_part_of was None for {snapshot_id}, expected a Project object.")

        self.assertIsInstance(snapshot.is_part_of, Project)
        self.assertEqual(snapshot.is_part_of.identifier, "enwiki")

        self.assertTrue(hasattr(snapshot, 'namespace'))
        if snapshot.namespace is None:
            self.fail(f"snapshot.namespace was None for {snapshot_id}, expected a Namespace object.")

        self.assertIsInstance(snapshot.namespace, Namespace)
        self.assertEqual(snapshot.namespace.identifier, 0)

        # --- Test 'size' ---
        self.assertTrue(hasattr(snapshot, 'size'))
        if snapshot.size is None:
            self.fail(f"snapshot.size was None for {snapshot_id}, expected a Size object.")

        self.assertTrue(hasattr(snapshot.size, 'value'))
        if snapshot.size.value is None:
            self.fail(f"snapshot.size.value was None for {snapshot_id}, expected a float.")

        self.assertIsInstance(snapshot.size.value, float)
        self.assertGreater(snapshot.size.value, 0)

        print(f"   ... Successfully fetched and validated snapshot {snapshot.identifier}.")

    def test_get_snapshots_with_filter(self):
        """Tests fetching snapshots, with a nested filter."""
        print("Running test_get_snapshots_with_filter...")

        filters = {"is_part_of.identifier": "enwiki"}

        req = Request(filters=filters, fields=["is_part_of"])

        try:
            snapshots = self.client.get_snapshots(req)
        except Exception as e:
            self.fail(f"client.get_snapshots() raised an unexpected exception: {e}")

        self.assertIsInstance(snapshots, list)

        self.assertGreater(len(snapshots), 0)

        print(f"   ... Received {len(snapshots)} snapshots.")

        print("   ... Filtered request completed successfully.")

    def test_head_and_download_batch(self):
        """
        Tests the full binary download workflow on a (much smaller)
        hourly batch file.
        """
        print("Running test_head_and_download_batch...")

        batch_time = datetime.now(timezone.utc) - timedelta(hours=3)

        req = Request(limit=1, fields=["identifier"])

        print(f"   ... Finding a batch from {batch_time.isoformat()}...")
        try:
            batches = self.client.get_batches(timestamp=batch_time, req=req)
        except Exception as e:
            self.fail(f"client.get_batches() failed, cannot proceed: {e}")

        self.assertGreater(len(batches), 0, f"No batches found for {batch_time}, cannot run download test.")

        batch_to_test = batches[0]
        batch_id = batch_to_test.identifier

        if not batch_id:
            self.fail("Found a batch, but its identifier was None.")
            return

        print(f"   ... Found batch to test: {batch_id}")

        download_buffer = io.BytesIO()

        print(f"   ... Sending HEAD request for batch {batch_id}...")
        try:
            headers = self.client.head_batch(timestamp=batch_time, idr=batch_id)
        except Exception as e:
            self.fail(f"client.head_batch() raised an unexpected exception: {e}")

        self.assertIsInstance(headers, dict)
        self.assertIn("Content-Length", headers)

        size_from_head = headers['Content-Length']
        self.assertIsInstance(size_from_head, int)
        self.assertGreater(size_from_head, 0)
        print(f"   ... HEAD success. Expected size: {size_from_head} bytes.")

        print("   ... Downloading file...")
        try:
            self.client.download_batch(timestamp=batch_time, idr=batch_id, writer=download_buffer)
        except Exception as e:
            self.fail(f"client.download_batch() raised an unexpected exception: {e}")

        size_from_download = download_buffer.getbuffer().nbytes
        print(f"   ... Download success. Received size: {size_from_download} bytes.")

        self.assertEqual(size_from_head, size_from_download)
        print("   ... Success! Head size matches downloaded size.")
