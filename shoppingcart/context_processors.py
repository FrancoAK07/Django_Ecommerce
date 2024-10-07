from .shoppingcart import ShoppingCart

def shoppingcart(request):
    return {"shoppingcart": ShoppingCart(request)}