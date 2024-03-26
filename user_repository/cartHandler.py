from models.user import User, CartItem

def addToCart(user_id, batch_id, volume):

    #Get user
    user = User.objects.with_id(user_id)

    if(user is None):
        return 1 #Invalid user
    
    current_cart_item = filter(lambda o : o.batch_id == batch_id, user.cart)

    current_cart_item = list(current_cart_item)

    if(len(current_cart_item) == 0):
        #Item not in cart yet
        cart_entry = CartItem(batch_id=batch_id, volume=volume)
        user.cart.append(cart_entry)
    else:
        #Item already in cart, increase volume
        item = current_cart_item[0]
        cart_entry = CartItem(batch_id=batch_id, volume=volume + item.volume)
        user.cart.remove(item)
        user.cart.append(cart_entry)
    
    user.save()

    return 0

def removeFromCart(user_id, batch_id):

    #Get user
    user = User.objects.with_id(user_id)
    
    if(user is None):
        return 1 #Invalid user
    
    if(batch_id==0):
        #Delete whole cart
        user.cart = []
        user.save()
        return 0
    else:

        current_cart_item = filter(lambda o : o.batch_id == batch_id, user.cart)
        current_cart_item = list(current_cart_item)

        if(len(current_cart_item) == 0):
            #Item not in cart
            return 2
        else:
            #Item is in cart, delete it
            item = current_cart_item[0]
            user.cart.remove(item)
            user.save()
            return 0



    

    

