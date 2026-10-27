"""Date-specific independent course examples; shared canonical source is read-only."""
from pathlib import Path
import runpy
_data = runpy.run_path(str(Path(__file__).resolve().parents[2] / 'shared/product_sources.py'))
SOURCES = _data['DAY16_SOURCES']
DAY16_PROPERTIES = _data['DAY16_PROPERTIES']
TEST_PROPERTIES = _data['TEST_PROPERTIES']
JPA_DEPENDENCIES = _data['JPA_DEPENDENCIES']
