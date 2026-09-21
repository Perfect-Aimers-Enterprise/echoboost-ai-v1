# Echoboost AI Store Generator V1

Echoboost AI V1 converts merchant requirements into a validated **StoreSpec JSON** that the main Echoboost frontend can render with predefined components.

## Architecture

`Merchant input -> Qwen3-1.7B -> StoreSpec JSON -> JSON Schema validation -> Echoboost renderer`

The model does **not** generate HTML/CSS/React/JS. The renderer owns the UI code; StoreSpec is the contract between AI and frontend.

## Why StoreSpec

The schema covers store identity, branding, colors, typography, navigation, homepage layout, product sections, categories, product-card behavior, banners/promotions, testimonials, FAQs, pages, footer, SEO, social links, checkout, currency, shipping, policies, and responsive behavior.

The contract is designed so the model can later be replaced by a smaller Echoboost-specific model without rebuilding the storefront renderer.

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
```

The first generation downloads the configured Hugging Face model. GPU/CUDA is used automatically when available; otherwise the runtime falls back to CPU. For low-memory CPU deployment, a future GGUF/llama.cpp backend can be added without changing StoreSpec.

## Commands

```bash
python -m src.main info
python -m src.main generate --input examples/fashion_store.json --output examples/generated_fashion.json
python -m pytest
```

## Generation logging

Successful generations are logged under `data/generations/` with:
- merchant input
- initial AI StoreSpec
- merchant edits placeholder
- final StoreSpec placeholder
- model metadata

This creates the future training dataset for Echoboost V2. Do not collect or train on merchant/customer data without the required permissions and privacy controls.

## V2 roadmap

V1 should run first without fine-tuning. Once Echoboost has enough high-quality merchant generation/edit pairs, those accepted StoreSpecs can become supervised training data for a smaller Echoboost-specific model.
