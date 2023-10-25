from django import template 
  
register = template.Library() 
@register.filter
def item_amount(request, id):
    return request.session.cart[str(id)]['amount']