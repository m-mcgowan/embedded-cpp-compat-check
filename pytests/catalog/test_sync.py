from pathlib import Path
from unittest.mock import patch, MagicMock
from compat_check.catalog.sync import sync_catalog

def test_sync_catalog_downloads_to_target(tmp_path):
    target = tmp_path / "data.yaml"
    mock_response = MagicMock()
    mock_response.text = "language: []\nlibrary: []\n"
    mock_response.raise_for_status = MagicMock()
    with patch("compat_check.catalog.sync.httpx") as mock_httpx:
        mock_httpx.get.return_value = mock_response
        sync_catalog(target)
    assert target.exists()
    assert "language" in target.read_text()

def test_sync_catalog_uses_correct_url():
    with patch("compat_check.catalog.sync.httpx") as mock_httpx:
        mock_response = MagicMock()
        mock_response.text = "language: []\n"
        mock_response.raise_for_status = MagicMock()
        mock_httpx.get.return_value = mock_response
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".yaml") as f:
            sync_catalog(Path(f.name))
        call_url = mock_httpx.get.call_args[0][0]
        assert "cpplearner" in call_url
        assert "data.yaml" in call_url
