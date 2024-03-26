from models.user import User, CartItem

def addToCart(user_id, batch_id, volume):

    #Get user
    user = User.objects.with_id(user_id)

    if(user is None):
        return 1 #Invalid user
    
    cart_entry = CartItem(batch_id=batch_id, volume=volume)

    user.cart.append(cart_entry)

    user.save()

    return 0
    

    

