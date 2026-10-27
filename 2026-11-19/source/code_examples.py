"""Exact verified reference; reveal only after attempting the worksheet."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from shared.product_sources import DAY19_SOURCES
SOURCES = dict(DAY19_SOURCES)
