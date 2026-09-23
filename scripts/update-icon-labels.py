"""Add the curated icon option labels to the Content Blocks catalogs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "packages/agency_theme/ContentBlocks/ContentElements"
LABELS = {
    "briefcase-business": ("Briefcase", "Aktenkoffer"),
    "chart-no-axes-combined": ("Growth", "Wachstum"),
    "compass": ("Compass", "Kompass"),
    "lightbulb": ("Idea", "Idee"),
    "shield-check": ("Trust", "Vertrauen"),
    "globe-2": ("Global", "Global"),
    "users-round": ("People", "Menschen"),
    "rocket": ("Launch", "Start"),
    "sparkles": ("Innovation", "Innovation"),
    "target": ("Goal", "Ziel"),
    "layers-3": ("Layers", "Ebenen"),
    "workflow": ("Workflow", "Arbeitsablauf"),
    "heart-handshake": ("Partnership", "Partnerschaft"),
    "building-2": ("Organization", "Organisation"),
    "leaf": ("Sustainability", "Nachhaltigkeit"),
    "zap": ("Energy", "Energie"),
    "puzzle": ("Integration", "Integration"),
    "lock-keyhole": ("Security", "Sicherheit"),
    "messages-square": ("Conversation", "Gespräch"),
    "calendar-days": ("Calendar", "Kalender"),
    "monitor-smartphone": ("Responsive", "Responsive"),
    "award": ("Award", "Auszeichnung"),
}
for block in ("services", "feature-grid"):
    for language in ("", "de."):
        path = ROOT / block / "language" / f"{language}labels.xlf"
        newline = "\r\n" if b"\r\n" in path.read_bytes() else "\n"
        xml = path.read_text(encoding="utf-8")
        if 'items.icon.items.briefcase-business.label' in xml:
            continue
        entries = []
        for value, (english, german) in LABELS.items():
            target = f"\n        <target>{german}</target>" if language else ""
            entries.append(f'      <trans-unit id="items.icon.items.{value}.label">\n        <source>{english}</source>{target}\n      </trans-unit>\n')
        marker = '      <trans-unit id="items.iconFile.label">'
        if marker not in xml:
            raise ValueError(f"Cannot find icon label insertion point: {path}")
        with path.open("w", encoding="utf-8", newline=newline) as output:
            output.write(xml.replace(marker, ''.join(entries) + marker, 1))
print("Updated English and German icon labels")
