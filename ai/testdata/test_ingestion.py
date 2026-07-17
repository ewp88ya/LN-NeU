import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from processing import DataIngestionPipeline
from memory.vector.search import VectorSearch

pipeline = DataIngestionPipeline()

pipeline.ingest("testdata/sample.txt")

search = VectorSearch(pipeline.vector)

print(search.search("workflow"))
