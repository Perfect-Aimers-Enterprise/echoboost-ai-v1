from __future__ import annotations
import json
import re
from jsonschema import Draft202012Validator
from .config import settings

class StoreSpecError(ValueError):
    pass

def load_schema() -> dict:
    return json.loads(settings.schema_path.read_text(encoding="utf-8"))

def extract_json(text: str) -> dict:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end <= start:
            raise StoreSpecError("Model output did not contain a JSON object.")
        try:
            return json.loads(cleaned[start:end + 1])
        except json.JSONDecodeError as exc:
            raise StoreSpecError(f"Invalid JSON from model: {exc}") from exc

def validate_store_spec(spec: dict) -> None:
    validator = Draft202012Validator(load_schema())
    errors = sorted(validator.iter_errors(spec), key=lambda e: list(e.path))
    if errors:
        details = "; ".join(f"{'.'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors[:8])
        raise StoreSpecError(details)
