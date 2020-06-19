---
layout: optable
theme: default

---

Changes from Pastraiser's tables
================================

This table is based on several sources, but heavily inspired by Pastraiser's opcode tables:

* [Pastraiser's 8080 table](https://pastraiser.com/cpu/i8080/i8080_opcodes.html)
* [Pastraiser's 8085 table](https://pastraiser.com/cpu/i8085/i8085_opcodes.html)

The following are the changes in this table from Pastraiser's.

Errata
------
* `SIM` uses 10 cycles (and 3 states), not 4 cycles. (Source: Intel's _8080/8085 Assembly Language Programming Manual_)

Other changes
-------------
* Use Intel's own instruction groups for classification
  * Classify `XTHL` as both "machine control" and "data transfer", as Intel does

New features
------------
* 8080 and 8085 in the same table
* Show when a flag is always set/reset (rather than just listing it as changed), like on other Pastraiser tables
* List duration in states, not just cycles
* Descriptions of each instruction
* Octal display, in addition to hexadecimal
