"""Maintainer-only additive 1.4 demo authoring. Never run on a customer site."""

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


def page(title, slug, parent, language=0, translation=0, layout='', sorting=512, abstract=''):
    found = db.execute('SELECT uid FROM pages WHERE slug=? AND sys_language_uid=? AND deleted=0',
                       (slug, language)).fetchone()
    if found:
        return found[0]
    return clone('pages', 14 if language else 13, {
        'pid': parent, 'sorting': sorting, 'title': title, 'nav_title': title,
        'slug': slug, 'sys_language_uid': language, 'l10n_parent': translation,
        'l10n_source': 0, 'nav_hide': 0, 'hidden': 0, 'deleted': 0,
        'backend_layout': layout, 'backend_layout_next_level': '',
        'abstract': abstract, 'description': abstract, 'seo_title': title,
        'og_title': title, 'og_description': abstract,
        'twitter_title': title, 'twitter_description': abstract,
        'media': 0,
    })


def block(pid, language, kind, marker, fields, sorting, translation=0, colpos=0):
    found = db.execute('SELECT uid FROM tt_content WHERE pid=? AND sys_language_uid=? AND header=? AND deleted=0',
                       (pid, language, marker)).fetchone()
    if found:
        return found[0]
    typename = kind.replace('-', '')
    fields = {'sectionSpacing': 'default', 'sectionBackground': 'default', 'width': 'default', **fields}
    values = {
        'pid': pid, 'sorting': sorting, 'colPos': colpos,
        'sys_language_uid': language, 'l18n_parent': translation,
        'CType': f'crispframe_{typename}', 'header': marker,
        'hidden': 0, 'deleted': 0,
    }
    values.update({f'crispframe_{typename}_{key}': value for key, value in fields.items()})
    return clone('tt_content', 2, values, prefix=f'crispframe_{typename}_')


def block_pair(pid, kind, name, english, german, sorting, colpos=0):
    en = block(pid, 0, kind, f'Demo 1.4: {name}', english, sorting, colpos=colpos)
    de = block(pid, 1, kind, f'Demo 1.4: {name} DE', german, sorting,
               translation=en, colpos=colpos)
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
        en_uid = db.execute(f'INSERT INTO {table} ({names}) VALUES ({placeholders})',
                            tuple(shared.values())).lastrowid
        localized = {**shared, 'foreign_table_parent_uid': de_parent,
                     'sys_language_uid': 1, 'l10n_parent': en_uid, **de}
        names = ','.join(localized)
        placeholders = ','.join('?' for _ in localized)
        db.execute(f'INSERT INTO {table} ({names}) VALUES ({placeholders})',
                   tuple(localized.values()))


def core_text(pid, language, marker, title, body, sorting, translation=0):
    found = db.execute('SELECT uid,header FROM tt_content WHERE pid=? AND sys_language_uid=? AND header IN (?,?) AND deleted=0',
                       (pid, language, marker, title)).fetchone()
    if found:
        if found['header'] == marker:
            db.execute('UPDATE tt_content SET header=? WHERE uid=?', (title, found['uid']))
        return found[0]
    return clone('tt_content', 88 if language else 87, {
        'pid': pid, 'sorting': sorting, 'colPos': 0,
        'sys_language_uid': language, 'l18n_parent': translation,
        'CType': 'text', 'header': title, 'header_layout': 2,
        'bodytext': body, 'hidden': 0, 'deleted': 0,
    })


def media(pid, en_owner, de_owner, field, file_uid, en_alt, de_alt, table='pages'):
    found = db.execute('SELECT uid FROM sys_file_reference WHERE tablenames=? AND fieldname=? AND uid_foreign=? AND deleted=0',
                       (table, field, en_owner)).fetchone()
    if found:
        return
    en = clone('sys_file_reference', 5, {
        'pid': pid, 'uid_local': file_uid, 'uid_foreign': en_owner,
        'tablenames': table, 'fieldname': field,
        'sys_language_uid': 0, 'l10n_parent': 0, 'alternative': en_alt,
        'deleted': 0,
    })
    clone('sys_file_reference', 6, {
        'pid': pid, 'uid_local': file_uid, 'uid_foreign': de_owner,
        'tablenames': table, 'fieldname': field,
        'sys_language_uid': 1, 'l10n_parent': en, 'alternative': de_alt,
        'deleted': 0,
    })
    column = 'media' if table == 'pages' else field
    db.execute(f'UPDATE {table} SET {column}=1 WHERE uid IN (?,?)', (en_owner, de_owner))


assert db.execute('SELECT title FROM pages WHERE uid=1').fetchone()[0] == 'Home'

insights = page('Insights', '/insights', 1, sorting=512,
                abstract='Ideas and practical guidance for clearer digital services.')
insights_de = page('Wissen', '/wissen', 1, 1, insights, sorting=512,
                   abstract='Ideen und praktische Anleitungen für verständliche digitale Angebote.')
resources = page('Resources', '/resources', 1, sorting=640,
                 abstract='Guides, examples and useful starting points for your team.')
resources_de = page('Ressourcen', '/ressourcen', 1, 1, resources, sorting=640,
                    abstract='Leitfäden, Beispiele und nützliche Ausgangspunkte für Ihr Team.')
guide = page('Make service pages easier to use', '/insights/clear-service-pages', insights,
             layout='pagets__Article', sorting=128,
             abstract='A short guide to writing and organizing a helpful service page.')
guide_de = page('Serviceseiten verständlicher gestalten', '/wissen/klare-service-seiten',
                insights, 1, guide, layout='pagets__Article', sorting=128,
                abstract='Ein kurzer Leitfaden für hilfreiche und gut strukturierte Serviceseiten.')
checklist = page('A practical content checklist', '/insights/content-checklist', insights,
                 layout='pagets__Article', sorting=256,
                 abstract='Questions to ask before publishing an important page.')
checklist_de = page('Eine praktische Inhaltscheckliste', '/wissen/inhaltscheckliste',
                    insights, 1, checklist, layout='pagets__Article', sorting=256,
                    abstract='Fragen, die Sie vor der Veröffentlichung einer wichtigen Seite stellen sollten.')

media(insights, guide, guide_de, 'media', 20,
      'Colleagues plan a clear digital service together',
      'Kolleginnen und Kollegen planen gemeinsam einen verständlichen digitalen Service')
media(insights, checklist, checklist_de, 'media', 21,
      'A team reviews content on a large screen',
      'Ein Team prüft Inhalte auf einem großen Bildschirm')

block_pair(insights, 'intro', 'insights intro',
           {'headline': 'Ideas worth putting to work', 'lead': 'Short guidance for clearer digital experiences.',
            'text': 'Explore the articles below and adapt their ideas to your organization.', 'link': '', 'linkLabel': '',
            'isPageTitle': 1, 'sectionSpacing': 'small'},
           {'headline': 'Ideen für die Praxis', 'lead': 'Kurze Anleitungen für verständliche digitale Angebote.',
            'text': 'Entdecken Sie die Artikel und passen Sie die Ideen an Ihre Organisation an.', 'link': '', 'linkLabel': '',
            'isPageTitle': 1, 'sectionSpacing': 'small'}, 64)
block_pair(insights, 'child-pages', 'insights articles',
           {'headline': 'Latest articles', 'lead': 'Choose a topic to explore.', 'parentPage': insights, 'layout': 'cards', 'sectionSpacing': 'small'},
           {'headline': 'Aktuelle Artikel', 'lead': 'Wählen Sie ein Thema.', 'parentPage': insights, 'layout': 'cards', 'sectionSpacing': 'small'}, 128)

block_pair(resources, 'intro', 'resources intro',
           {'headline': 'Useful resources', 'lead': 'Tools and examples for planning your next project.',
            'text': 'These editable examples show how to organize practical content.', 'link': '', 'linkLabel': '',
            'isPageTitle': 1, 'sectionSpacing': 'small'},
           {'headline': 'Nützliche Ressourcen', 'lead': 'Werkzeuge und Beispiele für Ihr nächstes Projekt.',
            'text': 'Diese bearbeitbaren Beispiele zeigen, wie sich praktische Inhalte strukturieren lassen.', 'link': '', 'linkLabel': '',
            'isPageTitle': 1, 'sectionSpacing': 'small'}, 64)
tabs_en, tabs_de = block_pair(resources, 'tabs', 'resource topics',
                              {'headline': 'Choose your starting point', 'lead': 'Two ways to improve an existing site.', 'items': 2, 'sectionSpacing': 'small'},
                              {'headline': 'Wählen Sie Ihren Einstieg', 'lead': 'Zwei Wege, eine bestehende Website zu verbessern.', 'items': 2, 'sectionSpacing': 'small'}, 128)
children('crispframe_tabs_items', resources, tabs_en, tabs_de,
         [{'label': 'Content', 'title': 'Start with useful answers', 'text': '<p>Identify the questions visitors bring to each page, then put the answers first.</p>', 'image': 0},
          {'label': 'Design', 'title': 'Make each action clear', 'text': '<p>Use a simple visual hierarchy and one obvious next step for every section.</p>', 'image': 0}],
         [{'label': 'Inhalte', 'title': 'Mit hilfreichen Antworten beginnen', 'text': '<p>Ermitteln Sie die Fragen Ihrer Besucherinnen und Besucher und beantworten Sie sie zuerst.</p>', 'image': 0},
          {'label': 'Gestaltung', 'title': 'Jeden Schritt verständlich machen', 'text': '<p>Nutzen Sie eine klare visuelle Hierarchie und einen eindeutigen nächsten Schritt.</p>', 'image': 0}])
links_en, links_de = block_pair(resources, 'resource-list', 'recommended links',
                                {'headline': 'Explore further', 'lead': 'Selected pages from this example site.', 'items': 3, 'sectionSpacing': 'small'},
                                {'headline': 'Mehr entdecken', 'lead': 'Ausgewählte Seiten dieser Beispielwebsite.', 'items': 3, 'sectionSpacing': 'small'}, 256)
children('crispframe_resourcelist_items', resources, links_en, links_de,
         [{'label': 'Service page guide', 'description': 'Plan a page around visitor needs.', 'link': f't3://page?uid={guide}', 'icon': 'layers-3'},
          {'label': 'Content checklist', 'description': 'Review a page before publication.', 'link': f't3://page?uid={checklist}', 'icon': 'arrow-right'},
          {'label': 'Selected work', 'description': 'See the approach in context.', 'link': 't3://page?uid=2', 'icon': 'briefcase-business'}],
         [{'label': 'Leitfaden für Serviceseiten', 'description': 'Eine Seite an den Bedürfnissen der Besucher ausrichten.', 'link': f't3://page?uid={guide}', 'icon': 'layers-3'},
          {'label': 'Inhaltscheckliste', 'description': 'Eine Seite vor der Veröffentlichung prüfen.', 'link': f't3://page?uid={checklist}', 'icon': 'arrow-right'},
          {'label': 'Ausgewählte Projekte', 'description': 'Den Ansatz im Zusammenhang sehen.', 'link': 't3://page?uid=2', 'icon': 'briefcase-business'}])

next_en, next_de = block_pair(resources, 'tabs', 'next steps',
                              {'headline': 'From idea to launch', 'lead': 'A second independent tab group.', 'items': 2, 'sectionSpacing': 'small'},
                              {'headline': 'Von der Idee zum Start', 'lead': 'Eine zweite unabhängige Registerkartengruppe.', 'items': 2, 'sectionSpacing': 'small'}, 384)
children('crispframe_tabs_items', resources, next_en, next_de,
         [{'label': 'Plan', 'title': 'Decide what matters', 'text': '<p>Agree on the audience and the most important outcome.</p>', 'image': 0},
          {'label': 'Publish', 'title': 'Check before launch', 'text': '<p>Review language, accessibility and links before going live.</p>', 'image': 0}],
         [{'label': 'Planen', 'title': 'Das Wesentliche festlegen', 'text': '<p>Stimmen Sie Zielgruppe und wichtigstes Ergebnis ab.</p>', 'image': 0},
          {'label': 'Veröffentlichen', 'title': 'Vor dem Start prüfen', 'text': '<p>Prüfen Sie Sprache, Barrierefreiheit und Links vor dem Start.</p>', 'image': 0}])

block_pair(guide, 'hero', 'service article hero',
           {'eyebrow': 'Practical guide', 'headline': 'Make service pages easier to use',
            'subheadline': 'A useful page starts with the visitor\'s next question.',
            'isHero': 1, 'image': 0, 'imageAlt': '', 'imagePosition': 'right',
            'mediaCrop': 'landscape', 'primaryLink': '', 'primaryLinkLabel': '',
            'secondaryLink': '', 'secondaryLinkLabel': '', 'sectionBackground': 'subtle'},
           {'eyebrow': 'Praxisleitfaden', 'headline': 'Serviceseiten verständlicher gestalten',
            'subheadline': 'Eine hilfreiche Seite beginnt mit der nächsten Frage der Besucher.',
            'isHero': 1, 'image': 0, 'imageAlt': '', 'imagePosition': 'right',
            'mediaCrop': 'landscape', 'primaryLink': '', 'primaryLinkLabel': '',
            'secondaryLink': '', 'secondaryLinkLabel': '', 'sectionBackground': 'subtle'}, 64)
block_pair(checklist, 'hero', 'checklist article hero',
           {'eyebrow': 'Editorial checklist', 'headline': 'A practical content checklist',
            'subheadline': 'A short review before a page goes live.',
            'isHero': 1, 'image': 0, 'imageAlt': '', 'imagePosition': 'right',
            'mediaCrop': 'landscape', 'primaryLink': '', 'primaryLinkLabel': '',
            'secondaryLink': '', 'secondaryLinkLabel': '', 'sectionBackground': 'subtle'},
           {'eyebrow': 'Redaktionelle Checkliste', 'headline': 'Eine praktische Inhaltscheckliste',
            'subheadline': 'Eine kurze Prüfung vor der Veröffentlichung.',
            'isHero': 1, 'image': 0, 'imageAlt': '', 'imagePosition': 'right',
            'mediaCrop': 'landscape', 'primaryLink': '', 'primaryLinkLabel': '',
            'secondaryLink': '', 'secondaryLinkLabel': '', 'sectionBackground': 'subtle'}, 64)

text_en = core_text(guide, 0, 'Demo 1.4: article body', 'Write for the next question',
                    '<p>People arrive with a goal. Give that goal a plain-language heading and a short answer near the top of the page.</p><p>Group details by task, use descriptive links, and make the next step visible without making visitors search for it.</p>', 128)
core_text(guide, 1, 'Demo 1.4: article body DE', 'Für die nächste Frage schreiben',
          '<p>Menschen kommen mit einem Ziel. Geben Sie diesem Ziel eine verständliche Überschrift und beantworten Sie die wichtigste Frage früh.</p><p>Ordnen Sie Details nach Aufgaben, verwenden Sie aussagekräftige Links und zeigen Sie den nächsten Schritt deutlich.</p>', 128, text_en)
block_pair(guide, 'pull-quote', 'article quotation',
           {'quote': 'Good content helps people decide what to do next.', 'attribution': 'Crispframe editorial team',
            'role': 'Service design', 'sectionSpacing': 'small', 'width': 'narrow'},
           {'quote': 'Gute Inhalte helfen Menschen, den nächsten Schritt zu finden.', 'attribution': 'Crispframe-Redaktion',
            'role': 'Servicegestaltung', 'sectionSpacing': 'small', 'width': 'narrow'}, 256)
author_en, author_de = block_pair(guide, 'author-card', 'article author',
                                  {'name': 'Alex Morgan', 'role': 'Content strategist',
                                   'bio': 'Alex helps teams make complex services easier to understand.',
                                   'portrait': 0, 'link': '', 'linkLabel': ''},
                                  {'name': 'Alex Morgan', 'role': 'Content-Strategie',
                                   'bio': 'Alex hilft Teams, komplexe Angebote verständlicher zu machen.',
                                   'portrait': 0, 'link': '', 'linkLabel': ''}, 128, colpos=2)

check_en = core_text(checklist, 0, 'Demo 1.4: checklist body', 'Before you publish',
                     '<p>Can visitors identify the page purpose in a few seconds? Is the most important action visible? Are links descriptive and images given useful alternative text?</p><p>Review the mobile layout and the translated page before publishing.</p>', 128)
core_text(checklist, 1, 'Demo 1.4: checklist body DE', 'Vor der Veröffentlichung',
          '<p>Erkennen Besucher den Zweck der Seite in wenigen Sekunden? Ist die wichtigste Handlung sichtbar? Sind Links aussagekräftig und Bilder sinnvoll beschrieben?</p><p>Prüfen Sie vor der Veröffentlichung auch die mobile Ansicht und die Übersetzung.</p>', 128, check_en)

# Tighten only the known, newly authored demo blocks when rerunning locally.
for typename in ('intro', 'childpages', 'tabs', 'resourcelist'):
    db.execute(f"UPDATE tt_content SET crispframe_{typename}_sectionSpacing='small' "
               f"WHERE CType='crispframe_{typename}' AND header LIKE 'Demo 1.4:%' "
               f"AND crispframe_{typename}_sectionSpacing='default'")
db.execute("UPDATE tt_content SET crispframe_intro_isPageTitle=1 WHERE CType='crispframe_intro' "
           "AND header IN ('Demo 1.4: insights intro','Demo 1.4: insights intro DE',"
           "'Demo 1.4: resources intro','Demo 1.4: resources intro DE')")
db.execute("UPDATE tt_content SET crispframe_authorcard_portrait=0 WHERE CType='crispframe_authorcard' "
           "AND header IN ('Demo 1.4: article author','Demo 1.4: article author DE')")
db.execute("UPDATE sys_file_reference SET deleted=1 WHERE tablenames='tt_content' "
           "AND fieldname='crispframe_authorcard_portrait' AND uid_foreign IN "
           "(SELECT uid FROM tt_content WHERE CType='crispframe_authorcard' "
           "AND header IN ('Demo 1.4: article author','Demo 1.4: article author DE'))")
db.execute("UPDATE tt_content SET crispframe_pullquote_sectionSpacing='small', "
           "crispframe_pullquote_sectionBackground='default' WHERE CType='crispframe_pullquote' "
           "AND header IN ('Demo 1.4: article quotation','Demo 1.4: article quotation DE')")

db.commit()
print('Added bilingual 1.4 Insights, Resources, two articles, and five new block examples.')
