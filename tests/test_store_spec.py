import json
from pathlib import Path
from src.validator import validate_store_spec, extract_json

ROOT = Path(__file__).resolve().parents[1]

def test_schema_file_loads():
    schema = json.loads((ROOT / "schemas/store_spec.schema.json").read_text())
    assert schema["$schema"].endswith("draft/2020-12/schema")

def test_json_extraction():
    assert extract_json("```json\n{\"ok\": true}\n```") == {"ok": True}

def test_sample_store_spec_valid():
    spec = {
      "schema_version":"1.0.0",
      "store":{"name":"Test","description":"Test","industry":"fashion","target_audience":"customers","locale":"en-NG","currency":"NGN"},
      "branding":{"style":"modern","colors":{"primary":"#111111","secondary":"#222222","accent":"#ff6600","background":"#ffffff","surface":"#f5f5f5","text":"#111111","muted_text":"#666666"},"typography":{"heading":"Inter","body":"Inter","scale":"compact"},"imagery":{"direction":"clean","product_image_style":"studio","use_lifestyle_images":True}},
      "navigation":{"items":[{"label":"Shop","href":"/shop","visible":True}],"mobile_behavior":"drawer","show_search":True,"show_cart":True,"show_account":True},
      "homepage":{"layout_variant":"hero_catalog","hero":{"headline":"Shop","subheadline":"Discover products","primary_cta":{"label":"Shop now","action":"/shop"},"secondary_cta":{"label":"Learn more","action":"/about"},"image_direction":"product","alignment":"left"},"sections":[{"id":"featured","type":"featured_products","title":"Featured","description":"","enabled":True,"variant":"grid"}]},
      "catalog":{"categories":[],"product_card":{"show_image":True,"show_badge":True,"show_rating":True,"show_price":True,"show_compare":False,"show_quick_view":True,"show_add_to_cart":True,"image_ratio":"1:1","hover_behavior":"lift"},"sorting":["featured"],"filters":["category"],"catalog_layout":"grid"},
      "pages":{k:{"enabled":True,"title":k.title(),"content_direction":"merchant-provided"} for k in ["about","contact","faq","shipping"]},
      "footer":{"layout_variant":"columns","columns":[],"show_newsletter":True,"show_social":True,"show_payment_methods":True,"copyright_text":""},
      "commerce":{"checkout_mode":"cart","guest_checkout":True,"account_required":False,"currency":"NGN","shipping":{"enabled":True,"information":"Merchant configures shipping","zones":[]},"payments":{"enabled":True,"methods":["card"]}},
      "seo":{"title":"Test Store","description":"Test store","keywords":["test"],"og_image_direction":"brand"},
      "social":{"enabled":False,"links":[]},
      "policies":{"returns":"","privacy":"","terms":"","cancellation":""},
      "responsive":{"mobile_first":True,"breakpoints":["640px","768px","1024px"],"behavior":["stack sections on mobile"]}
    }
    validate_store_spec(spec)
