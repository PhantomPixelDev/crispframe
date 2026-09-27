"""Additive maintainer seed for the 1.6 bilingual style showcase.

Run only after a backup and agency_theme schema setup. Existing records are
never updated; repeating the script leaves already-created examples alone.
"""

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


def row(table, condition, args=()):
    result = db.execute(f'SELECT * FROM {table} WHERE {condition} LIMIT 1', args).fetchone()
    if result is None:
        raise RuntimeError(f'Missing {table}: {condition} {args}')
    return result


def clone(table, original, changes):
    values = dict(original)
    values.pop('uid', None)
    values.update(changes)
    for key in ('tstamp', 'crdate'):
        if key in values:
            values[key] = now
    names = ','.join(values)
    placeholders = ','.join('?' for _ in values)
    return db.execute(f'INSERT INTO {table} ({names}) VALUES ({placeholders})', tuple(values.values())).lastrowid


def file_references(table, original_uid, new_uid, pid, language, parent_refs=None):
    refs = db.execute('SELECT * FROM sys_file_reference WHERE tablenames=? AND uid_foreign=? AND deleted=0 ORDER BY sorting_foreign,uid',
                      (table, original_uid)).fetchall()
    new_refs = []
    for index, ref in enumerate(refs):
        new_refs.append(clone('sys_file_reference', ref, {
            'pid': pid, 'uid_foreign': new_uid, 'sys_language_uid': language,
            'l10n_parent': parent_refs[index] if parent_refs and index < len(parent_refs) else 0,
            'l10n_source': 0, 'deleted': 0,
        }))
    return new_refs


def copy_items(table, source_en, source_de, target_en, target_de, pid):
    originals = db.execute(f'SELECT * FROM {table} WHERE foreign_table_parent_uid=? AND sys_language_uid=0 AND deleted=0 ORDER BY sorting,uid',
                           (source_en,)).fetchall()
    for original in originals:
        item_en = clone(table, original, {
            'pid': pid, 'foreign_table_parent_uid': target_en,
            'sys_language_uid': 0, 'l10n_parent': 0, 'l10n_source': 0,
        })
        en_refs = file_references(table, original['uid'], item_en, pid, 0)
        translation = db.execute(f'SELECT * FROM {table} WHERE foreign_table_parent_uid=? AND l10n_parent=? AND sys_language_uid=1 AND deleted=0 LIMIT 1',
                                 (source_de, original['uid'])).fetchone()
        if translation is None:
            translation = original
        item_de = clone(table, translation, {
            'pid': pid, 'foreign_table_parent_uid': target_de,
            'sys_language_uid': 1, 'l10n_parent': item_en, 'l10n_source': 0,
        })
        file_references(table, translation['uid'], item_de, pid, 1, en_refs)


components = row('pages', "slug='/components' AND sys_language_uid=0 AND deleted=0")
components_de = row('pages', 'l10n_parent=? AND sys_language_uid=1 AND deleted=0', (components['uid'],))
existing = db.execute("SELECT uid FROM pages WHERE slug='/components/style-variants' AND sys_language_uid=0 AND deleted=0").fetchone()
if existing:
    print('The 1.6 style showcase already exists; no existing records were changed.')
    db.close()
    raise SystemExit(0)

with db:
    page_en = clone('pages', components, {
        'pid': components['uid'], 'sorting': 2048, 'title': 'Style variants',
        'nav_title': 'Style variants', 'slug': '/components/style-variants',
        'nav_hide': 1, 'sys_language_uid': 0, 'l10n_parent': 0,
        'abstract': 'Compare the restrained presentation choices for six core Crispframe blocks.',
        'description': 'Compare the restrained presentation choices for six core Crispframe blocks.',
        'seo_title': 'Style variants', 'og_title': 'Style variants',
        'og_description': 'Compare the presentation choices for core Crispframe blocks.',
        'twitter_title': 'Style variants', 'twitter_description': 'Compare Crispframe style variants.',
        'media': 0, 'hidden': 0, 'deleted': 0,
    })
    clone('pages', components_de, {
        'pid': components['uid'], 'sorting': 2048, 'title': 'Stilvarianten',
        'nav_title': 'Stilvarianten', 'slug': '/components/stilvarianten',
        'nav_hide': 1, 'sys_language_uid': 1, 'l10n_parent': page_en,
        'abstract': 'Vergleichen Sie die zurückhaltenden Darstellungen der wichtigsten Crispframe-Bausteine.',
        'description': 'Vergleichen Sie die zurückhaltenden Darstellungen der wichtigsten Crispframe-Bausteine.',
        'seo_title': 'Stilvarianten', 'og_title': 'Stilvarianten',
        'og_description': 'Darstellungsvarianten der wichtigsten Crispframe-Bausteine.',
        'twitter_title': 'Stilvarianten', 'twitter_description': 'Crispframe-Stilvarianten im Vergleich.',
        'media': 0, 'hidden': 0, 'deleted': 0,
    })

    def add(kind, variant_field, variant, title_en, title_de, lead_en, lead_de, sorting, extra=None):
        typename = kind.replace('-', '')
        ctype = f'crispframe_{typename}'
        source_en = row('tt_content', 'CType=? AND sys_language_uid=0 AND deleted=0 AND hidden=0', (ctype,))
        source_de = db.execute('SELECT * FROM tt_content WHERE l18n_parent=? AND sys_language_uid=1 AND deleted=0 LIMIT 1',
                               (source_en['uid'],)).fetchone() or source_en
        field = f'crispframe_{typename}_'
        common = {'pid': page_en, 'sorting': sorting, 'colPos': 0,
                  'hidden': 0, 'deleted': 0, 'sectionIndex': 0}
        en_values = {**common, 'sys_language_uid': 0, 'l18n_parent': 0,
                     'header': f'Demo 1.6: {kind} {variant}',
                     field + variant_field: variant,
                     field + 'headline': title_en}
        de_values = {**common, 'sys_language_uid': 1,
                     'header': f'Demo 1.6: {kind} {variant} DE',
                     field + variant_field: variant,
                     field + 'headline': title_de}
        if kind == 'hero':
            en_values.update({field + 'subheadline': lead_en, field + 'isHero': 1 if sorting == 64 else 0,
                              field + 'image': 0, field + 'imageAlt': '', field + 'layout': 'minimal',
                              field + 'height': 'small', field + 'sectionBackground': 'subtle',
                              field + 'primaryLink': '', field + 'secondaryLink': ''})
            de_values.update({field + 'subheadline': lead_de, field + 'isHero': 1 if sorting == 64 else 0,
                              field + 'image': 0, field + 'imageAlt': '', field + 'layout': 'minimal',
                              field + 'height': 'small', field + 'sectionBackground': 'subtle',
                              field + 'primaryLink': '', field + 'secondaryLink': ''})
        elif kind == 'cta':
            en_values.update({field + 'text': lead_en, field + 'primaryLinkLabel': 'Start a conversation',
                              field + 'primaryLink': 't3://page?uid=3', field + 'secondaryLink': '',
                              field + 'sectionBackground': 'subtle'})
            de_values.update({field + 'text': lead_de, field + 'primaryLinkLabel': 'Kontakt aufnehmen',
                              field + 'primaryLink': 't3://page?uid=3', field + 'secondaryLink': '',
                              field + 'sectionBackground': 'subtle'})
        else:
            en_values[field + 'lead'] = lead_en
            de_values[field + 'lead'] = lead_de
        if extra:
            for key, value in extra.items():
                en_values[field + key] = value
                de_values[field + key] = value
        content_en = clone('tt_content', source_en, en_values)
        de_values['l18n_parent'] = content_en
        content_de = clone('tt_content', source_de, de_values)
        if kind in ('services', 'feature-grid', 'projects', 'testimonials'):
            copy_items(f'crispframe_{typename}_items', source_en['uid'], source_de['uid'], content_en, content_de, page_en)
        return content_en, content_de

    add('hero', 'headlineMeasure', 'narrow', 'A sharper point of view', 'Ein klarer Blickwinkel',
        'Narrow headlines give a short thought more presence.', 'Schmale Überschriften geben kurzen Gedanken mehr Raum.', 64)
    add('hero', 'headlineMeasure', 'standard', 'The familiar balanced headline', 'Die vertraute ausgewogene Überschrift',
        'The standard measure keeps the established layout.', 'Die Standardbreite erhält das bisherige Layout.', 128)
    add('hero', 'headlineMeasure', 'wide', 'An expansive headline for a longer editorial thought',
        'Eine breite Überschrift für einen längeren redaktionellen Gedanken',
        'Use the wider measure for a sentence that needs a calmer rhythm.',
        'Die breite Variante gibt längeren Aussagen einen ruhigeren Rhythmus.', 192)
    add('services', 'cardStyle', 'cards', 'Services in cards', 'Leistungen als Karten',
        'Use cards when each offer needs a clear boundary.', 'Karten trennen eigenständige Angebote deutlich.', 256)
    add('services', 'cardStyle', 'open', 'Services in open columns', 'Leistungen in offenen Spalten',
        'Use open columns for a lighter overview of related services.',
        'Offene Spalten eignen sich für einen ruhigen Überblick verwandter Leistungen.', 320)
    add('feature-grid', 'featureStyle', 'cards', 'Features in cards', 'Merkmale als Karten',
        'Use cards for distinct benefits.', 'Karten betonen einzelne Vorteile.', 384)
    add('feature-grid', 'featureStyle', 'open', 'Features in open columns', 'Merkmale in offenen Spalten',
        'Use open columns when the icons and words should lead.',
        'Offene Spalten lassen Symbolen und Text mehr Raum.', 448)
    add('projects', 'projectStyle', 'cards', 'Projects in cards', 'Projekte als Karten',
        'Use cards for a concise portfolio grid.', 'Karten eignen sich für eine kompakte Projektübersicht.', 512)
    add('projects', 'projectStyle', 'rows', 'Projects as editorial rows', 'Projekte als redaktionelle Reihen',
        'Use rows when each case study deserves more context.',
        'Reihen geben jeder Fallstudie mehr Platz für Kontext.', 576)
    add('testimonials', 'quoteStyle', 'cards', 'Quotes in cards', 'Zitate als Karten',
        'Use cards for a compact set of testimonials.', 'Karten bündeln mehrere Kundenstimmen kompakt.', 640)
    add('testimonials', 'quoteStyle', 'open', 'Open quotes', 'Offene Zitate',
        'Use the divider when the voices should feel part of the editorial flow.',
        'Die Trennlinie fügt Kundenstimmen ruhig in den Lesefluss ein.', 704)
    add('cta', 'ctaStyle', 'panel', 'A contained next step', 'Ein umrahmter nächster Schritt',
        'Use a panel to give a clear conversion moment.', 'Die Fläche markiert einen klaren nächsten Schritt.', 768)
    add('cta', 'ctaStyle', 'open', 'A quieter invitation', 'Eine ruhigere Einladung',
        'Use the open section when the invitation should flow with the page.',
        'Der offene Abschnitt fügt die Einladung in die Seite ein.', 832)

    # Append one translated resource-list record to Components. No existing record changes.
    for language, label, summary in (
        (0, 'Style variants', 'Compare the new visual choices.'),
        (1, 'Stilvarianten', 'Neue Darstellungen im Vergleich.'),
    ):
        source = db.execute('SELECT * FROM tt_content WHERE CType=? AND sys_language_uid=? AND deleted=0 LIMIT 1',
                            ('crispframe_resourcelist', language)).fetchone()
        if source is None:
            source = row('tt_content', 'CType=? AND sys_language_uid=0 AND deleted=0',
                         ('crispframe_resourcelist',))
        marker = f'Demo 1.6: style variants link {language}'
        content = clone('tt_content', source, {
            'pid': components['uid'], 'sorting': 8192, 'colPos': 0,
            'header': marker, 'sys_language_uid': language,
            'l18n_parent': link_en if language else 0,
            'crispframe_resourcelist_headline': label,
            'crispframe_resourcelist_lead': summary,
            'crispframe_resourcelist_items': 1,
            'hidden': 0, 'deleted': 0,
        })
        if not language:
            link_en = content
        item_source = row('crispframe_resourcelist_items', 'foreign_table_parent_uid=? AND deleted=0', (source['uid'],))
        item_uid = clone('crispframe_resourcelist_items', item_source, {
            'pid': components['uid'], 'foreign_table_parent_uid': content,
            'sys_language_uid': language, 'l10n_parent': link_item_en if language else 0,
            'label': label, 'description': summary,
            'link': f't3://page?uid={page_en}', 'deleted': 0, 'hidden': 0,
        })
        if not language:
            link_item_en = item_uid

print('Added the bilingual 1.6 style showcase and Components links without updating existing records.')
