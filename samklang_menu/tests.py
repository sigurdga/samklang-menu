"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from samklang_menu.models import Menu

class FindActiveTest(TestCase):

    def test_find_main(self):
        """
        Find main page even if main page is not in menu. Also checks empty
        search.
        """

        s = Site.objects.get(pk=1) # we always have a site: from django
        m = Menu(name="parent", url="/sitemap/", tree_id=s.id, user_id=1)
        m.save()
        m2 = Menu(name="main", url="/", tree_id=s.id, parent=m, user_id=1)
        m2.save()
        self.assertEqual(m2, Menu.find_active(s, "/"))
        self.assertEqual(m2, Menu.find_active(s, ""))

    def test_find_forum_new(self):
        """
        /forum/new/ does not exist, but /forum/ does. Checks for /forum/new
        without trailing slash as well.
        """

        s = Site.objects.get(pk=1) # we always have a site: from django
        m = Menu(name="parent", url="/sitemap/", tree_id=s.id, user_id=1)
        m.save()
        m2 = Menu(name="main", url="/", tree_id=s.id, parent=m, user_id=1)
        m2.save()
        m3 = Menu(name="forum", url="/forum/", tree_id=s.id, parent=m, user_id=1)
        m3.save()
        self.assertEqual(m3, Menu.find_active(s, "/forum/new/"))
        self.assertEqual(m3, Menu.find_active(s, "/forum/new"))

class MakeMenuTest(TestCase):

    def test_submenu(self):
        """
        Test making a simple menu.
        """

        s = Site.objects.get(pk=1) # we always have a site: from django
        u = User()
        m = Menu(name="parent", url="/sitemap/", tree_id=s.id, user_id=1)
        m.save()
        m2 = Menu(name="main", url="/", tree_id=s.id, parent=m, user_id=1)
        m2.save()
        m3 = Menu(name="forum", url="/forum/", tree_id=s.id, parent=m, user_id=1)
        m3.save()
        self.assertEqual([m2, m3], m3.submenu(u))

