# Db-Elf

Copyright (C) 2017 The Open Library Foundation

This software is distributed under the terms of the Apache License,
Version 2.0. See the file "[LICENSE](LICENSE)" for more information.

## Introduction

Db-Elf contains a Python script that will use the FOLIO demo database to create sample data for Mod-Elf.

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
