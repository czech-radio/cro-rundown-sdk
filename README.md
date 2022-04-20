# 𝖈𝖗𝖔-𝖗𝖚𝖓𝖉𝖔𝖜𝖓-𝖘𝖉𝖐

[RELEASES](https://github.com/czech-radio/cro-rundown-sdk/releases/) | [WEBSITE](https://czech-radio.github.io/cro-rundown-sdk/)

![language](https://img.shields.io/badge/language-Python_v3.10+-blue.svg)
![version](https://img.shields.io/badge/version-0.2.0-blue.svg)
[![main](https://github.com/czech-radio/cro-rundown-sdk/actions/workflows/main.yml/badge.svg)](https://github.com/czech-radio/cro-rundown-sdk/actions/workflows/main.yml)
[![reliability](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro-rundown-sdk&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=czech-radio_cro-rundown-sdk)

**Python library to work with Rozhlas rundowns.**

**DISCLAIMER:** Althougt we develop this package as open-source it is used internally for parsing specific type of
XML file (know as _Rundown_) exported from OpenMedia broadcast system. Feel free to read the source code.

:star: Star us on GitHub — it motivates us!

## Features & Usage

- [x] Arrange the rundown files.
- [x] Cleanse the rundown files.
- [ ] Extract the rundown datas.

(Todo: Add `--check` option what rundowns will be affected by running specified command.)

### The `arrange` command

Use `cro.rundown.arrange` command to: &hellip;

    cro.rundown.arrange [--source]

### The `cleanse` command

Use `cro.rundown.cleanse` command to: &hellip;

    cro.rundown.cleanse [--source]

### The `extract` command

Use `cro.rundown.extract` command to extract the broadcast data from the rundown XML files.

    cro.rundown.extract [--source]

## Installation

* We assume that you use at least Python 3.10.
* We assume that you use the virtual environment.

Install the package latest version from the GitHub repository.

    pip install git+https://github.com/czech-radio/cro-rundown-sdk.git

## Contribution

See the document [here](/.github\CONTRIBUTING.md)


## Documentation

The complete documentation soon&hellip;
