"""Build German Content Block label catalogs from the generated English XLIFF files."""
from pathlib import Path
import xml.etree.ElementTree as ET

NS = "urn:oasis:names:tc:xliff:document:1.2"
ET.register_namespace("", NS)

PAIRS = """
Add 2 to 4 statistics.|||Fügen Sie 2 bis 4 Kennzahlen hinzu.
Add 2 to 6 projects.|||Fügen Sie 2 bis 6 Projekte hinzu.
Add 2 to 6 team members.|||Fügen Sie 2 bis 6 Teammitglieder hinzu.
Add 3 to 6 features.|||Fügen Sie 3 bis 6 Merkmale hinzu.
Add 3 to 6 services.|||Fügen Sie 3 bis 6 Leistungen hinzu.
Add 3 to 6 steps.|||Fügen Sie 3 bis 6 Schritte hinzu.
Add 3 to 8 logos. Use SVG or PNG with transparent background.|||Fügen Sie 3 bis 8 Logos hinzu. Verwenden Sie SVG oder PNG mit transparentem Hintergrund.
Add up to 3 testimonials.|||Fügen Sie bis zu 3 Kundenstimmen hinzu.
Add up to 8 questions.|||Fügen Sie bis zu 8 Fragen hinzu.
Additional note|||Zusätzlicher Hinweis
Additional paragraphs. Line breaks are preserved.|||Weitere Absätze. Zeilenumbrüche bleiben erhalten.
Address|||Adresse
Answer|||Antwort
Arrow|||Pfeil
Author name|||Name der zitierten Person
Avatar|||Profilbild
Background variant for the section.|||Hintergrundvariante für den Abschnitt.
Body text|||Fließtext
Brand|||Markenfarbe
Button label|||Schaltflächenbeschriftung
Button link|||Schaltflächenlink
Call to action|||Handlungsaufforderung
Caption|||Bildunterschrift
Category|||Kategorie
Centered introductory text with headline, lead paragraph and optional copy.|||Zentrierter Einführungstext mit Überschrift, Einleitung und optionalem Fließtext.
Check|||Häkchen
Clarify taxes, setup costs or custom quotes.|||Erläutern Sie Steuern, Einrichtungskosten oder individuelle Angebote.
Code|||Code
Company name|||Unternehmensname
Contact|||Kontakt
Contact details and optional image with an anchor for the primary CTA.|||Kontaktdaten und optionales Bild mit Anker für die wichtigste Handlungsaufforderung.
Container width|||Containerbreite
Custom SVG icon (overrides icon)|||Eigenes SVG-Symbol (ersetzt das gewählte Symbol)
Customer quotes with attribution. Up to three testimonials.|||Kundenstimmen mit Namensnennung. Bis zu drei Einträge.
Dark|||Dunkel
Default|||Standard
Description|||Beschreibung
Design|||Design
Displayed after the visitor selects Yearly; include the currency symbol.|||Wird bei jährlicher Abrechnung angezeigt; Währungssymbol angeben.
Editable service tiers with monthly and yearly prices.|||Bearbeitbare Leistungspakete mit monatlichen und jährlichen Preisen.
Email address|||E-Mail-Adresse
Enable for custom quotes such as “On request”.|||Für individuelle Angebote wie „Auf Anfrage“ aktivieren.
Enable only for the first block on the page to keep a single h1.|||Nur beim ersten Block der Seite aktivieren, damit es genau eine H1 gibt.
Eyebrow|||Oberzeile
FAQ|||Häufige Fragen
Feature grid|||Merkmalsraster
Feature title|||Titel des Merkmals
Features|||Merkmale
Frequently asked questions rendered as accessible disclosure widgets.|||Häufige Fragen als barrierearm bedienbare Aufklappelemente.
Full|||Volle Breite
Gallery|||Galerie
Gallery images|||Galeriebilder
Grid of feature highlights with title and description. Ideal for benefits or differentiators.|||Raster mit Merkmalen, Titel und Beschreibung. Für Vorteile und Unterschiede geeignet.
Headline|||Überschrift
Hero|||Einstiegsbereich
Hero image|||Bild im Einstiegsbereich
Hide billing suffix|||Abrechnungszusatz ausblenden
Highlight this tier|||Dieses Paket hervorheben
Icon|||Symbol
Image|||Bild
Image alt text override|||Alternativer Bildtext
Image gallery with captions and a keyboard-friendly lightbox.|||Bildergalerie mit Bildunterschriften und per Tastatur bedienbarer Großansicht.
Image on left|||Bild links
Image on right|||Bild rechts
Image position|||Bildposition
Include the currency symbol, e.g. €950. Use “On request” if needed.|||Währungssymbol angeben, z. B. 950 €. Bei Bedarf „Auf Anfrage“ verwenden.
Included features|||Enthaltene Leistungen
Intro|||Einführung
Introduction|||Einleitung
Key figures as a definition list. Use for proof points and credibility.|||Kennzahlen als Definitionsliste für Nachweise und Glaubwürdigkeit.
Label|||Beschriftung
Large|||Groß
Large introductory section with headline, supporting copy, calls to action and an optional visual.|||Großer Einstiegsbereich mit Überschrift, Text, Handlungsaufforderungen und optionalem Bild.
Larger introductory sentence.|||Größer dargestellter Einleitungssatz.
Lead paragraph|||Einleitungsabsatz
Leave empty to hide. Use page, URL or email.|||Leer lassen zum Ausblenden. Seite, URL oder E-Mail verwenden.
Leave empty to use file metadata.|||Leer lassen, um die Dateimetadaten zu verwenden.
Link|||Link
Link label|||Linkbeschriftung
Local 16:9 image, ideally 1200 × 675 pixels.|||Lokales Bild im Format 16:9, idealerweise 1200 × 675 Pixel.
Logo cloud|||Logoraster
Logo image|||Logobild
Logos|||Logos
Main headline of the hero.|||Hauptüberschrift des Einstiegsbereichs.
Maximum width of the content container.|||Maximale Breite des Inhaltsbereichs.
Members|||Mitglieder
Monthly price|||Monatlicher Preis
Monthly price suffix|||Zusatz zum Monatspreis
Name|||Name
Narrow|||Schmal
None|||Keines
Office hours|||Öffnungszeiten
Optional large visual. Recommended 1280x960, WebP or JPG.|||Optionales großes Bild. Empfohlen: 1280 × 960 Pixel, WebP oder JPG.
Optional — e.g. LinkedIn.|||Optional, z. B. LinkedIn.
Optional — e.g. case study.|||Optional, z. B. eine Fallstudie.
Optional — e.g. office or map placeholder.|||Optional, z. B. Büro oder Kartenplatzhalter.
Overview of agency services in a card grid.|||Übersicht der Leistungen als Kartenraster.
Phone number|||Telefonnummer
Placeholder: #|||Platzhalter: #
Placeholder: Crispframe shipped our platform in ten weeks — on time and without a content freeze.|||Beispiel: Unsere Plattform war in zehn Wochen online – pünktlich und ohne Redaktionsstopp.
Placeholder: Digital Strategy|||Beispiel: Digitale Strategie
Placeholder: Discovery|||Beispiel: Analyse
Placeholder: Discovery takes 2 weeks, build 6–10 weeks. We ship an MVP early and iterate in sprints.|||Beispiel: Die Analyse dauert zwei Wochen, die Umsetzung sechs bis zehn Wochen. Eine erste Version erscheint früh.
Placeholder: Editor-first content|||Beispiel: Redaktion im Mittelpunkt
Placeholder: Head of Digital, Nordlicht Labs|||Beispiel: Leitung Digital, Muster GmbH
Placeholder: Headless TYPO3 storefront that lifted conversion by 34%.|||Beispiel: TYPO3-Shop mit 34 % höherer Conversion-Rate.
Placeholder: How long does a typical project take?|||Beispiel: Wie lange dauert ein typisches Projekt?
Placeholder: Laura Meier|||Beispiel: Laura Meier
Placeholder: Learn more|||Beispiel: Mehr erfahren
Placeholder: Managing Director|||Beispiel: Geschäftsführung
Placeholder: Maya Keller|||Beispiel: Maya Keller
Placeholder: Nordlicht Commerce Relaunch|||Beispiel: Relaunch eines Onlineshops
Placeholder: Nordlicht Labs|||Beispiel: Muster GmbH
Placeholder: Product strategist with 15 years in digital transformation.|||Beispiel: Produktstrategin mit 15 Jahren Erfahrung in der digitalen Transformation.
Placeholder: Profile — shown on the team card button|||Beispiel: Profil – erscheint auf der Teamkarte
Placeholder: Roadmaps that connect business goals to measurable outcomes.|||Beispiel: Fahrpläne, die Geschäftsziele mit messbaren Ergebnissen verbinden.
Placeholder: Structured blocks editors love — no developer needed for everyday changes.|||Beispiel: Strukturierte Bausteine für Änderungen ohne Entwicklungsteam.
Placeholder: View project|||Beispiel: Projekt ansehen
Placeholder: Workshops and research to define goals and success metrics.|||Beispiel: Workshops und Recherche für Ziele und Erfolgskriterien.
Plain text transcript for accessibility and visitors who do not play the video.|||Transkript als Klartext für Barrierefreiheit und Besucher ohne Videowiedergabe.
Portrait|||Porträt
Poster image|||Vorschaubild
Price when billed yearly|||Preis bei jährlicher Abrechnung
Pricing|||Preise
Pricing note|||Preishinweis
Pricing tiers|||Preispakete
Primary button label|||Beschriftung der ersten Schaltfläche
Primary button link|||Link der ersten Schaltfläche
Privacy-friendly YouTube or Vimeo video with a local poster and transcript.|||YouTube- oder Vimeo-Video mit lokalem Vorschaubild und Transkript; Einbettung erst nach Klick.
Process|||Ablauf
Profile link|||Profillink
Project image|||Projektbild
Project title|||Projekttitel
Projects|||Projekte
Prominent call to action with headline and up to two buttons.|||Auffällige Handlungsaufforderung mit Überschrift und bis zu zwei Schaltflächen.
Question|||Frage
Questions|||Fragen
Quote|||Zitat
Role|||Funktion
Role and company|||Funktion und Unternehmen
Row of client or partner logos with optional links.|||Reihe mit Kunden- oder Partnerlogos und optionalen Links.
Secondary button label|||Beschriftung der zweiten Schaltfläche
Secondary button link|||Link der zweiten Schaltfläche
Section background|||Abschnittshintergrund
Section spacing|||Abschnittsabstand
Selected work with image, category and link.|||Ausgewählte Projekte mit Bild, Kategorie und Link.
Service title|||Leistungstitel
Services|||Leistungen
Short bio|||Kurzbiografie
Short description|||Kurzbeschreibung
Short paragraph below the headline.|||Kurzer Absatz unter der Überschrift.
Side image|||Bild seitlich
Small|||Klein
Small label shown above the headline.|||Kleine Beschriftung über der Überschrift.
Star|||Stern
Statistics|||Kennzahlen
Stats|||Kennzahlen
Step title|||Schritttitel
Step-by-step process from discovery to launch.|||Schrittweiser Ablauf von der Analyse bis zum Start.
Steps|||Schritte
Strategy|||Strategie
Subtle|||Dezent
Supporting text|||Begleittext
Team|||Team
Team members with photo, role and short bio.|||Teammitglieder mit Foto, Funktion und Kurzbiografie.
Testimonials|||Kundenstimmen
Text with image|||Text mit Bild
Tier name|||Paketname
Transcript|||Transkript
Two-column text and image combination with configurable image position.|||Zweispaltige Kombination aus Text und Bild mit wählbarer Bildposition.
Use a bulleted list. Keep each benefit short and concrete.|||Verwenden Sie eine Liste mit kurzen, konkreten Vorteilen.
Use h1 for headline|||Überschrift als H1 verwenden
Value|||Wert
Vertical spacing before and after the section.|||Vertikaler Abstand vor und nach dem Abschnitt.
Video|||Video
Video ID|||Video-ID
Video provider|||Videoanbieter
Vimeo|||Vimeo
What the number describes.|||Beschreibung der Kennzahl.
Wide|||Breit
Yearly price suffix|||Zusatz zum Jahrespreis
YouTube|||YouTube
YouTube ID (11 characters) or Vimeo numeric ID. The embed loads only after a visitor clicks play.|||YouTube-ID (11 Zeichen) oder numerische Vimeo-ID. Die Einbettung lädt erst nach einem Klick.
e.g. 120+, 98%, 4.9/5|||z. B. 120+, 98 %, 4,9/5
e.g. E-commerce, Corporate site|||z. B. Onlineshop, Unternehmenswebsite
"""
TRANSLATIONS = dict(line.split("|||", 1) for line in PAIRS.strip().splitlines())

block_root = Path(__file__).resolve().parents[1] / "packages/agency_theme/ContentBlocks/ContentElements"
missing = set()
count = 0
for source_path in sorted(block_root.glob("*/language/labels.xlf")):
    tree = ET.parse(source_path)
    file_element = tree.find(f".//{{{NS}}}file")
    file_element.set("target-language", "de")
    for unit in tree.findall(f".//{{{NS}}}trans-unit"):
        source = unit.find(f"{{{NS}}}source")
        value = source.text or ""
        if value not in TRANSLATIONS:
            missing.add(value)
            continue
        target = unit.find(f"{{{NS}}}target")
        if target is None:
            target = ET.SubElement(unit, f"{{{NS}}}target")
        target.text = TRANSLATIONS[value]
        count += 1
    ET.indent(tree, space="  ")
    tree.write(source_path.with_name("de.labels.xlf"), encoding="utf-8", xml_declaration=True)
if missing:
    raise SystemExit("Missing German translations: " + repr(sorted(missing)))
print(f"Translated {count} Content Block labels.")
