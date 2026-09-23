"""Rebuild the curated SVG sprite from lucide-static 1.47.0.

Usage: npm pack lucide-static@1.47.0; unpack it; then pass the package path.
The checked-in sprite is the runtime asset; npm is not needed by TYPO3.
"""
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SPRITE = ROOT / "packages/agency_theme/Resources/Public/Icons/sprite.svg"
NOTICE = ROOT / "packages/agency_theme/Resources/Private/ThirdParty/LUCIDE-LICENSE"
NAMES = (
    "briefcase-business", "chart-no-axes-combined", "compass", "lightbulb",
    "shield-check", "globe-2", "users-round", "rocket", "sparkles",
    "target", "layers-3", "workflow", "heart-handshake", "building-2",
    "leaf", "zap", "puzzle", "lock-keyhole", "messages-square",
    "calendar-days", "monitor-smartphone", "award",
)

package = Path(sys.argv[1])
source = SPRITE.read_text(encoding="utf-8")
source = re.sub(r"<!-- Lucide v1\.47\.0 start -->.*?<!-- Lucide v1\.47\.0 end -->\n?", "", source, flags=re.S)
symbols = []
for name in NAMES:
    svg = (package / "icons" / f"{name}.svg").read_text(encoding="utf-8")
    body = svg[svg.index(">", svg.index("<svg")) + 1:].rsplit("</svg>", 1)[0].strip()
    symbols.append(
        f'<symbol id="icon-{name}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round">{body}</symbol>'
    )
block = "<!-- Lucide v1.47.0 start -->\n" + "\n".join(symbols) + "\n<!-- Lucide v1.47.0 end -->\n"
with SPRITE.open("w", encoding="utf-8", newline="\n") as output:
    output.write(source.replace("</svg>", block + "</svg>"))
NOTICE.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(package / "LICENSE", NOTICE)
print(f"Vendored {len(NAMES)} Lucide icons and license")
