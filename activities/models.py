from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from datetime import datetime


class Activity(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey('content_type','object_id')
    created_at      = models.DateTimeField(_('created_at'), default=datetime.now)
    text = models.TextField("message",blank=True)

    def __unicode__(self):
        return "%s %s at %s" % (str(self.user),self.text,str(self.created_at))

    class Meta:
        verbose_name="activity"
        verbose_name_plural = "activities"
        ordering = ['created_at']
        
    
    
    
