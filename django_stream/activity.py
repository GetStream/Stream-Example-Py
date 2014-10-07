from django.template.defaultfilters import slugify
from django.utils.timezone import make_naive
import pytz


class Activity(object):
    
    @classmethod
    def content_type(cls):
        '''
        the content_type reference for this activity model
        '''
        return '%s.%s' % (cls._meta.app_label, cls._meta.object_name)

    @property
    def related_models(self):
        '''
        Use this hook to setup related data to preload
        when reading activities from feeds.
        It must return None or a list of relationships see Django select_related for reference
        '''
        pass

    @property
    def extra_activity_data(self):
        '''
        Use this hook to setup extra activity data
        '''
        pass

    @property
    def actor_id(self):
        return self.user_id
    
    @property
    def verb(self):
        model_name = slugify(self.__class__.__name__)
        return model_name
    
    @property
    def object(self):
        foreign_id = '%s:%s' % (self.__class__.content_type(), self.pk)
        return foreign_id

    @property
    def foreign_id(self):
        return self.object

    @property
    def time(self):
        return make_naive(self.created_at, pytz.utc)
    
    @property
    def notify(self):
        pass
    
    def create_activity(self):
        extra_data = self.extra_activity_data()
        if not extra_data:
            extra_data = {}
        
        to = self.notify
        if to:
            extra_data['to'] = to
        
        activity = dict(
            actor=self.actor_id,
            verb=self.verb,
            object=self.object,
            foreign_id=self.foreign_id,
            time=self.time,
            **extra_data
        )
        return activity
