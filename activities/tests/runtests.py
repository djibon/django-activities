import os,sys

#hack
path = os.path.abspath(__file__)
for i in range(3):
    path = os.path.dirname(path)

sys.path.insert(0, path)
                 
os.environ['DJANGO_SETTINGS_MODULE'] = 'activities.tests.settings'



from django.test import simple
from django.db import connection
from django.db.models.loading import load_app
from django.conf import settings
import unittest


simple.setup_test_environment()
suite = simple.build_suite(load_app('activities.tests'))
old_name = settings.DATABASE_NAME
connection.creation.create_test_db(9)
result = unittest.TextTestRunner(verbosity=9).run(suite)
connection.creation.destroy_test_db(old_name, 9)
simple.teardown_test_environment()

                 

