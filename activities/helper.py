from pprint import pprint
from django.db import models
from django.contrib.admin.models import ADDITION,CHANGE,DELETION,User
from django.contrib.contenttypes.models import ContentType
from activities.models import Activity

class ActivityDescriptor(object):
    def __init__(self):
        """
        
        Arguments:
        - `self`:
        """
        pass

    def __get__(self,instance=None,owner=None):
        """
        
        Arguments:
        - `self`:
        - `instance`:
        - `owner`:
        """
        def my_func():
            print "aa"

        return my_func

class ActivityField(object):
    def __init__(self,user=None,create=None,update=None):
        """
        
        Arguments:
        - `self`:
        """
        if not create:
            self.create_message = "%s is created"
        else:
            self.create_message = create[0]

        if create == False:
            self.create_message = None
            
        self.update_message = {}
        self.fields= []
        if update:
            for field in update:
                fieldname,message = field
                self.fields.append(fieldname)
                self.update_message[fieldname] = message

        self.user = None
        if user:
            self.user = user
    def contribute_to_class(self,cls,name):
        def log(instance,message):
            #check instance of user

            _user_instance = None

            if self.user:
                if hasattr(instance,self.user):
                    _user_obj = getattr(instance,self.user)
                    if callable(_user_obj):
                        _user_insanctace = _user_obj(instance)
                    else:
                        _user_instance = _user_obj

                        if not _user_instance.__class__ == User:
                            raise Exception("User must instance of django.contrib.models.User")


            _activityInstance = Activity(user= _user_instance,
                                         content_object=instance,
                                         text=message)
            _activityInstance.save()
            
        def prepare_fields(instance):
            output = {}
            class_fields = instance.__class__._meta.fields
            instance._history_fields = {}
            all = dict([(f.name, f) for f in class_fields])
            for field_name in self.fields:
                modelfield = all[field_name]
                value = getattr(instance, modelfield.attname)
                if value is None: value = ''
                output[field_name] = unicode(value)
            return output
                                                        
        def _contribute(sender,**kwargs):
            descriptor = ActivityDescriptor()
            setattr(sender,name,descriptor)

            def pre_save(sender,**kwargs):
                """
                what to do:
                in pre save, we prepare the instance,
                we check if the instance is added or updated,
                and we add a flag in the instance using _activity_type.
                and if we track the field, we also add a old field and value
                and put in into _track_field (name,value)
                """
                instance = kwargs['instance']
                instance._activity_type = None
                instance._old_fields = None
                if instance.pk == None:
                    instance._old_fields = {}
                    for field_name in self.fields:
                        instance._old_fields[field_name] = ''

                    instance._activity_type = ADDITION
                else:
                    try:
                        db_instance = instance.__class__.objects.get(pk=instance.pk)
                    except instance.__class__.DoesNotExist:
                        db_instance = instance

                    instance._old_fields = prepare_fields(db_instance)
                    instance._activity_type = CHANGE
                
            def post_save(sender,**kwargs):
                """
                check if there is _activity_type.
                and we update the database.
                """
                instance = kwargs['instance']

                if instance._activity_type == ADDITION:
                    if self.create_message:
                        if hasattr(instance,self.create_message) and callable(getattr(instance,self.create_message)):
                            _func = getattr(instance,self.create_message)
                            _message = _func(instance)
                        else :                        
                            _message = self.create_message % instance
                            
                        log(instance, _message)
                else:
                    pre_fields = instance._old_fields
                    post_fields = prepare_fields(instance)

                    for name,after in post_fields.iteritems():
                        before = pre_fields[name]
                        if before != after:
                            _str = self.update_message[name]
                            _message = _str
                            if hasattr(instance,_str) and callable(getattr(instance,_str)):
                                func = getattr(instance,_str)
                                _message = func(instance,before=before,after=after)

                            log(instance,_message)
                #cleanup                            
                del instance._activity_type 
                del instance._old_fields
            models.signals.pre_save.connect(pre_save,sender=cls,weak=False)
            models.signals.post_save.connect(post_save,sender=cls,weak=False)
        

        models.signals.class_prepared.connect(_contribute,sender=cls,weak=False)

class ActivityHandler:
    def pre_save(self,sender,**kwargs):
        """
        
        Arguments:
        - `self`:
        """
        pprint( sender)
        pprint(kwargs)


    def post_save(self,sender,**kwargs):
        """
        
        Arguments:
        - `self`:
        - `**kwargs`:
        """
        pprint(sender)
        pprint(kwargs)

