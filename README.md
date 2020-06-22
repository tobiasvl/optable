Optable
=======

> **optable** \[Latin: _optabilis_\] _(obsolete)_ That may be chosen; desirable.

A website with (reverse) opcode tables for various CPUs. Work in progress.

Inspired by [Pastraiser's opcode tables](https://pastraiser.com/) and based on the [GBDev Game Boy opcode table website](https://gbdev.io/gb-opcodes/optables/).

File structure
--------------

Each architecture has two directories:

* `collections/<arch>/`: HTML and Markdown templates
* `_data/<arch>/`: Data sources
  * `generate_opcodes.py`: Script that generates `opcodes.json`
  * `instructions.json`: JSON file with all instructions
  * `flags.json`: JSON file with flag registers

The file structure isn't very logical right now. The templates in `collections` shouldn't need to be duplicated per architecture, and should probably live in `_layouts` somehow. Pull requests rectifying this are very welcome.
