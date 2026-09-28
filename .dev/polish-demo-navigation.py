"""Add editable jump links to the maintainer demo; never replace existing content.

Defaults to a dry run. Pass --apply only on the development fixture or a fresh
demo export copy. An SQLite backup is created before the first insertion.
"""
import argparse
import os
import sqlite3
import subprocess
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
root = Path(os.environ.get('CRISPFRAME_SITE_ROOT', '/app'))
db_path = subprocess.check_output(['php', '-r', "$s=require $argv[1]; echo $s['DB']['Connections']['Default']['path'];", str(root / 'config/system/settings.php')], text=True).strip()
db = sqlite3.connect(db_path)
db.row_factory = sqlite3.Row
now = int(time.time())
plans = [
    ('/components', [('pricing', 'Plans and pricing', 'Pakete und Preise'), ('video', 'Video', 'Video'), ('gallery', 'Image gallery', 'Bildergalerie'), ('testimonials', 'Client voices', 'Kundenstimmen'), ('comparison', 'Compare options', 'Optionen vergleichen'), ('timeline', 'Timeline', 'Zeitstrahl')]),
    ('/components/style-variants', [('hero', 'Hero headings', 'Hero-Überschriften'), ('services', 'Service layouts', 'Leistungsdarstellung'), ('featuregrid', 'Feature layouts', 'Merkmalsdarstellung'), ('projects', 'Project layouts', 'Projektdarstellung'), ('testimonials', 'Quote layouts', 'Zitatdarstellung'), ('cta', 'Calls to action', 'Handlungsaufforderungen')]),
]
pending = []
for slug, choices in plans:
    page = db.execute('SELECT uid FROM pages WHERE slug=? AND sys_language_uid=0 AND deleted=0', (slug,)).fetchone()
    if page is None:
        raise RuntimeError(f'Missing demo page: {slug}')
    parent = 0
    for language in (0, 1):
        marker = f'Demo polish: showcase navigation {language}'
        existing = db.execute('SELECT uid FROM tt_content WHERE pid=? AND header=? AND sys_language_uid=? AND deleted=0', (page['uid'], marker, language)).fetchone()
        if existing:
            continue
        links = []
        for kind, en, de in choices:
            target = db.execute('SELECT uid FROM tt_content WHERE pid=? AND CType=? AND sys_language_uid=? AND deleted=0 AND hidden=0 ORDER BY sorting,uid LIMIT 1', (page['uid'], 'crispframe_' + kind, language)).fetchone()
            if target:
                links.append((en if language == 0 else de, '#c' + str(target['uid'])))
        if not links:
            raise RuntimeError(f'No visible demo targets: {slug}/{language}')
        pending.append((page['uid'], language, marker, 96 if 'style-variants' in slug else 1, links))
        print(f'{slug} language {language}: add {len(links)} editable jump links')
if not args.apply or not pending:
    print('No writes.' if not args.apply else 'Already present; no changes.')
    raise SystemExit(0)
backup_dir = root / 'var/backups'
backup_dir.mkdir(parents=True, exist_ok=True)
with sqlite3.connect(backup_dir / f'before-showcase-navigation-{now}.sqlite') as backup:
    db.backup(backup)

def insert(table, values):
    return db.execute(f'INSERT INTO {table} ({",".join(values)}) VALUES ({",".join("?" for _ in values)})', tuple(values.values())).lastrowid

with db:
    parents = {}
    for pid, language, marker, sorting, links in pending:
        parent = parents.get(pid, 0)
        if language and not parent:
            parent = db.execute('SELECT uid FROM tt_content WHERE pid=? AND header=? AND sys_language_uid=0 AND deleted=0', (pid, 'Demo polish: showcase navigation 0')).fetchone()[0]
        uid = insert('tt_content', {'pid': pid, 'CType': 'crispframe_resourcelist', 'header': marker, 'sorting': sorting, 'colPos': 0, 'sys_language_uid': language, 'l18n_parent': parent if language else 0, 'tstamp': now, 'crdate': now, 'crispframe_resourcelist_headline': 'Explore the showcase' if not language else 'Beispiele entdecken', 'crispframe_resourcelist_lead': 'Jump to a section and compare the editable examples.' if not language else 'Direkt zum Abschnitt springen und die bearbeitbaren Beispiele vergleichen.', 'crispframe_resourcelist_sectionSpacing': 'small', 'crispframe_resourcelist_sectionBackground': 'default', 'crispframe_resourcelist_width': 'default', 'crispframe_resourcelist_items': len(links)})
        if not language:
            parents[pid] = uid
        original_items = []
        if language:
            original_items = db.execute('SELECT uid FROM crispframe_resourcelist_items WHERE foreign_table_parent_uid=? AND sys_language_uid=0 AND deleted=0 ORDER BY sorting', (parent,)).fetchall()
        for index, (label, link) in enumerate(links):
            insert('crispframe_resourcelist_items', {'pid': pid, 'foreign_table_parent_uid': uid, 'sys_language_uid': language, 'l10n_parent': original_items[index]['uid'] if language and index < len(original_items) else 0, 'sorting': (index + 1) * 128, 'tstamp': now, 'crdate': now, 'label': label, 'link': link, 'icon': 'none'})
print('Added showcase navigation. Existing records were not changed.')
