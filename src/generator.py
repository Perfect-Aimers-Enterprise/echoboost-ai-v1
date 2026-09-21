from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from .config import settings
from .model import StoreModel
from .validator import extract_json, validate_store_spec, StoreSpecError

class StoreGenerator:
    def __init__(self) -> None:
        self.system_prompt = settings.prompt_path.read_text(encoding="utf-8")
        self.model = StoreModel()

    def generate(self, merchant_input: dict) -> dict:
        last_error = None
        for attempt in range(settings.generation_retries + 1):
            raw = self.model.generate(self.system_prompt, merchant_input)
            print("\n===== RAW MODEL OUTPUT =====\n")
            print(raw)
            print("\n===== END RAW MODEL OUTPUT =====\n")
            try:
                spec = extract_json(raw)
                validate_store_spec(spec)
                self._log(merchant_input, spec, attempt + 1)
                return spec
            except StoreSpecError as exc:
                last_error = exc
        raise StoreSpecError(f"StoreSpec generation failed after retries: {last_error}")

    def _log(self, merchant_input: dict, spec: dict, attempts: int) -> None:
        settings.log_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        record = {"schema_version":"1.0.0","created_at":datetime.now(timezone.utc).isoformat(),"merchant_input":merchant_input,"initial_store_spec":spec,"merchant_edits":None,"final_store_spec":None,"metadata":{"model_id":settings.model_id,"attempts":attempts}}
        (settings.log_dir / f"generation_{stamp}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
