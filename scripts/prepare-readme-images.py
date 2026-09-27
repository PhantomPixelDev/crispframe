"""Encode real browser captures for the README; requires Pillow."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "output/playwright"
TARGET = ROOT / "packages/agency_theme/Documentation/Images"
NAMES = (
    "home-desktop", "home-mobile", "work-desktop", "contact-desktop",
    "services-desktop", "about-desktop", "insights-desktop",
    "resources-desktop", "article-desktop", "case-study-de-desktop",
    "pricing-block", "service-cards", "mega-menu", "contact-form", "mobile-menu",
    "style-variants-desktop", "style-variants-de-desktop",
)

missing = [name for name in NAMES if not (SOURCE / f"readme-{name}.png").is_file()]
if missing:
    raise SystemExit("Capture screenshots first; missing: " + ", ".join(missing))
TARGET.mkdir(parents=True, exist_ok=True)
for name in NAMES:
    with Image.open(SOURCE / f"readme-{name}.png") as image:
        image.convert("RGB").save(TARGET / f"{name}.webp", "WEBP", quality=84, method=6)
print(f"Encoded {len(NAMES)} screenshots without cropping or retouching.")
