# Db-Elf

Copyright (C) 2017 The Open Library Foundation

This software is distributed under the terms of the Apache License,
Version 2.0. See the file "[LICENSE](LICENSE)" for more information.

## Introduction

Db-Elf contains a Python script that will use the FOLIO demo database to create sample data for Mod-Elf.

## Configure Db-Elf

Mod-Elf will send a receipt via e-mail to the patron that has checked out an electronic item. For testing purposes, we recommend changing the e-mail address of one of the users in the FOLIO demo database to your own e-mail address.

1. Open init_mod_elf.py
    ```bash
    code ~/Desktop/folio/db/db-elf/init_mod_elf.py
    ```
1. Replace the `NEW_USER_EMAIL` with your own e-mail address.
    ```python
    # FOLIO demo user id and new email
    USER_ID = '04c0b012-5149-49c6-aded-13aef10f4619'
    NEW_USER_EMAIL = 'john.doe@institution.edu'
    ```

## Ingest Db-Elf Sample Data

1. Start postgresql database.
    ```bash
    sudo ifconfig lo0 alias 10.0.2.15
    brew services restart postgresql@9.6
    ```
1. Run Python ingestion script.
    ```bash
    source activate folio
    python ~/Desktop/folio/db/db-elf/init_mod_elf.py
    source deactivate folio
    ```
