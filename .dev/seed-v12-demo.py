"""Maintainer-only, additive authoring script for the v1.2 demo export.

Run inside the local Podman web container after extension:setup. The public demo
distribution installs only the exported Initialisation/data.xml, never this script.
"""

import hashlib
import shutil
import sqlite3
import subprocess
import time
from pathlib import Path

DB = subprocess.check_output([
    "php", "-r",
    "$settings = require '/app/config/system/settings.php'; echo $settings['DB']['Connections']['Default']['path'];",
], text=True).strip()
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row
now = int(time.time())


def copy_row(table, source_uid, overrides, *, keep_block=None):
    source = dict(db.execute(f"SELECT * FROM {table} WHERE uid = ?", (source_uid,)).fetchone())
    source.pop("uid")
    if table == "tt_content":
        source = {key: value for key, value in source.items() if not key.startswith("crispframe_") or (keep_block and key.startswith(keep_block))}
    source.update(overrides)
    if "tstamp" in source:
        source["tstamp"] = now
    if "crdate" in source:
        source["crdate"] = now
    columns = ", ".join(source)
    placeholders = ", ".join("?" for _ in source)
    return db.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(source.values())).lastrowid


def page(title, slug, sorting, *, german=False, parent=0, description=""):
    existing = db.execute("SELECT uid FROM pages WHERE slug = ? AND sys_language_uid = ? AND deleted = 0", (slug, int(german))).fetchone()
    if existing:
        return existing[0]
    return copy_row("pages", 6 if german else 2, {
        "pid": 1, "sorting": sorting, "title": title, "nav_title": title,
        "slug": slug, "sys_language_uid": int(german), "l10n_parent": parent,
        "l10n_source": 0, "nav_hide": 0, "hidden": 0,
        "description": description, "seo_title": title,
    })


def block(pid, language, parent, kind, header, fields, sorting):
    existing = db.execute("SELECT uid FROM tt_content WHERE pid = ? AND sys_language_uid = ? AND header = ? AND deleted = 0", (pid, language, header)).fetchone()
    if existing:
        return existing[0]
    values = {
        "pid": pid, "sorting": sorting, "colPos": 0,
        "sys_language_uid": language, "l18n_parent": parent,
        "CType": f"crispframe_{kind}", "header": header,
        "hidden": 0, "deleted": 0,
    }
    values.update({f"crispframe_{kind}_{key}": value for key, value in fields.items()})
    return copy_row("tt_content", 2, values)


def add_items(table, pid, parent_uid, language, rows, base_uids=()):
    if db.execute(f"SELECT COUNT(*) FROM {table} WHERE foreign_table_parent_uid = ?", (parent_uid,)).fetchone()[0]:
        return []
    ids = []
    for index, values in enumerate(rows):
        record = {
            "pid": pid, "tstamp": now, "crdate": now, "sorting": (index + 1) * 128,
            "sys_language_uid": language, "l10n_parent": base_uids[index] if base_uids else 0,
            "foreign_table_parent_uid": parent_uid,
        }
        record.update(values)
        columns = ", ".join(record)
        placeholders = ", ".join("?" for _ in record)
        ids.append(db.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(record.values())).lastrowid)
    return ids


def content_pair(pid, kind, label, english, deutsch, en_items=(), de_items=(), sorting=128, background="default", layout=None):
    common = {"sectionSpacing": "default", "sectionBackground": background, "width": "default"}
    en_fields = {**common, **english}
    de_fields = {**common, **deutsch}
    if layout:
        en_fields["layout"] = de_fields["layout"] = layout
    if en_items:
        key = "rows" if kind == "comparison" else "items"
        en_fields[key] = de_fields[key] = len(en_items)
    english_uid = block(pid, 0, 0, kind, f"Demo 1.2: {label}", en_fields, sorting)
    german_uid = block(pid, 1, english_uid, kind, f"Demo 1.2: {label} DE", de_fields, sorting)
    if en_items:
        table = f"crispframe_{kind}_{key}"
        base_ids = add_items(table, pid, english_uid, 0, en_items)
        if not base_ids:
            base_ids = [r[0] for r in db.execute(f"SELECT uid FROM {table} WHERE foreign_table_parent_uid = ? ORDER BY sorting", (english_uid,))]
        add_items(table, pid, german_uid, 1, de_items, base_ids)
    return english_uid, german_uid


assert db.execute("SELECT title FROM pages WHERE uid = 1").fetchone()[0] == "Home"
services = page("Services", "/services", 256, description="Strategy, design and engineering services that move your organisation forward.")
page("Leistungen", "/leistungen", 256, german=True, parent=services, description="Strategie, Design und Entwicklung für den nächsten Schritt Ihrer Organisation.")
about = page("About", "/about", 320, description="Meet the people and principles behind our work.")
page("Über uns", "/ueber-uns", 320, german=True, parent=about, description="Lernen Sie die Menschen und Prinzipien hinter unserer Arbeit kennen.")

content_pair(services, "intro", "services opening", {
    "headline": "Services shaped around your goals", "lead": "From the first question to a better digital experience.",
    "text": "We bring research, clear design and dependable engineering together. Choose the support you need now, then grow it as your organisation changes.",
    "linkLabel": "Start a conversation", "link": "/contact", "width": "narrow",
}, {
    "headline": "Leistungen für Ihre Ziele", "lead": "Von der ersten Frage bis zum besseren digitalen Erlebnis.",
    "text": "Wir verbinden Recherche, klares Design und verlässliche Entwicklung. Wählen Sie die Unterstützung, die Sie jetzt brauchen, und entwickeln Sie sie mit Ihrer Organisation weiter.",
    "linkLabel": "Gespräch beginnen", "link": "/contact", "width": "narrow",
}, sorting=128)

comparison_en = [
    {"label": "Starting point", "firstValue": "A predefined scope", "secondValue": "A focused discovery of your needs"},
    {"label": "Design decisions", "firstValue": "Based on assumptions", "secondValue": "Grounded in evidence and feedback"},
    {"label": "Delivery", "firstValue": "One large handover", "secondValue": "Useful releases you can review early"},
    {"label": "After launch", "firstValue": "A fixed end date", "secondValue": "Room to measure, learn and improve"},
]
comparison_de = [
    {"label": "Ausgangspunkt", "firstValue": "Ein vorgegebener Umfang", "secondValue": "Ein genauer Blick auf Ihre Anforderungen"},
    {"label": "Designentscheidungen", "firstValue": "Auf Annahmen gestützt", "secondValue": "Mit Erkenntnissen und Feedback belegt"},
    {"label": "Umsetzung", "firstValue": "Eine große Übergabe", "secondValue": "Frühe, überprüfbare Ergebnisse"},
    {"label": "Nach dem Start", "firstValue": "Ein festes Enddatum", "secondValue": "Raum für Messung und Verbesserung"},
]
content_pair(services, "comparison", "comparison", {
    "headline": "A more considered way to build", "lead": "A comparison of common delivery approaches, not a promise that one size fits all.",
    "firstHeading": "Fixed delivery", "secondHeading": "Collaborative delivery", "emphasizeSecond": 1,
}, {
    "headline": "Bewusster entwickeln", "lead": "Zwei mögliche Vorgehensweisen im Vergleich. Jedes Projekt braucht eine passende Lösung.",
    "firstHeading": "Feste Umsetzung", "secondHeading": "Gemeinsame Umsetzung", "emphasizeSecond": 1,
}, comparison_en, comparison_de, sorting=256, background="subtle")

service_steps_en = [
    {"period": "01 · Discover", "title": "Understand the opportunity", "description": "Align goals, audiences and constraints before making decisions."},
    {"period": "02 · Shape", "title": "Create a useful direction", "description": "Test content, journeys and visual ideas with the people who will use them."},
    {"period": "03 · Build", "title": "Deliver in visible steps", "description": "Release working software, check quality and keep editors involved."},
    {"period": "04 · Evolve", "title": "Improve from evidence", "description": "Learn from real use and make the next change count."},
]
service_steps_de = [
    {"period": "01 · Verstehen", "title": "Die Aufgabe klären", "description": "Ziele, Zielgruppen und Grenzen vor den ersten Entscheidungen abstimmen."},
    {"period": "02 · Gestalten", "title": "Eine Richtung entwickeln", "description": "Inhalte, Wege und Gestaltung mit den Menschen prüfen, die sie nutzen."},
    {"period": "03 · Umsetzen", "title": "In sichtbaren Schritten liefern", "description": "Funktionierende Lösungen veröffentlichen und Redaktionsteams einbeziehen."},
    {"period": "04 · Verbessern", "title": "Aus Erfahrung lernen", "description": "Die echte Nutzung auswerten und gezielt weiterentwickeln."},
]
content_pair(services, "timeline", "service roadmap", {
    "headline": "A clear path from idea to improvement", "lead": "Every stage has a purpose and a useful outcome.",
}, {
    "headline": "Ein klarer Weg von der Idee zur Verbesserung", "lead": "Jede Phase hat ein Ziel und ein nutzbares Ergebnis.",
}, service_steps_en, service_steps_de, sorting=384, layout="rail")

content_pair(services, "cta", "services invitation", {
    "headline": "Tell us what you want to change", "text": "A short conversation is enough to find a practical first step.",
    "primaryLinkLabel": "Get in touch", "primaryLink": "/contact",
}, {
    "headline": "Erzählen Sie uns von Ihrem Vorhaben", "text": "Ein kurzes Gespräch genügt für den ersten sinnvollen Schritt.",
    "primaryLinkLabel": "Kontakt aufnehmen", "primaryLink": "/contact",
}, sorting=512, background="brand")

content_pair(about, "intro", "about opening", {
    "headline": "A small team with a wide view", "lead": "We care about what happens after a site goes live.",
    "text": "Our work combines thoughtful strategy, accessible design and maintainable technology. We make room for your team to own the result.",
    "linkLabel": "See our work", "link": "/work", "width": "narrow",
}, {
    "headline": "Ein kleines Team mit weitem Blick", "lead": "Uns interessiert, was nach dem Start einer Website passiert.",
    "text": "Unsere Arbeit verbindet durchdachte Strategie, zugängliches Design und wartbare Technik. Ihr Team soll das Ergebnis selbst weiterführen können.",
    "linkLabel": "Projekte ansehen", "link": "/work", "width": "narrow",
}, sorting=128)

about_steps_en = [
    {"period": "Listen", "title": "Start with context", "description": "Good questions reveal the real problem before a solution takes shape."},
    {"period": "Make", "title": "Work in the open", "description": "Shared prototypes and frequent reviews keep decisions understandable."},
    {"period": "Hand over", "title": "Leave room to grow", "description": "Clear systems let the people behind a website keep it useful."},
]
about_steps_de = [
    {"period": "Zuhören", "title": "Mit dem Kontext beginnen", "description": "Gute Fragen zeigen die eigentliche Aufgabe, bevor eine Lösung entsteht."},
    {"period": "Gestalten", "title": "Offen zusammenarbeiten", "description": "Gemeinsame Prototypen und regelmäßige Rückmeldungen machen Entscheidungen verständlich."},
    {"period": "Weitergeben", "title": "Platz für Entwicklung lassen", "description": "Klare Systeme helfen den Menschen hinter einer Website, sie nützlich zu halten."},
]
content_pair(about, "timeline", "working principles", {
    "headline": "Principles that shape our work", "lead": "A simple way to explain how we collaborate.",
}, {
    "headline": "Prinzipien unserer Arbeit", "lead": "So gestalten wir die Zusammenarbeit.",
}, about_steps_en, about_steps_de, sorting=256, background="subtle", layout="cards")

content_pair(about, "cta", "about invitation", {
    "headline": "Work with people who listen", "text": "Bring your challenge. We will bring curiosity and a clear next step.",
    "primaryLinkLabel": "Start a project", "primaryLink": "/contact",
}, {
    "headline": "Arbeiten Sie mit Menschen, die zuhören", "text": "Bringen Sie Ihre Aufgabe mit. Wir finden gemeinsam den nächsten Schritt.",
    "primaryLinkLabel": "Projekt starten", "primaryLink": "/contact",
}, sorting=384, background="brand")

content_pair(4, "comparison", "component comparison", {
    "headline": "Compare two ways of working", "lead": "Editors can change both headings and every row.",
    "firstHeading": "Starting point", "secondHeading": "Next step", "emphasizeSecond": 1,
}, {
    "headline": "Zwei Arbeitsweisen vergleichen", "lead": "Redaktionsteams können beide Überschriften und jede Zeile ändern.",
    "firstHeading": "Ausgangspunkt", "secondHeading": "Nächster Schritt", "emphasizeSecond": 1,
}, comparison_en[:2], comparison_de[:2], sorting=1920, background="subtle")
content_pair(4, "timeline", "component timeline", {
    "headline": "Milestones in context", "lead": "Switch between a vertical rail and responsive cards in the editor.",
}, {
    "headline": "Meilensteine im Zusammenhang", "lead": "Im Editor zwischen vertikaler Linie und responsiven Karten wechseln.",
}, about_steps_en, about_steps_de, sorting=2048, layout="cards")


def demo_file(filename):
    identifier = f"/user_upload/crispframe-demo/{filename}"
    source = Path("/app/packages/agency_demo/Resources/Public/Images") / filename
    destination = Path("/app/public/fileadmin") / identifier.lstrip("/")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.copyfile(source, destination)
    existing = db.execute("SELECT uid FROM sys_file WHERE identifier = ?", (identifier,)).fetchone()
    if existing:
        return existing[0]
    file_uid = copy_row("sys_file", 9, {
        "identifier": identifier,
        "identifier_hash": hashlib.sha1(identifier.encode()).hexdigest(),
        "name": filename,
        "sha1": hashlib.sha1(destination.read_bytes()).hexdigest(),
        "size": destination.stat().st_size,
        "tstamp": now,
        "last_indexed": now,
        "creation_date": now,
        "modification_date": now,
    })
    copy_row("sys_file_metadata", db.execute("SELECT uid FROM sys_file_metadata WHERE file = 9").fetchone()[0], {
        "file": file_uid, "title": "", "description": "", "alternative": "",
    })
    return file_uid


def hero(pid, label, image_uid, english, deutsch, alt_en, alt_de):
    base_header = f"Demo 1.2: {label} hero"
    existing = db.execute("SELECT uid FROM tt_content WHERE pid = ? AND header = ? AND deleted = 0", (pid, base_header)).fetchone()
    if existing:
        return
    base = copy_row("tt_content", 1, {
        "pid": pid, "sorting": 64, "colPos": 0, "header": base_header,
        "sys_language_uid": 0, "l18n_parent": 0,
        "crispframe_hero_eyebrow": english[0],
        "crispframe_hero_headline": english[1],
        "crispframe_hero_subheadline": english[2],
        "crispframe_hero_primaryLinkLabel": english[3],
        "crispframe_hero_primaryLink": "/contact",
        "crispframe_hero_secondaryLinkLabel": "",
        "crispframe_hero_secondaryLink": "",
        "crispframe_hero_imageAlt": alt_en,
        "crispframe_hero_sectionSpacing": "default",
    }, keep_block="crispframe_hero_")
    localized = copy_row("tt_content", 14, {
        "pid": pid, "sorting": 64, "colPos": 0, "header": base_header + " DE",
        "sys_language_uid": 1, "l18n_parent": base,
        "crispframe_hero_eyebrow": deutsch[0],
        "crispframe_hero_headline": deutsch[1],
        "crispframe_hero_subheadline": deutsch[2],
        "crispframe_hero_primaryLinkLabel": deutsch[3],
        "crispframe_hero_primaryLink": "/contact",
        "crispframe_hero_secondaryLinkLabel": "",
        "crispframe_hero_secondaryLink": "",
        "crispframe_hero_imageAlt": alt_de,
        "crispframe_hero_sectionSpacing": "default",
    }, keep_block="crispframe_hero_")
    reference = copy_row("sys_file_reference", 5, {
        "pid": pid, "uid_local": image_uid, "uid_foreign": base,
        "sys_language_uid": 0, "l10n_parent": 0, "alternative": alt_en,
    })
    copy_row("sys_file_reference", 6, {
        "pid": pid, "uid_local": image_uid, "uid_foreign": localized,
        "sys_language_uid": 1, "l10n_parent": reference, "alternative": alt_de,
    })


hero(services, "services", demo_file("services-team.webp"),
     ("Strategy · Design · Engineering", "Services for meaningful progress", "Focused help from the first question through launch and beyond.", "Let's talk"),
     ("Strategie · Design · Entwicklung", "Leistungen für echten Fortschritt", "Gezielte Unterstützung von der ersten Frage bis über den Start hinaus.", "Kontakt aufnehmen"),
     "Three colleagues review digital strategy concepts around a studio table",
     "Drei Kolleginnen und Kollegen besprechen digitale Konzepte am Studiotisch")
hero(about, "about", demo_file("about-team.webp"),
     ("People · Principles · Practice", "Good work is made together", "A collaborative team that turns complex challenges into clear digital experiences.", "Meet us"),
     ("Menschen · Haltung · Praxis", "Gute Arbeit entsteht gemeinsam", "Ein Team, das komplexe Aufgaben in klare digitale Erlebnisse übersetzt.", "Uns kennenlernen"),
     "Colleagues share ideas in a bright, relaxed studio conversation",
     "Kolleginnen und Kollegen tauschen sich in einem hellen Studio aus")

db.execute("UPDATE tt_content SET crispframe_intro_sectionSpacing = 'small' WHERE header IN (?, ?) AND CType = 'crispframe_intro'", ("Demo 1.2: services opening", "Demo 1.2: about opening"))
db.execute("UPDATE tt_content SET crispframe_intro_sectionSpacing = 'small' WHERE header IN (?, ?) AND CType = 'crispframe_intro'", ("Demo 1.2: services opening DE", "Demo 1.2: about opening DE"))

db.commit()
print("Added Services, About and comparison/timeline examples in English and German.")
