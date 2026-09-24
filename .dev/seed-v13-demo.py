"""Maintainer-only additive 1.3 demo authoring; never run on an installed customer site."""

import hashlib
import os
import shutil
import sqlite3
import subprocess
import time
from pathlib import Path

site_root = Path(os.environ.get('CRISPFRAME_SITE_ROOT', '/app'))
db_path = subprocess.check_output([
    'php', '-r', "$s=require $argv[1]; echo $s['DB']['Connections']['Default']['path'];",
    str(site_root / 'config/system/settings.php'),
], text=True).strip()
db = sqlite3.connect(db_path)
db.row_factory = sqlite3.Row
now = int(time.time())


def copy_row(table, uid, updates, prefix=None):
    row = dict(db.execute(f'SELECT * FROM {table} WHERE uid=?', (uid,)).fetchone())
    row.pop('uid')
    if prefix and table == 'tt_content':
        row = {k: v for k, v in row.items() if not k.startswith('crispframe_') or k.startswith(prefix)}
    row.update(updates)
    for key in ('tstamp', 'crdate'):
        if key in row:
            row[key] = now
    keys = ','.join(row)
    return db.execute(f"INSERT INTO {table} ({keys}) VALUES ({','.join('?' for _ in row)})", tuple(row.values())).lastrowid


def add_page(title, slug, language, parent=0, description=''):
    existing = db.execute('SELECT uid FROM pages WHERE slug=? AND sys_language_uid=? AND deleted=0', (slug, language)).fetchone()
    if existing:
        return existing[0]
    return copy_row('pages', 6 if language else 2, {
        'pid': 2, 'sorting': 128 if 'service' in slug or 'service' in title.lower() else 256,
        'title': title, 'nav_title': title, 'slug': slug, 'nav_hide': 1,
        'sys_language_uid': language, 'l10n_parent': parent, 'l10n_source': 0,
        'description': description, 'seo_title': title, 'og_title': title,
        'og_description': description, 'twitter_title': title, 'twitter_description': description,
        'hidden': 0, 'deleted': 0,
    })


def add_block(pid, language, kind, label, fields, sorting, parent=0, source=2):
    existing = db.execute('SELECT uid FROM tt_content WHERE pid=? AND sys_language_uid=? AND header=? AND deleted=0', (pid, language, label)).fetchone()
    if existing:
        return existing[0]
    values = {
        'pid': pid, 'sorting': sorting, 'colPos': 0, 'sys_language_uid': language,
        'l18n_parent': parent, 'CType': f'crispframe_{kind}', 'header': label,
        'hidden': 0, 'deleted': 0,
    }
    values.update({f'crispframe_{kind}_{k}': v for k, v in fields.items()})
    return copy_row('tt_content', source, values, prefix=f'crispframe_{kind}_')


def pair(pid, kind, label, en, de, sorting, source=2):
    defaults = {'sectionSpacing': 'default', 'sectionBackground': 'default', 'width': 'default'}
    if kind == 'intro':
        defaults.update({'linkLabel': '', 'link': ''})
    first = add_block(pid, 0, kind, f'Demo 1.3: {label}', {**defaults, **en}, sorting, source=source)
    second = add_block(pid, 1, kind, f'Demo 1.3: {label} DE', {**defaults, **de}, sorting, parent=first, source=source)
    if kind == 'intro':
        db.execute("UPDATE tt_content SET crispframe_intro_linkLabel='', crispframe_intro_link='' WHERE uid IN (?,?)", (first, second))
    return first, second


def add_file(filename):
    identifier = f'/user_upload/crispframe-demo/{filename}'
    source = Path('/app/packages/agency_demo/Resources/Public/Images') / filename
    destination = site_root / 'public/fileadmin' / identifier.lstrip('/')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.copyfile(source, destination)
    found = db.execute('SELECT uid FROM sys_file WHERE identifier=?', (identifier,)).fetchone()
    if found:
        return found[0]
    uid = copy_row('sys_file', 9, {
        'identifier': identifier, 'identifier_hash': hashlib.sha1(identifier.encode()).hexdigest(),
        'name': filename, 'sha1': hashlib.sha1(destination.read_bytes()).hexdigest(),
        'size': destination.stat().st_size, 'last_indexed': now,
        'creation_date': now, 'modification_date': now,
    })
    meta = db.execute('SELECT uid FROM sys_file_metadata WHERE file=9').fetchone()[0]
    copy_row('sys_file_metadata', meta, {'file': uid, 'title': '', 'description': '', 'alternative': ''})
    return uid


def attach_image(pid, en_uid, de_uid, file_uid, en_alt, de_alt):
    if db.execute("SELECT uid FROM sys_file_reference WHERE uid_foreign=? AND tablenames='tt_content' AND fieldname='crispframe_hero_image' AND deleted=0", (en_uid,)).fetchone():
        return
    base = copy_row('sys_file_reference', 5, {
        'pid': pid, 'uid_local': file_uid, 'uid_foreign': en_uid,
        'sys_language_uid': 0, 'l10n_parent': 0, 'alternative': en_alt,
    })
    copy_row('sys_file_reference', 6, {
        'pid': pid, 'uid_local': file_uid, 'uid_foreign': de_uid,
        'sys_language_uid': 1, 'l10n_parent': base, 'alternative': de_alt,
    })


def timeline_items(pid, en_uid, de_uid, english, german):
    table = 'crispframe_timeline_items'
    if db.execute(f'SELECT uid FROM {table} WHERE foreign_table_parent_uid=? AND deleted=0', (en_uid,)).fetchone():
        return
    for index, (en, de) in enumerate(zip(english, german)):
        common = {'pid': pid, 'sorting': (index + 1) * 128, 'tstamp': now, 'crdate': now,
                  'foreign_table_parent_uid': en_uid, 'sys_language_uid': 0,
                  'period': en[0], 'title': en[1], 'description': en[2]}
        uid = db.execute(f"INSERT INTO {table} ({','.join(common)}) VALUES ({','.join('?' for _ in common)})", tuple(common.values())).lastrowid
        common.update({'foreign_table_parent_uid': de_uid, 'sys_language_uid': 1, 'l10n_parent': uid,
                       'period': de[0], 'title': de[1], 'description': de[2]})
        db.execute(f"INSERT INTO {table} ({','.join(common)}) VALUES ({','.join('?' for _ in common)})", tuple(common.values()))


def attach_project_image(en_item, de_item, file_uid, en_alt, de_alt):
    if db.execute("SELECT uid FROM sys_file_reference WHERE tablenames='crispframe_projects_items' AND fieldname='image' AND uid_foreign=? AND deleted=0", (en_item,)).fetchone():
        return
    base = copy_row('sys_file_reference', 1, {
        'pid': 2, 'uid_local': file_uid, 'uid_foreign': en_item,
        'tablenames': 'crispframe_projects_items', 'fieldname': 'image',
        'sys_language_uid': 0, 'l10n_parent': 0, 'alternative': en_alt,
    })
    copy_row('sys_file_reference', 3, {
        'pid': 2, 'uid_local': file_uid, 'uid_foreign': de_item,
        'tablenames': 'crispframe_projects_items', 'fieldname': 'image',
        'sys_language_uid': 1, 'l10n_parent': base, 'alternative': de_alt,
    })
    db.execute('UPDATE crispframe_projects_items SET image=1 WHERE uid IN (?,?)', (en_item, de_item))


assert db.execute('SELECT title FROM pages WHERE uid=1').fetchone()[0] == 'Home'

# Correct only known unfinished demo placeholders. Existing customer records never enter this script.
db.execute("UPDATE tt_content SET header='Demo: Kontaktformular' WHERE uid=24 AND header LIKE '[Translate to Deutsch:]%'")
db.execute("UPDATE sys_file_reference SET alternative='Abstrakte blaue Illustration einer Benutzeroberfläche' WHERE uid=3 AND alternative LIKE '[Translate to Deutsch:]%'")
db.execute("UPDATE sys_file_reference SET alternative='Abstrakte grüne Illustration zur Zusammenarbeit' WHERE uid=4 AND alternative LIKE '[Translate to Deutsch:]%'")
db.execute("UPDATE tt_content SET hidden=0 WHERE uid=10 AND CType='crispframe_projects' AND header='Demo: project examples'")
db.execute("UPDATE crispframe_projects_items SET deleted=1 WHERE foreign_table_parent_uid=23 AND sys_language_uid=0 AND uid IN (7,8,9)")
db.execute("UPDATE crispframe_projects_items SET deleted=1 WHERE uid IN (3,6) AND foreign_table_parent_uid IN (10,23)")
db.execute("UPDATE tt_content SET crispframe_projects_items=2 WHERE uid IN (10,23) AND CType='crispframe_projects'")
db.execute("UPDATE tt_content SET crispframe_intro_text='Our projects bring content, interaction and technology into one coherent experience. Explore two examples of how clear decisions become useful digital services.' WHERE uid=4 AND crispframe_intro_text LIKE '%Add your case studies here%'")
db.execute("UPDATE tt_content SET crispframe_intro_text='Unsere Projekte verbinden Inhalt, Interaktion und Technik zu einem stimmigen Erlebnis. Entdecken Sie zwei Beispiele für nützliche digitale Angebote.' WHERE uid=17 AND crispframe_intro_text LIKE '%Ergänzen Sie hier Ihre eigenen Fallstudien%'")
db.execute("UPDATE tt_content SET crispframe_projects_headline='Selected case studies', crispframe_projects_lead='Explore the challenge, approach and outcome behind each example.' WHERE uid=10 AND crispframe_projects_headline='Example project formats'")
db.execute("UPDATE tt_content SET crispframe_projects_headline='Ausgewählte Projektberichte', crispframe_projects_lead='Erfahren Sie mehr über Aufgabe, Vorgehen und Ergebnis.' WHERE uid=23 AND crispframe_projects_headline='Beispielprojekte'")
for uid, old, title, category, description in [
    (1, 'Corporate website', 'A clearer public service', 'Public service', 'A bilingual service journey with a clear next step for every visitor.'),
    (2, 'Customer portal', 'A focused customer workspace', 'Digital product', 'A focused workspace for recurring customer tasks.'),
    (4, 'Unternehmenswebsite', 'Ein verständlicher öffentlicher Dienst', 'Öffentlicher Dienst', 'Ein zweisprachiger Service mit einem klaren nächsten Schritt.'),
    (5, 'Kundenportal', 'Ein klarer Kundenbereich', 'Digitales Produkt', 'Ein übersichtlicher Arbeitsbereich für wiederkehrende Aufgaben.'),
]:
    db.execute('UPDATE crispframe_projects_items SET title=?,category=?,description=? WHERE uid=? AND title=?',
               (title, category, description, uid, old))

for uid, description, title in [
    (1, 'Clear strategy, thoughtful design and dependable digital platforms for ambitious organizations.', 'Crispframe — Digital experiences with purpose'),
    (2, 'Explore selected website and product projects, from early discovery to useful outcomes.', 'Selected work — Crispframe'),
    (3, 'Contact the Crispframe team to discuss your next digital project.', 'Contact — Crispframe'),
    (4, 'Explore the flexible content blocks available to editors in the Crispframe theme.', 'Components — Crispframe'),
    (5, 'Klare Strategie, durchdachtes Design und verlässliche digitale Plattformen für Organisationen.', 'Crispframe — Digitale Erlebnisse mit Sinn'),
    (6, 'Entdecken Sie ausgewählte Website- und Produktprojekte von der ersten Idee bis zum Ergebnis.', 'Ausgewählte Projekte — Crispframe'),
    (7, 'Sprechen Sie mit dem Crispframe-Team über Ihr nächstes digitales Projekt.', 'Kontakt — Crispframe'),
    (8, 'Entdecken Sie die flexiblen Inhaltsbausteine des Crispframe-Themes.', 'Bausteine — Crispframe'),
]:
    db.execute("UPDATE pages SET description=?,seo_title=?,og_title=?,og_description=?,twitter_title=?,twitter_description=? WHERE uid=? AND (description IS NULL OR description='')", (description, title, title, description, title, description, uid))

cases = [
    ('service', 'A clearer public service', 'Ein verständlicher öffentlicher Dienst',
     '/work/clearer-public-service', '/work/clearer-public-service',
     'A bilingual public-service journey that helps people find the right next step.',
     'Ein zweisprachiger Service, der Menschen schnell zum nächsten Schritt führt.',
     'case-study-service.webp', 'Three colleagues review a service website journey at a studio table',
     'Drei Mitarbeitende besprechen einen digitalen Service an einem Studiotisch'),
    ('product', 'A focused customer workspace', 'Ein klarer Kundenbereich',
     '/work/customer-workspace', '/work/customer-workspace',
     'A practical digital workspace built around recurring customer tasks.',
     'Ein praktischer digitaler Arbeitsbereich für wiederkehrende Aufgaben.',
     'case-study-product.webp', 'Two colleagues review a product prototype on a tablet',
     'Zwei Mitarbeitende besprechen einen Produktprototyp auf einem Tablet'),
]

case_ids = []
for kind, en_title, de_title, en_slug, de_slug, en_desc, de_desc, filename, en_alt, de_alt in cases:
    en_page = add_page(en_title, en_slug, 0, description=en_desc)
    add_page(de_title, de_slug, 1, parent=en_page, description=de_desc)
    case_ids.append(en_page)
    hero_en, hero_de = pair(en_page, 'hero', f'{kind} case hero', {
        'eyebrow': 'Selected work · Case study', 'headline': en_title, 'subheadline': en_desc,
        'primaryLinkLabel': 'Discuss a project', 'primaryLink': 't3://page?uid=3',
        'secondaryLinkLabel': 'All work', 'secondaryLink': 't3://page?uid=2',
        'image': 1, 'imageAlt': en_alt, 'imagePosition': 'left' if kind == 'product' else 'right',
        'mediaCrop': 'square' if kind == 'product' else 'landscape', 'isHero': 1,
    }, {
        'eyebrow': 'Ausgewählte Arbeit · Projektbericht', 'headline': de_title, 'subheadline': de_desc,
        'primaryLinkLabel': 'Projekt besprechen', 'primaryLink': 't3://page?uid=3',
        'secondaryLinkLabel': 'Alle Projekte', 'secondaryLink': 't3://page?uid=2',
        'image': 1, 'imageAlt': de_alt, 'imagePosition': 'left' if kind == 'product' else 'right',
        'mediaCrop': 'square' if kind == 'product' else 'landscape', 'isHero': 1,
    }, 64, source=1)
    attach_image(en_page, hero_en, hero_de, add_file(filename), en_alt, de_alt)
    pair(en_page, 'intro', f'{kind} case challenge', {
        'headline': 'The challenge', 'lead': 'Make a complex journey feel simple.',
        'text': 'The team needed a clear structure that worked for people with different goals, devices and levels of confidence. We mapped the key tasks, reduced friction and shaped an editorial system that remains easy to maintain.',
        'width': 'narrow',
    }, {
        'headline': 'Die Aufgabe', 'lead': 'Einen komplexen Weg einfach gestalten.',
        'text': 'Das Team brauchte eine klare Struktur für Menschen mit unterschiedlichen Zielen, Geräten und Erfahrungen. Wir ordneten die wichtigsten Aufgaben, vereinfachten die Wege und entwickelten ein redaktionelles System, das leicht zu pflegen bleibt.',
        'width': 'narrow',
    }, 192)
    steps_en = [
        ('01 · Discover', 'Understand the real task', 'Talk with editors and users; map the decisions people need to make.'),
        ('02 · Shape', 'Make the journey clear', 'Prototype the structure, content and visual patterns before building.'),
        ('03 · Deliver', 'Create room to improve', 'Publish flexible pages and give the team a system it can maintain.'),
    ]
    steps_de = [
        ('01 · Verstehen', 'Die Aufgabe erkennen', 'Mit Redaktion und Nutzenden sprechen und wichtige Entscheidungen erfassen.'),
        ('02 · Gestalten', 'Den Weg klären', 'Struktur, Inhalte und visuelle Muster vor der Umsetzung erproben.'),
        ('03 · Umsetzen', 'Verbesserung ermöglichen', 'Flexible Seiten veröffentlichen und ein pflegbares System übergeben.'),
    ]
    timeline_en, timeline_de = pair(en_page, 'timeline', f'{kind} case process', {
        'headline': 'From question to useful experience', 'lead': 'Three connected steps shaped the work.',
        'items': 3, 'layout': 'cards',
    }, {
        'headline': 'Von der Frage zum nützlichen Erlebnis', 'lead': 'Drei zusammenhängende Schritte prägten die Arbeit.',
        'items': 3, 'layout': 'cards',
    }, 256)
    timeline_items(en_page, timeline_en, timeline_de, steps_en, steps_de)
    pair(en_page, 'intro', f'{kind} case outcome', {
        'headline': 'The outcome', 'lead': 'A useful foundation for what comes next.',
        'text': 'The finished experience pairs a strong visual identity with accessible patterns and flexible content. Editors can publish new material without breaking the layout, and the organization can improve each journey using real feedback.',
        'width': 'narrow', 'sectionBackground': 'subtle',
    }, {
        'headline': 'Das Ergebnis', 'lead': 'Eine gute Grundlage für die nächsten Schritte.',
        'text': 'Das fertige Angebot verbindet eine klare visuelle Identität mit zugänglichen Mustern und flexiblen Inhalten. Redaktionsteams können neue Inhalte sicher veröffentlichen und die Organisation kann jeden Weg anhand echter Rückmeldungen verbessern.',
        'width': 'narrow', 'sectionBackground': 'subtle',
    }, 320)
    native_en = 'A closer look' if kind == 'service' else 'Designed for repeat visits'
    native_de = 'Ein genauerer Blick' if kind == 'service' else 'Für wiederkehrende Besuche gestaltet'
    editorial_en = ('The clearest service journeys begin with plain language. We grouped information around the questions people actually ask and gave each page an obvious next step.'
                    if kind == 'service' else
                    'Customers return to a product workspace to get something done. We brought frequent tasks forward and kept secondary detail close at hand without crowding the main view.')
    editorial_de = ('Die verständlichsten Servicewege beginnen mit klarer Sprache. Wir ordneten Informationen nach den Fragen der Menschen und gaben jeder Seite einen eindeutigen nächsten Schritt.'
                    if kind == 'service' else
                    'Kundinnen und Kunden kommen in einen Arbeitsbereich zurück, um Aufgaben zu erledigen. Wir stellten häufige Schritte nach vorn und hielten weitere Details leicht erreichbar.')
    first = db.execute('SELECT uid FROM tt_content WHERE pid=? AND header IN (?,?) AND deleted=0',
                       (en_page, native_en, f'Demo 1.3: {kind} editorial notes')).fetchone()
    if not first:
        first_uid = copy_row('tt_content', 2, {
            'pid': en_page, 'sorting': 384, 'CType': 'text', 'header': native_en,
            'sys_language_uid': 0, 'l18n_parent': 0,
            'bodytext': f'<p>{editorial_en}</p>',
        }, prefix='__no_crispframe__')
        copy_row('tt_content', 2, {
            'pid': en_page, 'sorting': 384, 'CType': 'text', 'header': native_de,
            'sys_language_uid': 1, 'l18n_parent': first_uid,
            'bodytext': f'<p>{editorial_de}</p>',
        }, prefix='__no_crispframe__')
    else:
        db.execute('UPDATE tt_content SET header=? WHERE uid=?', (native_en, first[0]))
        db.execute('UPDATE tt_content SET header=? WHERE l18n_parent=?', (native_de, first[0]))
        db.execute("UPDATE tt_content SET bodytext=? WHERE uid=? AND bodytext LIKE '%regular TYPO3 text elements%'", (f'<p>{editorial_en}</p>', first[0]))
        db.execute("UPDATE tt_content SET bodytext=? WHERE l18n_parent=? AND bodytext LIKE '%normale TYPO3-Textelemente%'", (f'<p>{editorial_de}</p>', first[0]))
    pair(en_page, 'cta', f'{kind} case invitation', {
        'headline': 'Have a similar challenge?', 'text': 'Tell us what you are planning and we will find a useful first step together.',
        'primaryLinkLabel': 'Get in touch', 'primaryLink': 't3://page?uid=3',
        'sectionBackground': 'brand',
    }, {
        'headline': 'Eine ähnliche Aufgabe?', 'text': 'Erzählen Sie uns von Ihren Plänen. Gemeinsam finden wir einen sinnvollen ersten Schritt.',
        'primaryLinkLabel': 'Kontakt aufnehmen', 'primaryLink': 't3://page?uid=3',
        'sectionBackground': 'brand',
    }, 448)

for uid, target, label in [(1, case_ids[0], 'Read case study'), (2, case_ids[1], 'Read case study'),
                           (4, case_ids[0], 'Projekt ansehen'), (5, case_ids[1], 'Projekt ansehen')]:
    db.execute('UPDATE crispframe_projects_items SET link=?, linkLabel=? WHERE uid=? AND (link IS NULL OR link="")',
               (f't3://page?uid={target}', label, uid))
for en_item, de_item, filename, alt_en, alt_de in [
    (1, 4, 'case-study-service.webp', cases[0][8], cases[0][9]),
    (2, 5, 'case-study-product.webp', cases[1][8], cases[1][9]),
]:
    attach_project_image(en_item, de_item, add_file(filename), alt_en, alt_de)

# Page links resolve against the active language and avoid hard-coded English paths.
for table in ('tt_content', 'crispframe_projects_items', 'crispframe_services_items', 'crispframe_featuregrid_items'):
    columns = [c[1] for c in db.execute(f'PRAGMA table_info({table})')]
    for column in columns:
        if column.endswith('Link') or column == 'link':
            db.execute(f'UPDATE {table} SET {column}=? WHERE {column}=?', ('t3://page?uid=3', '/contact'))
            db.execute(f'UPDATE {table} SET {column}=? WHERE {column}=?', ('t3://page?uid=2', '/work'))

db.commit()
print('Added bilingual case studies and localized demo links and metadata.')
