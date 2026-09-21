from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .config import settings
from .model import StoreModel
from .generator import StoreGenerator

def load_input(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def cmd_info() -> None:
    import torch
    print(f"Model: {settings.model_id}")
    print(f"Device: {settings.device} (CUDA available: {torch.cuda.is_available()})")
    print(f"Schema: {settings.schema_path}")

def cmd_generate(args) -> None:
    spec = StoreGenerator().generate(load_input(args.input))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated: {output}")

def cmd_interactive() -> None:
    print("Enter merchant JSON. Finish with an empty line:")
    lines=[]
    while True:
        line=input()
        if not line: break
        lines.append(line)
    merchant=json.loads("\n".join(lines))
    print(json.dumps(StoreGenerator().generate(merchant), ensure_ascii=False, indent=2))

def main() -> None:
    parser=argparse.ArgumentParser(description="Echoboost AI Store Generator")
    sub=parser.add_subparsers(dest="command", required=True)
    sub.add_parser("info")
    p=sub.add_parser("generate"); p.add_argument("--input",required=True); p.add_argument("--output",required=True)
    sub.add_parser("interactive")
    args=parser.parse_args()
    {"info":cmd_info,"generate":cmd_generate,"interactive":cmd_interactive}[args.command](args) if args.command=="generate" else {"info":cmd_info,"interactive":cmd_interactive}[args.command]()

if __name__ == "__main__":
    main()
