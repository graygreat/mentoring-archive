"""Exact verified reference; reveal only after attempting the worksheet."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from shared.order_sources import ORDER_SOURCES
SOURCES = dict(ORDER_SOURCES)
