from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

def _int(name: str, default: int) -> int:
    return int(os.getenv(name, default))

def _float(name: str, default: float) -> float:
    return float(os.getenv(name, default))

@dataclass(frozen=True)
class Settings:
    model_id: str = os.getenv("ECHOBOOST_MODEL_ID", "Qwen/Qwen3-1.7B")
    device: str = os.getenv("ECHOBOOST_DEVICE", "auto")
    dtype: str = os.getenv("ECHOBOOST_DTYPE", "auto")
    max_new_tokens: int = _int("ECHOBOOST_MAX_NEW_TOKENS", 3000)
    temperature: float = _float("ECHOBOOST_TEMPERATURE", 0.2)
    top_p: float = _float("ECHOBOOST_TOP_P", 0.9)
    generation_retries: int = _int("ECHOBOOST_GENERATION_RETRIES", 2)
    log_dir: Path = ROOT / os.getenv("ECHOBOOST_LOG_DIR", "data/generations")
    schema_path: Path = ROOT / "schemas/store_spec.schema.json"
    prompt_path: Path = ROOT / "prompts/store_generator.txt"

settings = Settings()
