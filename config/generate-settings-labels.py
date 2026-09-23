"""Build English/German XLIFF for the current Site Set definitions."""
from pathlib import Path
import xml.etree.ElementTree as ET
import yaml

base = Path(__file__).resolve().parents[1] / "packages/agency_theme/Configuration/Sets/SitePackage"
definitions = yaml.safe_load((base / "settings.definitions.yaml").read_text(encoding="utf-8"))
existing = {}
if (base / "labels.xlf").exists():
    for unit in ET.parse(base / "labels.xlf").findall(".//trans-unit"):
        existing[unit.attrib["id"]] = unit.findtext("source")
de = {
    "Crispframe Agency Theme": "Crispframe Unternehmensvorlage",
    "Brand": "Marke", "Contact": "Kontakt", "Social": "Soziale Netzwerke",
    "Footer": "Footer", "Call to Action": "Handlungsaufforderung", "Styles": "Gestaltung",
    "Company name": "Unternehmensname", "Displayed in header, footer and meta fallbacks.": "Wird in Kopf- und Fußbereich sowie als Meta-Fallback angezeigt.",
    "Tagline": "Kurzbeschreibung", "Short brand statement used in hero and footer.": "Kurze Markenaussage für Einstiegsbereich und Footer.",
    "Logo": "Logo", "Primary brand mark. SVG preferred.": "Primäres Markenzeichen. SVG wird empfohlen.",
    "Logo alt text": "Alternativer Text für das Logo", "Public email": "Öffentliche E-Mail-Adresse",
    "Phone": "Telefon", "E.164 preferred, e.g. +49 30 000000.": "E.164 wird empfohlen, z. B. +49 30 000000.",
    "Address": "Adresse", "Single-line or multiline postal address.": "Ein- oder mehrzeilige Postanschrift.",
    "LinkedIn URL": "LinkedIn-URL", "Instagram URL": "Instagram-URL", "GitHub URL": "GitHub-URL",
    "X / Twitter URL": "X-/Twitter-URL", "YouTube URL": "YouTube-URL",
    "Footer text": "Footertext", "Copyright / colophon line rendered in the footer.": "Copyright- oder Impressumshinweis im Footer.",
    "Legal notice link": "Link zum Impressum", "Privacy policy link": "Link zur Datenschutzerklärung",
    "Services parent page UID": "Übergeordnete Seite für Leistungen",
    "Page whose children populate the footer Services column. 0 disables the column (default). Set to a page UID (e.g. Services page) to enable.": "Unterseiten dieser Seite füllen die Leistungsspalte im Footer. 0 blendet sie aus.",
    "Show footer call to action": "Handlungsaufforderung im Footer anzeigen",
    "Footer call to action heading": "Überschrift der Footer-Handlungsaufforderung",
    "Footer call to action text": "Text der Footer-Handlungsaufforderung",
    "Primary CTA label": "Beschriftung der ersten Handlungsaufforderung",
    "Primary CTA link": "Link der ersten Handlungsaufforderung",
    "Secondary CTA label": "Beschriftung der zweiten Handlungsaufforderung",
    "Secondary CTA link": "Link der zweiten Handlungsaufforderung",
    "Content width": "Inhaltsbreite", "Maximum width of the main content area.": "Maximale Breite des Hauptinhalts.",
    "Colour palette": "Farbpalette", "Type scale": "Schriftgrößen", "Corner style": "Eckenstil",
    "Section spacing": "Abschnittsabstand", "Sticky header": "Fixierter Kopfbereich",
    "Keep the navigation visible while scrolling.": "Navigation beim Scrollen sichtbar halten.",
    "Show header button": "Schaltfläche im Kopfbereich anzeigen",
    "The button appears when a valid primary CTA link is configured.": "Die Schaltfläche erscheint, wenn ein gültiger Link für die erste Handlungsaufforderung gesetzt ist.",
}

def save(language: str) -> None:
    root = ET.Element("xliff", version="1.2")
    attributes = {"datatype": "plaintext", "original": "labels.xlf", "source-language": "en", "product-name": "crispframe/agency-theme"}
    if language == "de":
        attributes["target-language"] = "de"
    file_element = ET.SubElement(root, "file", attributes)
    body = ET.SubElement(file_element, "body")
    entries = {"label": "Crispframe Agency Theme"}
    for key, category in definitions["categories"].items():
        category = category or {}
        label_key = f"categories.{key}"
        entries[label_key] = category.get("label", existing.get(label_key))
    for key, setting in definitions["settings"].items():
        label_key = f"settings.{key}"
        description_key = f"settings.description.{key}"
        entries[label_key] = setting.get("label", existing.get(label_key))
        description = setting.get("description", existing.get(description_key))
        if description:
            entries[description_key] = description
    for key, source in entries.items():
        unit = ET.SubElement(body, "trans-unit", id=key)
        ET.SubElement(unit, "source").text = source
        if language == "de":
            if source not in de:
                raise ValueError(f"Missing German translation: {source}")
            ET.SubElement(unit, "target").text = de[source]
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(base / ("de.labels.xlf" if language == "de" else "labels.xlf"), encoding="utf-8", xml_declaration=True)

save("en")
save("de")
