from django.test import TestCase
from activities.tests import models as test

class ActivityTest(TestCase):
    def testOne(self):
        """
        """
        m = test.Movie(name="the rock")
        m.save()
    
