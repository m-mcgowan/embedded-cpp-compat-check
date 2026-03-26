"""Sync the SD-6 feature catalog from upstream."""
from pathlib import Path
import httpx

UPSTREAM_URL = (
    "https://raw.githubusercontent.com/"
    "cpplearner/feature-test-macro/master/data.yaml"
)

def sync_catalog(target: Path, url: str = UPSTREAM_URL) -> None:
    """Download data.yaml from upstream and write to target path."""
    response = httpx.get(url)
    response.raise_for_status()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(response.text)
