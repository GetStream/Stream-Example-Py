from core.models import Follow
from core.models import Pin
from django import forms
from datetime import datetime


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
        else:
            pin = Pin.objects.create(user=self.user, item_id=item, influencer_id=influencer)


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
            now = datetime.now()
            for follow in follows:
                follow.deleted_at = now
                follow.save()
        else:
            follow, created = Follow.objects.get_or_create(user=self.user, target_id=target)
            if not created:
                follow.deleted_at = None
                follow.save()
