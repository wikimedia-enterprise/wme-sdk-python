"""Test suite for Wikidata-specific endpoints in the WME API Client."""

from datetime import datetime
from unittest.mock import MagicMock, patch
import pytest

from modules.api.api_client import Client
from modules.api.snapshot import Snapshot
from modules.api.batch import Batch
from modules.api.article import Article

@pytest.fixture(name="api_client")
def api_client_fixture():
    """Fixture to set up a clean Client instance."""
    return Client(access_token="dummy_token")

def test_get_wikidata_snapshots(api_client):
    """Tests retrieving metadata for all Wikidata snapshots."""
    def mock_get_entity(_req, path, val):
        """Mocks the internal _get_entity method for Wikidata snapshots."""
        assert path == "snapshots/wikidata"
        val.append({"identifier": "items", "version": "test_version"})

    with patch.object(api_client, '_get_entity', side_effect=mock_get_entity):
        snapshots = api_client.get_wikidata_snapshots()
        assert len(snapshots) == 1
        assert isinstance(snapshots[0], Snapshot)
        assert snapshots[0].identifier == "items"

def test_get_wikidata_snapshot(api_client):
    """Tests retrieving metadata for a specific Wikidata snapshot."""
    def mock_get_entity(_req, path, val):
        """Mocks the internal _get_entity method for a specific snapshot."""
        assert path == "snapshots/wikidata/properties"
        val.update({"identifier": "properties", "version": "test_version"})

    with patch.object(api_client, '_get_entity', side_effect=mock_get_entity):
        snapshot = api_client.get_wikidata_snapshot("properties")
        assert isinstance(snapshot, Snapshot)
        assert snapshot.identifier == "properties"

def test_head_wikidata_snapshot(api_client):
    """Tests retrieving response headers for a Wikidata snapshot download."""
    with patch.object(api_client, '_head_entity', return_value={"Content-Length": 1024}) as mock_head:
        headers = api_client.head_wikidata_snapshot("items")
        mock_head.assert_called_once_with("snapshots/wikidata/items/download")
        assert headers["Content-Length"] == 1024

def test_read_wikidata_snapshot(api_client):
    """Tests streaming and reading a Wikidata snapshot."""
    def mock_read_archive(path, parsing_callback):
        """Mocks the archive extraction and simulates a parsed NDJSON line."""
        assert path == "snapshots/wikidata/properties/download"
        parsing_callback({"name": "P10410", "identifier": 106063463})

    with patch.object(api_client, '_read_archive_entity', side_effect=mock_read_archive):
        mock_cbk = MagicMock()
        api_client.read_wikidata_snapshot("properties", mock_cbk)

        mock_cbk.assert_called_once()
        args, _ = mock_cbk.call_args
        assert isinstance(args[0], Article)
        assert args[0].identifier == 106063463

def test_download_wikidata_snapshot(api_client):
    """Tests downloading a Wikidata snapshot."""
    mock_writer = MagicMock()
    with patch.object(api_client, '_download_entity') as mock_download:
        api_client.download_wikidata_snapshot("properties", mock_writer)
        mock_download.assert_called_once_with("snapshots/wikidata/properties/download", mock_writer)

def test_get_wikidata_chunks(api_client):
    """Tests retrieving metadata for all chunks of a Wikidata snapshot."""
    def mock_get_entity(_req, path, val):
        """Mocks the internal _get_entity method for chunks."""
        assert path == "snapshots/wikidata/items/chunks"
        val.append({"identifier": "wikidata_items_chunk_0"})

    with patch.object(api_client, '_get_entity', side_effect=mock_get_entity):
        chunks = api_client.get_wikidata_chunks("items")
        assert len(chunks) == 1
        assert chunks[0].identifier == "wikidata_items_chunk_0"

def test_head_wikidata_chunk(api_client):
    """Tests retrieving response headers for a Wikidata chunk download."""
    with patch.object(api_client, '_head_entity', return_value={"Content-Length": 2048}) as mock_head:
        headers = api_client.head_wikidata_chunk("items", "0")
        mock_head.assert_called_once_with("snapshots/wikidata/items/chunks/0/download")
        assert headers["Content-Length"] == 2048

def test_read_wikidata_chunk(api_client):
    """Tests streaming and reading a specific Wikidata chunk."""
    def mock_read_archive(path, parsing_callback):
        """Mocks the archive extraction and simulates a parsed NDJSON line."""
        assert path == "snapshots/wikidata/items/chunks/0/download"
        parsing_callback({"name": "Q42", "identifier": 42})

    with patch.object(api_client, '_read_archive_entity', side_effect=mock_read_archive):
        mock_cbk = MagicMock()
        api_client.read_wikidata_chunk("items", "0", mock_cbk)

        mock_cbk.assert_called_once()
        args, _ = mock_cbk.call_args
        assert isinstance(args[0], Article)
        assert args[0].identifier == 42

def test_download_wikidata_chunk(api_client):
    """Tests downloading a specific Wikidata chunk."""
    mock_writer = MagicMock()
    with patch.object(api_client, '_download_entity') as mock_download:
        api_client.download_wikidata_chunk("items", "0", mock_writer)
        mock_download.assert_called_once_with("snapshots/wikidata/items/chunks/0/download", mock_writer)

def test_get_wikidata_batches(api_client):
    """Tests retrieving metadata for Wikidata batches at a specific timestamp."""
    test_time = datetime(2026, 9, 30, 14, 0, 0)

    def mock_get_entity(_req, path, val):
        """Mocks the internal _get_entity method for batches."""
        assert path == "batches/2026-09-30/14/wikidata"
        val.append({"identifier": "items", "version": "batch_version"})

    with patch.object(api_client, '_get_entity', side_effect=mock_get_entity):
        batches = api_client.get_wikidata_batches(test_time)
        assert len(batches) == 1
        assert isinstance(batches[0], Batch)
        assert batches[0].identifier == "items"

def test_get_wikidata_batch(api_client):
    """Tests retrieving metadata for a specific Wikidata batch."""
    test_time = datetime(2026, 9, 30, 14, 0, 0)

    def mock_get_entity(_req, path, val):
        """Mocks the internal _get_entity method for a specific batch."""
        assert path == "batches/2026-09-30/14/wikidata/properties"
        val.update({"identifier": "properties"})

    with patch.object(api_client, '_get_entity', side_effect=mock_get_entity):
        batch = api_client.get_wikidata_batch(test_time, "properties")
        assert isinstance(batch, Batch)
        assert batch.identifier == "properties"

def test_head_wikidata_batch(api_client):
    """Tests retrieving response headers for a Wikidata batch download."""
    test_time = datetime(2026, 9, 30, 14, 0, 0)
    with patch.object(api_client, '_head_entity', return_value={"Content-Length": 4096}) as mock_head:
        headers = api_client.head_wikidata_batch(test_time, "items")
        mock_head.assert_called_once_with("batches/2026-09-30/14/wikidata/items/download")
        assert headers["Content-Length"] == 4096

def test_read_wikidata_batch(api_client):
    """Tests streaming and reading a Wikidata batch."""
    test_time = datetime(2026, 9, 30, 14, 0, 0)
    def mock_read_archive(path, parsing_callback):
        """Mocks the archive extraction and simulates a parsed NDJSON line."""
        assert path == "batches/2026-09-30/14/wikidata/items/download"
        parsing_callback({"name": "Q123", "identifier": 123})

    with patch.object(api_client, '_read_archive_entity', side_effect=mock_read_archive):
        mock_cbk = MagicMock()
        api_client.read_wikidata_batch(test_time, "items", mock_cbk)

        mock_cbk.assert_called_once()
        args, _ = mock_cbk.call_args
        assert isinstance(args[0], Article)
        assert args[0].identifier == 123

def test_download_wikidata_batch(api_client):
    """Tests downloading a Wikidata batch."""
    test_time = datetime(2026, 9, 30, 14, 0, 0)
    mock_writer = MagicMock()

    with patch.object(api_client, '_download_entity') as mock_download:
        api_client.download_wikidata_batch(test_time, "items", mock_writer)
        mock_download.assert_called_once_with("batches/2026-09-30/14/wikidata/items/download", mock_writer)
