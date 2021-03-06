#!/usr/bin/env python3
"""Digests mod-elf json data."""
import json
import os
import uuid
import dataset

# FOLIO demo user id and new email
USER_ID = '04c0b012-5149-49c6-aded-13aef10f4619'
NEW_USER_EMAIL = 'john.doe@institution.edu'

# FOLIO demo item id and new title
ITEM_ID = '459afaba-5b39-468d-9072-eb1685e0ddf4'
NEW_ITEM_TITLE = 'Asus Tablet'

# directory
DATA_DIR = 'data'
ITEM_INFO_FILE = 'iteminfo.json'

# postgres
PG_USER = 'folio_admin'
PG_PASSWORD = 'folio_admin'
PG_NETLOC = '10.0.2.15'
PG_PORT = '5432'
PG_DBNAME = 'okapi_modules'
PG_URL = ("postgresql://" + PG_USER + ":" + PG_PASSWORD +
          '@' + PG_NETLOC + ':' + PG_PORT + '/' + PG_DBNAME)

MOD_USERS_SCHEMA = 'diku_mod_users'
MOD_USERS_TBL = 'users'

INV_STORAGE_SCHEMA = 'diku_inventory_storage'
INV_ITEM_TBL = 'item'

ELF_SCHEMA = 'diku_mod_elf'
ELF_ITEMS_TBL = 'items'


def load_json(fpath):
    """Loads a JSON file."""
    with open(fpath) as fs:
        d = json.load(fs)
    print("Loaded {0} objects from {1}...".format(len(d), fpath))
    return d


def populate_table(rows, tbl_name, schema_name, clear=True):
    """Populate a postgres table with provided rows."""
    print("Saving {0} rows to {1}.{2}...".format(
        len(rows), schema_name, tbl_name))
    with dataset.Database(url=PG_URL, schema=schema_name) as db:
        table = db[tbl_name]
        if clear:
            table.delete()
        table.insert_many(rows)
    db.executable.close()
    db = None

def update_user_email(row_id, user_email, tbl_name, schema_name):
    """Updates an user e-mail by id."""
    print("Updating e-mail to {0} for row {1} in {2}.{3}...".format(
        user_email, row_id, schema_name, tbl_name))
    with dataset.Database(url=PG_URL, schema=schema_name) as db:
        tbl = db[tbl_name]
        row = tbl.find_one(id=row_id)
        if row is not None:
            row['jsonb']['personal']['email'] = user_email
            tbl.upsert(row, ['id'])
    db.executable.close()
    db = None

def update_item_title(row_id, item_title, tbl_name, schema_name):
    """Updates an item title by id."""
    print("Updating title to {0} for row {1} in {2}.{3}...".format(
        item_title, row_id, schema_name, tbl_name))
    with dataset.Database(url=PG_URL, schema=schema_name) as db:
        tbl = db[tbl_name]
        row = tbl.find_one(_id=row_id)
        if row is not None:
            row['jsonb']['title'] = item_title
            tbl.upsert(row, ['_id'])
    db.executable.close()
    db = None


def create_item_info_row(itemid, item_info):
    """Creates item info rows."""
    print("Creating item info row for {0}...".format(itemid))
    item_info['id'] = str(uuid.uuid4())
    item_info['itemid'] = itemid
    return [dict(jsonb=item_info)]

if __name__ == '__main__':
    # update existing FOLIO user and item
    update_user_email(USER_ID, NEW_USER_EMAIL, MOD_USERS_TBL, MOD_USERS_SCHEMA)
    update_item_title(ITEM_ID, NEW_ITEM_TITLE, INV_ITEM_TBL, INV_STORAGE_SCHEMA)
    
    # load sample item info into elf items table
    item_info_path = os.path.join(DATA_DIR, ITEM_INFO_FILE)
    item_info_json = load_json(item_info_path)
    item_info_rows = create_item_info_row(ITEM_ID, item_info_json)
    populate_table(item_info_rows, ELF_ITEMS_TBL, ELF_SCHEMA)

    print('Complete...')
