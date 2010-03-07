from django.test import TestCase
from django.contrib.auth.models import User
from activities.tests import models as test
from activities.models import Activity

class ActivityTest(TestCase):
    def testOne(self):
        """
        """
        m = test.Movie(name="the rock")
        m.save()

        self.assertEqual(1,Activity.objects.count())
        print Activity.objects.all()

    def testTwo(self):
        user = User(username="john_doe")
        user.save()
        f = test.FakeUser(status="",user=user)
        f.save()

        f1 = test.FakeUser.objects.get()
        f1.status="i am here"
        f1.comment=" ia m comment"
        f1.save()

        print Activity.objects.all()

        
