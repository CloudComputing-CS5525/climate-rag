from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────
ROOT_DIR        = Path(__file__).resolve().parent.parent
DATA_DIR        = ROOT_DIR / "data"
CHECKPOINT_DIR  = DATA_DIR / "checkpoints"

PAPERS_CHECKPOINT = CHECKPOINT_DIR / "papers.parquet"
CHUNKS_CHECKPOINT = CHECKPOINT_DIR / "chunks.parquet"
NODES_CHECKPOINT  = CHECKPOINT_DIR / "nodes.parquet"
EDGES_CHECKPOINT  = CHECKPOINT_DIR / "edges.parquet"
MAP_CHECKPOINT    = CHECKPOINT_DIR / "chunk_entity_map.parquet"

# ── Dataset ───────────────────────────────────────────────────
NUM_PAPERS      = 2000

# ── Climate filter keywords ───────────────────────────────────
CLIMATE_KEYWORDS = [
    "climate", "environment", "carbon", "emission",
    "atmospheric", "ocean", "renewable", "fossil fuel",
    "greenhouse", "temperature", "precipitation", "drought"
]

# ── Chunking ──────────────────────────────────────────────────
CHUNK_SIZE_WORDS    = 200
CHUNK_OVERLAP_WORDS = 30
MIN_CHUNK_WORDS     = 30

# ── Embedding ─────────────────────────────────────────────────
EMBEDDING_MODEL      = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_DIM        = 768
EMBEDDING_BATCH_SIZE = 64

# ── Knowledge Graph ───────────────────────────────────────────
SPACY_MODEL         = "en_core_sci_sm"
KG_MIN_NAME_LENGTH  = 3