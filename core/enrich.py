from stream_django.enrich import Enrich as BaseEnrich
from core.models import Follow
from core.models import Pin


def did_i_pin_items(user, items):
    pinned_items_ids = user.pin_set.filter(item_id__in=items).values_list('item_id', flat=True)
    for item in items:
        item.pinned = item.id in pinned_items_ids


def did_i_pin(user, pins):
    did_i_pin_items(user, [pin.item for pin in pins])


def do_i_follow_users(user, users):
    followed_user_ids = Follow.objects.filter(user=user, target__in=users).values_list('target_id', flat=True)
    for u in users:
        u.followed = u.id in followed_user_ids


def do_i_follow(user, follows):
    do_i_follow_users(user, [f.target for f in follows])


class Enrich(BaseEnrich):

    def __init__(self, current_user, *args, **kwargs):
        super(Enrich, self).__init__(*args, **kwargs)
        self.current_user = current_user

    def fetch_pin_instances(self, pks):
        pins = Pin.objects.select_related(*Pin.activity_related_models()).in_bulk(pks)
        if self.current_user.is_authenticated():
            did_i_pin(self.current_user, pins.values())
        return pins

    def fetch_follow_instances(self, pks):
        follows = Follow.objects.select_related(*Follow.activity_related_models()).in_bulk(pks)
        if self.current_user.is_authenticated():
            do_i_follow(self.current_user, follows.values())
        return follows
