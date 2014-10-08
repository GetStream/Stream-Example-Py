from django import template


register = template.Library()


def render_activity(activity):
    return ''

register.simple_tag(render_activity)
