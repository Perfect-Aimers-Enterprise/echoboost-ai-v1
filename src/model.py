from __future__ import annotations
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from .config import settings

class StoreModel:
    def __init__(self) -> None:
        self.device = self._resolve_device(settings.device)
        self.dtype = self._resolve_dtype(settings.dtype, self.device)
        kwargs = {"torch_dtype": self.dtype}
        if self.device == "cuda":
            kwargs["device_map"] = "auto"
        self.tokenizer = AutoTokenizer.from_pretrained(settings.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(settings.model_id, **kwargs)
        if self.device != "cuda":
            self.model.to(self.device)
        self.model.eval()

    @staticmethod
    def _resolve_device(value: str) -> str:
        if value != "auto":
            return value
        return "cuda" if torch.cuda.is_available() else "cpu"

    @staticmethod
    def _resolve_dtype(value: str, device: str):
        if value == "float16":
            return torch.float16
        if value == "bfloat16":
            return torch.bfloat16
        if value == "float32":
            return torch.float32
        return torch.bfloat16 if device == "cuda" and torch.cuda.is_bf16_supported() else (torch.float16 if device == "cuda" else torch.float32)

    def generate(self, system_prompt: str, merchant_input: dict) -> str:
        user_payload = json.dumps(merchant_input, ensure_ascii=False, indent=2)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create a complete StoreSpec for this merchant input:\n{user_payload}"},
        ]
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        target = next(self.model.parameters()).device
        inputs = {k: v.to(target) for k, v in inputs.items()}
        with torch.inference_mode():
            output = self.model.generate(**inputs, max_new_tokens=settings.max_new_tokens, do_sample=settings.temperature > 0, temperature=settings.temperature, top_p=settings.top_p)
        generated = output[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(generated, skip_special_tokens=True).strip()
