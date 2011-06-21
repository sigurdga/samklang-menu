#!/usr/bin/env python
from distutils.core import setup

setup(
        name = 's7n-menu',
        version = "1a1",
        packages = ['s7n.menu', 's7n.menu.templatetags'],
        package_data = {'s7n.menu': ['templates/menu/*.html']},
        )
