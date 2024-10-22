from collections import defaultdict

from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.paginator import Paginator
from django.http import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from ecommerce import settings
from .models import *


from product_admin.models import Add_Productmaster

from product_admin.models import Category


# from product_admin.models import Add_Product


# Create your views here.
def index(request):
    categories=Category.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Add_Productmaster.objects.filter(product_category=categoryID).order_by('-id')
        selected_category=Category.objects.get(id=categoryID)
    else:
        products = None
        selected_category= None

    products_by_category = {}
    for category in categories:
        products_by_category[category] = Add_Productmaster.objects.filter(product_category=category)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'products_by_category': products_by_category,
        'products':products,

    }
    return render(request,'user/index.html',context)


def about(request):
    return render(request,'user/about.html')


def contact(request):
    return render(request,'user/contact.html')


def product(request):
    products=Add_Productmaster.objects.all()
    paginator=Paginator(products,9)

    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={'page_obj':page_obj}
    return render(request,'user/products.html',context)


def single_product(request,product_id):
    product=get_object_or_404(Add_Productmaster, id=product_id)
    context={'product':product}
    return render(request,'user/single-product.html',context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = authenticate(username=username, password=password)
        if user_obj is None:
            print("Authentication failed")
            messages.info(request, 'Invalid username or password. Please try again.')
            return redirect('login')

        auth_login(request, user_obj)

        if user_obj.is_superuser:
            return redirect('ecommerce_admin_app:admin_dashboard')
        else:
            return redirect('index')
    return render(request,'login.html')


def signUp(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        pno = request.POST['phoneNo']
        city = request.POST['city']
        state = request.POST['state']
        password = request.POST['password']
        cpassword = request.POST['confirm_password']

        # Email and username validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('registration')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters.")
            return redirect('registration')

        if password != cpassword:
            messages.error(request, "Passwords didn't match.")
            return redirect('registration')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
            return redirect('registration')

        # Creating the user
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()

        # Creating the user profile
        user_profile = UserProfile(user=myuser, phoneNo=pno, city=city, state=state)
        user_profile.save()

        messages.success(request,
                         "Your account has been successfully created")
        return redirect('login')
    return render(request,'user/registration.html')


def logout(request):
    auth_logout(request)
    return redirect('index')


def base(request):
    return render(request,'user/base.html')

@login_required(login_url='/login/')
def add_to_cart(request, id):
    product = get_object_or_404(Add_Productmaster, id=id)
    user = request.user

    cart_item, created = Add_to_cart.objects.get_or_create(
        user=user,
        addProduct=product,
        defaults={'product_quantity': 1, 'total_price': product.product_price}
    )
    if created:
        messages.success(request, f'{product.product_name} was added to your cart.')
    else:
        cart_item.product_quantity += 1
        cart_item.save()
        messages.success(request, f'{product.product_name} quantity was updated in your cart.')

    return redirect('view_cart')

@login_required
def view_cart(request):
    user = request.user
    cart_items = Add_to_cart.objects.filter(user=user)

    for item in cart_items:
        item.item_total = item.product_quantity * item.addProduct.product_price


    total_price = sum(item.item_total for item in cart_items)

    return render(request, 'user/cart.html', {'total_price': total_price, 'cart_items': cart_items})

@login_required
def remove_from_cart(request,id):
    if request.method == 'POST':
     cart_item=get_object_or_404(Add_to_cart,id=id)
     cart_item.delete()
     messages.success(request,'Item Remove From Cart Successfully')
    return redirect('view_cart')

@login_required
def wishlist(request):
    wishlist_items=Wishlist.objects.filter(user=request.user)
    context={'wishlist_item':wishlist_items,
     }
    return render(request,'user/wishlist.html',context)

@login_required(login_url='/login/')
def add_wishlist(request,id):
    product=get_object_or_404(Add_Productmaster,id=id)
    wishlist , created = Wishlist.objects.get_or_create(user=request.user,product=product)
    if created:
        pass
    messages.success(request,'Item Add in Wishlist Successfully')
    return redirect('wishlist')

@login_required
def delete_wishlist(request,id):
    wishlist_item = get_object_or_404(Wishlist, id=id)
    if request.method == 'POST':
        wishlist_item.delete()

    messages.success(request,'Item Remove From Wishlist Successfully')
    return redirect('wishlist')


def view_wishlist(request):
    wishlist_item = Wishlist.objects.all()
    context = {
        'wishlist_item': wishlist_item
    }
    return render(request, 'user/wishlist.html', context)

@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(Add_to_cart, id=item_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            item.product_quantity += 1
        elif action == 'decrease' and item.product_quantity > 1:
            item.product_quantity -= 1
        item.save()
    return redirect('view_cart')


@login_required(login_url='/login/')
def place_to_order(request):
    user = request.user
    cart_items = Add_to_cart.objects.filter(user=user)
    grand_total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        payment_option = request.POST.get('payment_option')

        if not (name and address and city and state and pincode and payment_option):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'user/place_to_order.html', {'cart_items': cart_items, 'grand_total': grand_total})

        try:

            order = Place_to_order.objects.create(
                user=user,
                name=name,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                payment_option=payment_option
            )

            # Debugging: Print the order ID
            print(f"Order ID: {order.id}")



            for cart_item in cart_items:
                confirm_order = Confirm_order.objects.create(
                    product=cart_item.addProduct,
                    user=user,
                    placeorder=order,  # Reusing the same order instance
                    final_total_price=cart_item.total_price,
                    quantity=cart_item.product_quantity
                )


                print(f"Confirm Order ID: {confirm_order.id}, Linked Order ID: {confirm_order.placeorder.id}")

            cart_items.delete()

            messages.success(request, 'Product ordered successfully!')
            return redirect('confirm_order')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'user/place_to_order.html', {'cart_items': cart_items, 'grand_total': grand_total})

    return render(request, 'user/place_to_order.html', {'cart_items': cart_items, 'grand_total': grand_total})


def confirm_order(request):
    return render(request,'user/confirm_order.html')

@login_required(login_url='/login/')
def my_order(request):
    orders=Confirm_order.objects.filter(user=request.user).order_by('-created_at')
    orders_by_date = defaultdict(list)
    for order in orders:
        date = order.created_at.date()
        orders_by_date[date].append(order)
    context={
        'orders_by_date':dict(orders_by_date)
    }
    return render(request,'user/my_order.html',context)


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        old_password=request.POST['old_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        user=request.user

        if not user.check_password(old_password):
            messages.error(request,'old password is incorrect')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request,'New password do not match')
            return redirect('change_password')

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request,user)
        messages.success(request,'Your password has been successfully changed.')
        return redirect('change_password')


    return render(request,'user/change_password.html')

@login_required
def change_profile(request):
    user=request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':

        fname = request.POST.get('first_name', user.first_name)
        lname = request.POST.get('last_name', user.last_name)
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        pno = request.POST.get('phoneNo', UserProfile.phoneNo if profile else '')
        city = request.POST.get('city', UserProfile.city if profile else '')
        state = request.POST.get('state', UserProfile.state if profile else '')

        user.first_name = fname
        user.last_name = lname
        user.username = username
        user.email = email
        user.save()

        if profile:

            profile.phone_number = pno
            profile.city = city
            profile.state = state
            profile.save()
        else:

            UserProfile.objects.create(
                user=user,
                phone_number=pno,
                city=city,
                state=state
            )

        messages.success(request, 'Profile updated successfully')
        return redirect('change_profile')

    return render(request, 'user/change_profile.html', {
        'profile': profile,
        'user': user
    })