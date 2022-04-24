# -*- coding: utf-8 -*-

import os


def test_arrange_program_entrypoint():
    exit_status = os.system("cro.rundown.arrange --help")
    assert exit_status == 0


def test_cleanse_program_entrypoint():
    exit_status = os.system("cro.rundown.cleanse --help")
    assert exit_status == 0


def test_extract_program_entrypoint():
    exit_status = os.system("cro.rundown.extract --help")
    assert exit_status == 0
