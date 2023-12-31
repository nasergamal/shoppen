'''
    CartSession (class): handle session creation and any modification to cart session.
    
    cart_items_update (function): update User's Cart database with cart session items
    
'''
from main.models import Product
from cart.models import CartItem

class CartSession():
    '''
    handle cart session logic
    '''
    
    def __init__(self, request):
        '''Get or create session for cart'''
        # self.cart = settings.session.get(settings.CART_SESSION, {})
        self.session = request.session
        self.cart = self.session.get('cart', {})
        self.save()
    
    def add(self, request, product, amount):
        '''Create/add item to cart'''
        id = str(product.id)
        if id not in self.cart:
            self.cart[id] = amount
        else:
            self.cart[id] += amount
        if self.cart[id] > product.stock:
            self.cart[id] = product.stock
        self.save()
    
    def decrement(self, request, id):
        '''Decrease/remove item from cart'''
        if id in self.cart:
            self.cart[id] -= 1
            if self.cart[id] <= 0:
                del self.cart[id]
        self.save()
            
    def remove(self, request, id):
        '''Remove item from cart'''
        if id in self.cart:
            del self.cart[id]
        self.save()
            
    def total_price(self):
        '''Return total price of all items in cart'''
        id_list = [i for i in self.cart.keys()]
        items = Product.objects.filter(id__in=id_list)
        total_price = sum([item.price * self.cart[str(item.id)]  for item in items])
        return total_price
    
    def item_quantity(self, id):
        '''Return cart items' count'''
        id = self.cart.get(str(id))
        if id:
            return id
        return 0
        
    def __len__(self):
        return sum([i for i in self.cart.values()])
        # total_amount = sum([i.values().amount for i in self.cart.values()])
        return 1
    
    def save(self):
        '''save to session'''
        self.session['cart'] = self.cart
        self.session.modified = True
    
    def empty(self, request):
        '''delete session'''
        del self.session['cart'] 
        self.session.modified = True
        
def cart_items_update(user_cart,session_cart):
    '''update Cart database with cart session'''
    for item in session_cart:
        try:
            cart_item = CartItem.objects.get(cart=user_cart, product_id=item)
            cart_item.quantity = session_cart[item]
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=user_cart, product_id=item, quantity=session_cart[item])