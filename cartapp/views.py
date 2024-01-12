from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from productsapp.models import Product
from cartapp.models import Cart,CartItem

def create_cartId(request):
    cart = request.session.session_key
    if not cart :
        cart=request.session.create()
    return cart

@login_required(login_url="/login")
def removeCart(request,product_id):
    cart=Cart.objects.get(cart_id=create_cartId(request),customer=request.user)
    product=Product.objects.get(pk=product_id)
    cartItem=CartItem.objects.get(product=product,cart=cart)#ສິນຄ້າທີ່ຕ້ອງການລົບ
    cartItem.delete()
    return redirect("/cart")

# Create your views here.
@login_required(login_url="/login")
def cart(request):
    counter=0
    total=0
    try:
        #ດຶງຂໍ້ມູນກະຕ່າສິນຄ້າ

        cart=Cart.objects.get(cart_id=create_cartId(request),customer=request.user)
        #ດຶງຂໍ້ມູນສິນຄ້າໃນກະຕ່າ
        cartItem=CartItem.objects.filter(cart=cart)
        for item in cartItem:
            counter+=item.quantity # 3, 1
            total+=(item.product.price * item.quantity) # 3x50 , 1x100
    except (Cart.DoesNotExist,CartItem.DoesNotExist): 
        cart=None 
        cartItem=None
    return render(request,"cart.html",{"cartItem":cartItem,"total":total,"counter":counter})

@login_required(login_url="/login")
def addCart(request,product_id):
    product=Product.objects.get(pk=product_id)
    #ສ້າງກະຕ່າສິນຄ້າ
    try:
        #ມີກະຕ່າສິນຄ້າ 
        cart=Cart.objects.get(cart_id=create_cartId(request))
    except Cart.DoesNotExist:
        #ບໍ່ມີກະຕ່າສິນຄ້າ
        cart=Cart.objects.create(
            cart_id=create_cartId(request),
            customer=request.user
        )
        cart.save()
    #ບັນທືກລາຍການສິນຄ້າໃນກະຕ່າ
    try:
        #ຊື້ສິນຄ້າອັນເກົ່າ
        cartitem=CartItem.objects.get(product=product,cart=cart)
        if cartitem.quantity<cartitem.product.stock:
            cartitem.quantity+=1
            cartitem.save()
    except CartItem.DoesNotExist:
        #ຊື້ສິນຄ້າ
        cartitem=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cartitem.save()
    return redirect("/cart")