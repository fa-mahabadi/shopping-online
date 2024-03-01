# category_tags.py
from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('product/category_list.html')
def show_categories(categories=None, depth=1):
    if categories is None:
        categories = Category.objects.filter(parent_category__isnull=True)
    # else:
    #     categories = category.nested_category.all()

    return {'categories': categories, 'depth': depth+1}
