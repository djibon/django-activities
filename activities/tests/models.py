from django.db import models
from django.contrib.auth.models import User
from activities import helper


class Movie(models.Model):
    name = models.CharField(max_length=150)

    activity = helper.ActivityField()
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class FakeUser(models.Model):
    user = models.OneToOneField(User,unique=True)
    status = models.CharField(max_length=150)
    comment = models.CharField(max_length=150)
    activity = helper.ActivityField(user='user',create=('this is a new one',),
                                    update=(('status','this will change'),
                                            ('comment','callable_func')))

    
    
    def callable_func(self,instance,**kwargs):
        return  "me %s update %s %s" % (str(instance),kwargs['before'],kwargs['after'])
