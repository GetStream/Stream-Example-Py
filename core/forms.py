from django_stream.feed_managers import feed_manager
from core.models import Board, Pin
from django import forms
from django.template.defaultfilters import slugify
from core.models import Follow


class PinForm(forms.ModelForm):
    board_name = forms.CharField()
    remove = forms.IntegerField(required=False)

    class Meta:
        model = Pin
        exclude = ['board']

    def save(self, *args, **kwargs):
        board_name = self.cleaned_data['board_name']
        user = self.cleaned_data['user']
        remove = bool(int(self.cleaned_data.get('remove', 0) or 0))
        if remove:
            pins = Pin.objects.filter(
                user=user, item=self.cleaned_data['item'])
            for pin in pins:
                pin.delete()
            return

        # create the board with the given name
        defaults = dict(slug=slugify(board_name))
        board, created = Board.objects.get_or_create(
            user=user, name=board_name, defaults=defaults)

        # save the pin
        pin = forms.ModelForm.save(self, commit=False)
        pin.board = board
        pin.save()

        return pin


class FollowForm(forms.Form):
    user = forms.IntegerField()
    target = forms.IntegerField()
    remove = forms.IntegerField(required=False)

    def save(self):
        user = self.cleaned_data['user']
        target = self.cleaned_data['target']
        remove = bool(int(self.cleaned_data.get('remove', 0) or 0))

        if remove:
            follows = Follow.objects.filter(user=user, target=target)
            for follow in follows:
                feed_manager.unfollow_user(user, target)
                follow.delete()
            return

        follow = Follow.objects.create(user_id=user, target_id=target)
        feed_manager.follow_user(user, target)
        return follow
