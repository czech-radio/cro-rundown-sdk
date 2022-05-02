# 𝖈𝖗𝖔-𝖗𝖚𝖓𝖉𝖔𝖜𝖓-𝖘𝖉𝖐

[RELEASES](https://github.com/czech-radio/cro-rundown-sdk/releases/) | [WEBSITE](https://czech-radio.github.io/cro-rundown-sdk/)

![language](https://img.shields.io/badge/language-Python_v3.10+-blue.svg)
![version](https://img.shields.io/badge/version-0.3.0-blue.svg)
[![main](https://github.com/czech-radio/cro-rundown-sdk/actions/workflows/main.yml/badge.svg)](https://github.com/czech-radio/cro-rundown-sdk/actions/workflows/main.yml)
[![reliability](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro-rundown-sdk&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=czech-radio_cro-rundown-sdk)

**Python library and command line program to work with Rozhlas rundowns.**

**DISCLAIMER:** Althougt we develop this package as open-source it is used internally for parsing specific type of
XML file (know as _Rundown_) exported from OpenMedia broadcast system. Feel free to read the source code.

:star: Star us on GitHub — it motivates us!

## Features & Usage

- [ ] Archive rundown files
- [x] Arrange rundown files.
- [x] Cleanse rundown files.
- [x] Extract rundown datas.

(Todo: Add `--check` option what rundowns will be affected by running specified command.)

### The `arrange` command

Use `cro.rundown.arrange` command to arrange the rundown files.

    cro.rundown.arrange --source <path>                             e.g.
    cro.rundown.arrange --source \\cro.cz\srv\annova\export-avo
    
    
    PREPARE: Rundown 10
    100%|███████████████████████████████████████████████████████████████████████████████████████| 72/72 [00:10<00:00,  7.06it/s]
    100%|███████████████████████████████████████████████████████████████████████████████████████| 69/69 [00:12<00:00,  5.42it/s]
     51%|████████████████████████████████████████████▏                                          | 35/69 [00:04<00:04,  8.41it/s]


### The `cleanse` command

Use `cro.rundown.cleanse` command to cleanse the rundown files.

    cro.rundown.cleanse -i . -o .

### The `extract` command

Use `cro.rundown.extract` command to extract data from rundown files.

     cro.rundown.extract -i .\data\source\2021\W44\ -o .\data\target\2021\w44
     cro.rundown.extract --input .\data\source\2021\W44\ --output .\data\target\2021\w44

### The `archive` command

Use `cro.rundown.archive` command to archive data from rundown files.

    cro.rundown.archive -i . -o .

## Installation

* We assume that you use at least Python 3.10.
* We assume that you use the virtual environment.

Install the package latest version from the GitHub repository.

    pip install git+https://github.com/czech-radio/cro-rundown-sdk.git

## Contribution

See the document [here](/.github\CONTRIBUTING.md)


## Documentation

The complete documentation soon&hellip;
