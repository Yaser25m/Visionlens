from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    """طرح قيمة من أخرى"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def multiply(value, arg):
    """ضرب قيمة في أخرى"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def currency(value):
    """تنسيق العملة"""
    try:
        return f"{int(value):,} د.ع"
    except (ValueError, TypeError):
        return "0 د.ع"


@register.filter
def free_shipping_remaining(cart_total):
    """حساب المبلغ المطلوب للشحن المجاني"""
    try:
        remaining = 50000 - int(cart_total)
        return max(0, remaining)
    except (ValueError, TypeError):
        return 50000
