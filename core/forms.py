from core.models import Follow
from core.models import Pin
from django import forms
from stream_django.feed_manager import feed_manager


class PinForm(forms.Form):
    item = forms.IntegerField()
    influencer = forms.IntegerField()
    remove = forms.IntegerField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PinForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        item = self.cleaned_data['item']
        influencer = self.cleaned_data['influencer']
        remove = bool(int(self.cleaned_data.get('remove', 0) or 0))
        if remove:
            pins = Pin.objects.filter(
                user=self.user, item=item)
            for pin in pins:
                pin.delete()
            return
        pin = Pin.objects.create(user=self.user, item_id=item, influencer_id=influencer)
        return pin


class FollowForm(forms.Form):
    target = forms.IntegerField()
    remove = forms.IntegerField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(FollowForm, self).__init__(*args, **kwargs)

    def save(self):
        target = self.cleaned_data['target']
        remove = bool(int(self.cleaned_data.get('remove', 0) or 0))

        if remove:
            follows = Follow.objects.filter(user=self.user, target_id=target)
            for follow in follows:
                feed_manager.unfollow_user(self.user.id, target)
                follow.delete()
            return

        follow = Follow.objects.create(user=self.user, target_id=target)
        feed_manager.follow_user(self.user_id, target)
        return follow
