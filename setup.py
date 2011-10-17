#!/usr/bin/env python
from distutils.core import setup

setup(
        name='samklang-menu',
        version="0.1.0",
        author='Sigurd Gartmann',
        author_email='sigurdga-samklang@sigurdga.no',
        url='http://github.com/sigurdga/samklang-menu',
        description='Horizontal tree menu with breadcrumbs for Samklang',
        long_description=open('README.txt').read(),
        license="AGPL",
        packages = ['samklang_menu', 'samklang_menu.templatetags', 'samklang_menu.migrations'],
        package_data = {'samklang_menu': ['templates/samklang_menu/*.html', 'locale/*/LC_MESSAGES/django.*o']},
        classifiers=[
                "Development Status :: 3 - Alpha",
                "License :: OSI Approved :: GNU Affero General Public License v3",
                "Intended Audience :: Developers",
                "Framework :: Django",
                "Environment :: Web Environment",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                ]
        )
