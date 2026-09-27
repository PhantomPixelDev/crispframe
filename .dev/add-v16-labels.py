"""Add the bilingual labels for the fixed 1.6 block presentation choices."""

from pathlib import Path
from xml.sax.saxutils import escape

root = Path(__file__).resolve().parents[1] / "packages/agency_theme/ContentBlocks/ContentElements"
choices = {
    "hero": ("headlineMeasure", [("label", "Headline width", "Überschriftenbreite"), ("description", "Control how the headline wraps without changing its font size.", "Steuert den Zeilenumbruch der Überschrift, ohne die Schriftgröße zu ändern."), ("items.narrow.label", "Narrow", "Schmal"), ("items.standard.label", "Standard", "Standard"), ("items.wide.label", "Wide", "Breit")]),
    "services": ("cardStyle", [("label", "Service presentation", "Darstellung der Leistungen"), ("description", "Choose contained cards or open icon-and-text columns.", "Wählen Sie Karten oder offene Spalten mit Symbol und Text."), ("items.cards.label", "Cards", "Karten"), ("items.open.label", "Open columns", "Offene Spalten")]),
    "feature-grid": ("featureStyle", [("label", "Feature presentation", "Darstellung der Merkmale"), ("description", "Choose contained cards or open icon-and-text columns.", "Wählen Sie Karten oder offene Spalten mit Symbol und Text."), ("items.cards.label", "Cards", "Karten"), ("items.open.label", "Open columns", "Offene Spalten")]),
    "projects": ("projectStyle", [("label", "Project presentation", "Darstellung der Projekte"), ("description", "Choose cards or editorial image-and-text rows.", "Wählen Sie Karten oder redaktionelle Reihen mit Bild und Text."), ("items.cards.label", "Cards", "Karten"), ("items.rows.label", "Editorial rows", "Redaktionelle Reihen")]),
    "testimonials": ("quoteStyle", [("label", "Quote presentation", "Darstellung der Zitate"), ("description", "Choose contained cards or open quotes with a subtle divider.", "Wählen Sie Karten oder offene Zitate mit einer dezenten Trennlinie."), ("items.cards.label", "Cards", "Karten"), ("items.open.label", "Open quotes", "Offene Zitate")]),
    "cta": ("ctaStyle", [("label", "Call-to-action presentation", "Darstellung des Handlungsaufrufs"), ("description", "Choose a contained panel or an open section.", "Wählen Sie eine umrahmte Fläche oder einen offenen Abschnitt."), ("items.panel.label", "Contained panel", "Umrahmte Fläche"), ("items.open.label", "Open section", "Offener Abschnitt")]),
}

for block, (field, labels) in choices.items():
    for filename, german in (("labels.xlf", False), ("de.labels.xlf", True)):
        path = root / block / "language" / filename
        content = path.read_text(encoding="utf-8")
        if block == "cta":
            content = content.replace("<source>CTA presentation</source>", "<source>Call-to-action presentation</source>")
        for suffix, en, de in labels:
            key = f"{field}.{suffix}"
            if f'id="{key}"' in content:
                continue
            xml = f'      <trans-unit id="{key}"><source>{escape(en)}</source>'
            if german:
                xml += f'<target>{escape(de)}</target>'
            xml += '</trans-unit>\n'
            content = content.replace('    </body>', xml + '    </body>')
        original_newline = "\r\n" if german and block != "hero" else "\n"
        with path.open("w", encoding="utf-8", newline=original_newline) as output:
            output.write(content)
