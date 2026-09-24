"""Remove TYPO3 13 Content Blocks indexes on absent columns before SQLite/DBAL4 upgrade.

Content Blocks 1.x created quoted t3ver_oid/t3ver_wsid indexes for collection
tables without those columns. SQLite accepted them as expression indexes; DBAL 4
cannot introspect them. This only removes indexes whose indexed columns have no
name, and leaves all records and valid indexes intact.
"""

import sqlite3
import sys
import re

db = sqlite3.connect(sys.argv[1])
removed = []
for (table,) in list(db.execute("SELECT name FROM sqlite_master WHERE type='table'")):
    for index in list(db.execute(f'PRAGMA index_list("{table}")')):
        name = index[1]
        if not name.startswith('t3ver_oid_'):
            continue
        columns = [part for part in db.execute(f'PRAGMA index_xinfo("{name}")') if part[5]]
        if columns and all(part[2] is None for part in columns):
            db.execute(f'DROP INDEX "{name}"')
            removed.append(f'{table}.{name}')
db.commit()
print(f'Removed {len(removed)} invalid TYPO3 13 Content Blocks indexes: {", ".join(removed)}')

# TYPO3 14's image-size migration writes NULL. Some SQLite TYPO3 13 databases
# retained NOT NULL on these legacy columns, even after extension:setup.
schema = db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tt_content'").fetchone()[0]
new_schema = schema
for column in ('imagewidth', 'imageheight'):
    new_schema, count = re.subn(
        rf'("?){column}\1 INTEGER UNSIGNED DEFAULT 0 NOT NULL\b',
        lambda match: f'{match.group(1)}{column}{match.group(1)} INTEGER UNSIGNED DEFAULT NULL', new_schema,
    )
    if count not in (0, 1):
        raise RuntimeError(f'Unexpected schema for tt_content.{column}')
if new_schema != schema:
    indexes = [row[0] for row in db.execute("SELECT sql FROM sqlite_master WHERE type IN ('index','trigger') AND tbl_name='tt_content' AND sql IS NOT NULL")]
    original_count = db.execute('SELECT COUNT(*) FROM tt_content').fetchone()[0]
    db.execute('PRAGMA foreign_keys=OFF')
    with db:
        db.execute(new_schema.replace('CREATE TABLE tt_content', 'CREATE TABLE tt_content_upgrade', 1).replace('CREATE TABLE "tt_content"', 'CREATE TABLE "tt_content_upgrade"', 1))
        db.execute('INSERT INTO tt_content_upgrade SELECT * FROM tt_content')
        db.execute('DROP TABLE tt_content')
        db.execute('ALTER TABLE tt_content_upgrade RENAME TO tt_content')
        for sql in indexes:
            db.execute(sql)
    assert db.execute('SELECT COUNT(*) FROM tt_content').fetchone()[0] == original_count
    print('Made tt_content.imagewidth and imageheight nullable for the TYPO3 14 migration.')
