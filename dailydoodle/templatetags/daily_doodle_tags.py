from django import template

register = template.Library()

@register.inclusion_tag("dailydoodle/nav.html")
def get_nav(current_link=None):
    # links of format { name: link}
    links = {}
    return {"links": links,"current_link": current_link}