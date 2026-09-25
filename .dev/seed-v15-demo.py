"""Maintainer-only additive 1.5 demo authoring. Never run on a customer site."""

import os
import sqlite3
import subprocess
import time
from pathlib import Path

root = Path(os.environ.get('CRISPFRAME_SITE_ROOT', '/app'))
db_path = subprocess.check_output([
    'php', '-r', "$s=require $argv[1]; echo $s['DB']['Connections']['Default']['path'];",
    str(root / 'config/system/settings.php'),
], text=True).strip()
db = sqlite3.connect(db_path)
db.row_factory = sqlite3.Row
now = int(time.time())


def clone(table, uid, changes, prefix=None):
    record = dict(db.execute(f'SELECT * FROM {table} WHERE uid=?', (uid,)).fetchone())
    record.pop('uid')
    if prefix and table == 'tt_content':
        record = {key: value for key, value in record.items()
                  if not key.startswith('crispframe_') or key.startswith(prefix)}
    record.update(changes)
    for key in ('tstamp', 'crdate'):
        if key in record:
            record[key] = now
    columns = ','.join(record)
    placeholders = ','.join('?' for _ in record)
    return db.execute(f'INSERT INTO {table} ({columns}) VALUES ({placeholders})', tuple(record.values())).lastrowid


base_page_en = db.execute("SELECT uid FROM pages WHERE slug='/work/clearer-public-service' AND sys_language_uid=0 AND deleted=0").fetchone()[0]
base_page_de = db.execute("SELECT uid FROM pages WHERE slug='/work/clearer-public-service' AND sys_language_uid=1 AND deleted=0").fetchone()[0]
base_content = db.execute("SELECT uid FROM tt_content WHERE sys_language_uid=0 AND deleted=0 ORDER BY uid LIMIT 1").fetchone()[0]


def page(title, slug, parent, language=0, translation=0, sorting=512, abstract='', in_menu=True):
    found = db.execute('SELECT uid FROM pages WHERE slug=? AND sys_language_uid=? AND deleted=0',
                       (slug, language)).fetchone()
    if found:
        return found[0]
    return clone('pages', base_page_de if language else base_page_en, {
        'pid': parent, 'sorting': sorting, 'title': title, 'nav_title': title,
        'slug': slug, 'sys_language_uid': language, 'l10n_parent': translation,
        'l10n_source': 0, 'nav_hide': 0 if in_menu else 1, 'hidden': 0, 'deleted': 0,
        'backend_layout': '', 'backend_layout_next_level': '',
        'abstract': abstract, 'description': abstract, 'seo_title': title,
        'og_title': title, 'og_description': abstract,
        'twitter_title': title, 'twitter_description': abstract, 'media': 0,
    })


def block(pid, language, kind, marker, fields, sorting, translation=0):
    found = db.execute('SELECT uid FROM tt_content WHERE pid=? AND sys_language_uid=? AND header=? AND deleted=0',
                       (pid, language, marker)).fetchone()
    if found:
        return found[0]
    typename = kind.replace('-', '')
    fields = {'sectionSpacing': 'default', 'sectionBackground': 'default', 'width': 'default', **fields}
    values = {
        'pid': pid, 'sorting': sorting, 'colPos': 0,
        'sys_language_uid': language, 'l18n_parent': translation,
        'CType': f'crispframe_{typename}', 'header': marker,
        'hidden': 0, 'deleted': 0,
    }
    values.update({f'crispframe_{typename}_{key}': value for key, value in fields.items()})
    return clone('tt_content', base_content, values, prefix=f'crispframe_{typename}_')


def block_pair(pid, kind, name, english, german, sorting):
    en = block(pid, 0, kind, f'Demo 1.5: {name}', english, sorting)
    de = block(pid, 1, kind, f'Demo 1.5: {name} DE', german, sorting, translation=en)
    return en, de


def children(table, pid, en_parent, de_parent, english, german):
    if db.execute(f'SELECT uid FROM {table} WHERE foreign_table_parent_uid=? AND deleted=0',
                  (en_parent,)).fetchone():
        return
    for position, (en, de) in enumerate(zip(english, german), 1):
        shared = {'pid': pid, 'sorting': position * 128, 'tstamp': now, 'crdate': now,
                  'deleted': 0, 'hidden': 0, 'foreign_table_parent_uid': en_parent,
                  'sys_language_uid': 0, **en}
        names = ','.join(shared)
        placeholders = ','.join('?' for _ in shared)
        en_uid = db.execute(f'INSERT INTO {table} ({names}) VALUES ({placeholders})', tuple(shared.values())).lastrowid
        localized = {**shared, 'foreign_table_parent_uid': de_parent,
                     'sys_language_uid': 1, 'l10n_parent': en_uid, **de}
        names = ','.join(localized)
        placeholders = ','.join('?' for _ in localized)
        db.execute(f'INSERT INTO {table} ({names}) VALUES ({placeholders})', tuple(localized.values()))


def hero_pair(pid, headline, headline_de, eyebrow, eyebrow_de, sorting=64, layout='minimal'):
    return block_pair(pid, 'hero', headline.lower(), {
        'eyebrow': eyebrow, 'headline': headline, 'subheadline': '', 'isHero': 1,
        'image': 0, 'imageAlt': '', 'imagePosition': 'right', 'mediaCrop': 'landscape',
        'layout': layout, 'height': 'small', 'primaryLink': '', 'primaryLinkLabel': '',
        'secondaryLink': '', 'secondaryLinkLabel': '', 'sectionBackground': 'subtle',
    }, {
        'eyebrow': eyebrow_de, 'headline': headline_de, 'subheadline': '', 'isHero': 1,
        'image': 0, 'imageAlt': '', 'imagePosition': 'right', 'mediaCrop': 'landscape',
        'layout': layout, 'height': 'small', 'primaryLink': '', 'primaryLinkLabel': '',
        'secondaryLink': '', 'secondaryLinkLabel': '', 'sectionBackground': 'subtle',
    }, sorting)


services = db.execute("SELECT uid FROM pages WHERE slug='/services' AND sys_language_uid=0 AND deleted=0").fetchone()[0]
about = db.execute("SELECT uid FROM pages WHERE slug='/about' AND sys_language_uid=0 AND deleted=0").fetchone()[0]

# Make the block library discoverable in the demo's primary mega navigation.
components = db.execute("SELECT uid FROM pages WHERE slug='/components' AND sys_language_uid=0 AND deleted=0").fetchone()
if components:
    db.execute("UPDATE pages SET title='Showcase', nav_title='Showcase', nav_hide=0 WHERE uid=?", (components[0],))
    components_de = db.execute("SELECT uid FROM pages WHERE l10n_parent=? AND sys_language_uid=1 AND deleted=0", (components[0],)).fetchone()
    if components_de:
        db.execute("UPDATE pages SET title='Bausteine', nav_title='Bausteine', nav_hide=0 WHERE uid=?", (components_de[0],))

# Keep an accidental root-level test page out of the public demo navigation.
db.execute("UPDATE pages SET nav_hide=1 WHERE slug='/asdasd' AND sys_language_uid=0 AND deleted=0")

service_pages = [
    ('Strategy and discovery', 'Strategie und Analyse', '/services/strategy', '/leistungen/strategie'),
    ('Experience design', 'Experience Design', '/services/experience-design', '/leistungen/experience-design'),
    ('TYPO3 platforms', 'TYPO3-Plattformen', '/services/typo3-platforms', '/leistungen/typo3-plattformen'),
    ('Continuous improvement', 'Laufende Weiterentwicklung', '/services/improvement', '/leistungen/weiterentwicklung'),
]
for index, (title, title_de, slug, slug_de) in enumerate(service_pages, 1):
    child = page(title, slug, services, sorting=index * 128,
                 abstract=f'Learn how {title.lower()} supports a successful digital service.')
    page(title_de, slug_de, services, 1, child, sorting=index * 128,
         abstract=f'Erfahren Sie mehr über {title_de.lower()} für erfolgreiche digitale Angebote.')
    hero_pair(child, title, title_de, 'Service', 'Leistung')

locations = page('Locations', '/about/locations', about, sorting=128,
                 abstract='Meet the teams supporting clients from Berlin and Hamburg.')
locations_de = page('Standorte', '/ueber-uns/standorte', about, 1, locations, sorting=128,
                    abstract='Lernen Sie unsere Teams in Berlin und Hamburg kennen.')
hero_pair(locations, 'Teams close to your work', 'Teams in Ihrer Nähe', 'Locations', 'Standorte', layout='centered')
locations_en, locations_de_block = block_pair(locations, 'locations', 'office locations', {
    'headline': 'Our offices', 'lead': 'Work with the same focused team from either location.',
    'items': 2, 'sectionBackground': 'default',
}, {
    'headline': 'Unsere Standorte', 'lead': 'An beiden Standorten arbeitet dasselbe fokussierte Team für Sie.',
    'items': 2, 'sectionBackground': 'default',
}, 128)
children('crispframe_locations_items', locations, locations_en, locations_de_block, [
    {'name': 'Berlin', 'address': 'Torstraße 140\n10119 Berlin', 'phone': '+49 30 000000',
     'email': 'berlin@crispframe.example', 'hours': 'Monday–Friday\n09:00–18:00 CET',
     'image': 0, 'mapLabel': 'Open map', 'mapLink': 'https://www.openstreetmap.org/search?query=Berlin'},
    {'name': 'Hamburg', 'address': 'Shanghaiallee 12\n20457 Hamburg', 'phone': '+49 40 000000',
     'email': 'hamburg@crispframe.example', 'hours': 'Monday–Friday\n09:00–18:00 CET',
     'image': 0, 'mapLabel': 'Open map', 'mapLink': 'https://www.openstreetmap.org/search?query=Hamburg'},
], [
    {'name': 'Berlin', 'address': 'Torstraße 140\n10119 Berlin', 'phone': '+49 30 000000',
     'email': 'berlin@crispframe.example', 'hours': 'Montag–Freitag\n09:00–18:00 Uhr',
     'image': 0, 'mapLabel': 'Karte öffnen', 'mapLink': 'https://www.openstreetmap.org/search?query=Berlin'},
    {'name': 'Hamburg', 'address': 'Shanghaiallee 12\n20457 Hamburg', 'phone': '+49 40 000000',
     'email': 'hamburg@crispframe.example', 'hours': 'Montag–Freitag\n09:00–18:00 Uhr',
     'image': 0, 'mapLabel': 'Karte öffnen', 'mapLink': 'https://www.openstreetmap.org/search?query=Hamburg'},
])
block_pair(locations, 'callout', 'location note', {
    'appearance': 'information', 'headline': 'Meetings by appointment',
    'body': '<p>Choose the office that is easiest for you, or meet us remotely.</p>',
    'linkLabel': 'Start a conversation', 'link': 't3://page?uid=3', 'width': 'default',
}, {
    'appearance': 'information', 'headline': 'Termine nach Vereinbarung',
    'body': '<p>Wählen Sie den passenden Standort oder treffen Sie uns digital.</p>',
    'linkLabel': 'Gespräch beginnen', 'link': 't3://page?uid=3', 'width': 'default',
}, 256)

inquiry = page('Request a project', '/project-inquiry', 1, sorting=768,
               abstract='Share the goals, timing and scale of your next digital project.', in_menu=False)
inquiry_de = page('Projekt anfragen', '/projektanfrage', 1, 1, inquiry, sorting=768,
                  abstract='Beschreiben Sie Ziele, Zeitrahmen und Umfang Ihres nächsten Digitalprojekts.', in_menu=False)
hero_pair(inquiry, 'Tell us what you want to improve', 'Was möchten Sie verbessern?',
          'Project inquiry', 'Projektanfrage', layout='minimal')
form_base_en = db.execute("SELECT uid FROM tt_content WHERE CType='form_formframework' AND sys_language_uid=0 AND deleted=0 ORDER BY uid LIMIT 1").fetchone()[0]
form_base_de = db.execute("SELECT uid FROM tt_content WHERE CType='form_formframework' AND sys_language_uid=1 AND deleted=0 ORDER BY uid LIMIT 1").fetchone()[0]
form_xml = '<?xml version="1.0" encoding="utf-8"?><T3FlexForms><data><sheet index="sDEF"><language index="lDEF"><field index="settings.persistenceIdentifier"><value index="vDEF">EXT:agency_theme/Resources/Private/Forms/ProjectInquiry.form.yaml</value></field></language></sheet></data></T3FlexForms>'
existing_form = db.execute("SELECT uid FROM tt_content WHERE pid=? AND header='Demo 1.5: project inquiry form' AND deleted=0", (inquiry,)).fetchone()
if not existing_form:
    form_en = clone('tt_content', form_base_en, {'pid': inquiry, 'sorting': 128, 'header': 'Demo 1.5: project inquiry form', 'pi_flexform': form_xml})
    clone('tt_content', form_base_de, {'pid': inquiry, 'sorting': 128, 'header': 'Demo 1.5: Projektanfrage',
                                      'pi_flexform': form_xml, 'l18n_parent': form_en})

section_en, section_de = block_pair(services, 'section-navigation', 'services page navigation', {
    'headline': 'On this page', 'layout': 'inline', 'sticky': 0, 'sectionSpacing': 'small',
    'sectionBackground': 'default', 'width': 'default',
}, {
    'headline': 'Auf dieser Seite', 'layout': 'inline', 'sticky': 0, 'sectionSpacing': 'small',
    'sectionBackground': 'default', 'width': 'default',
}, 32)
db.execute("UPDATE tt_content SET sectionIndex=1 WHERE pid=? AND CType LIKE 'crispframe_%' AND uid NOT IN (?,?) AND deleted=0", (services, section_en, section_de))

db.commit()
print('Added the bilingual 1.5 Locations and Project Inquiry pages, service tree, and three new block examples.')
