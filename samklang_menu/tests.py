"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User

from samklang_menu.templatetags.menu_tags import find_active, submenu, html_menu
from samklang_menu.models import Menu

class FindActiveTest(TestCase):

    def test_find_main(self):
        """
        Find main page even if main page is not in menu. Also checks empty
        search.
        """
        m = Menu(name="parent", url="/sitemap/", tree_id=1, user_id=1)
        m.save()
        m2 = Menu(name="main", url="/", tree_id=1, parent=m, user_id=1)
        m2.save()
        self.assertEqual(m2, find_active(1, "/"))
        self.assertEqual(m2, find_active(1, ""))

    def test_find_forum_new(self):
        """
        /forum/new/ does not exist, but /forum/ does. Checks for /forum/new
        without trailing slash as well.
        """
        m = Menu(name="parent", url="/sitemap/", tree_id=1, user_id=1)
        m.save()
        m2 = Menu(name="main", url="/", tree_id=1, parent=m, user_id=1)
        m2.save()
        m3 = Menu(name="forum", url="/forum/", tree_id=1, parent=m, user_id=1)
        m3.save()
        self.assertEqual(m3, find_active(1, "/forum/new/"))
        self.assertEqual(m3, find_active(1, "/forum/new"))

class MakeMenuTest(TestCase):

    def test_submenu(self):
        u = User()
        m = Menu(name="parent", url="/sitemap/", tree_id=1, user_id=1)
        m.save()
        m2 = Menu(name="main", url="/", tree_id=1, parent=m, user_id=1)
        m2.save()
        m3 = Menu(name="forum", url="/forum/", tree_id=1, parent=m, user_id=1)
        m3.save()
        self.assertEqual([m2, m3], submenu(m3, u))

