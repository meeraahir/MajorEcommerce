from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET

from .models import *
from user.models import Confirm_order
from user.models import Place_to_order


# Create your views here.
def admin_dashboard(request):
    total_user = User.objects.filter(is_superuser=False).count()
    total_product = Add_Productmaster.objects.count()
    total_orders = Confirm_order.objects.count()

    context = {
        'total_user': total_user,
        'total_product': total_product,
        'total_orders': total_orders,
    }
    return render(request, 'admin/admin_dashboard.html', context)


def add_product(request, id=None):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }

    if request.method == 'POST':
        pname = request.POST.get('product_name')
        pdes = request.POST.get('product_description')
        price = request.POST.get('product_price')
        img = request.FILES.get('product_img')
        category_id = request.POST.get('product_category')

        # Ensure all required fields are provided
        if not all([pname, pdes, price, img, category_id]):
            context['error'] = "All fields are required."
            return render(request, 'admin/add_product.html', context)

        product_category = None
        if category_id:
            product_category = get_object_or_404(Category, id=category_id)

        try:
            product = Add_Productmaster.objects.create(
                product_name=pname,
                product_description=pdes,
                product_price=price,
                product_img=img,
                product_category=product_category
            )
            product.save()
            return redirect('ecommerce_admin_app:admin_dashboard')
        except IntegrityError as e:
            context['error'] = f"Error saving product: {e}"
            return render(request, 'admin/add_product.html', context)

    return render(request, 'admin/add_product.html', context)


def view_product(request):
    product = Add_Productmaster.objects.all()
    print(f"Products: {product}")
    context = {'product': product}
    return render(request, 'admin/view_product.html', context)


def base(request):
    return render(request, 'admin/base1.html')


def update_product(request, id):
    p = get_object_or_404(Add_Productmaster, id=id)
    if request.method == 'POST':
        pname = request.POST['product_name']
        pdes = request.POST.get('product_description', p.product_description)
        price = request.POST['product_price']
        img = request.FILES.get('product_img', p.product_img)
        category_id = request.POST.get('product_category')

        if category_id:

            category = get_object_or_404(Category, id=category_id)
        else:
            category = p.product_category

        p.product_name = pname
        p.product_description = pdes
        p.product_price = price
        p.product_img = img
        p.product_category = category
        p.save()
        return redirect('ecommerce_admin_app:view_product')
    return render(request, 'admin/update_product.html', {'p': p})


def delete(request, id):
    p = Add_Productmaster.objects.get(id=id)
    p.delete()
    return redirect('ecommerce_admin_app:view_product')


def add_category(request):
    if request.method == 'POST':
        name = request.POST['category_name']
        category = Category.objects.create(
            name=name
        )
        category.save()
        return redirect('ecommerce_admin_app:add_category')
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'admin/add_category.html', context)


def view_category(request):
    categories = Category.objects.all()
    print(categories)
    context = {'categories': categories}
    return render(request, 'admin/add_category.html', context)


def order_received(request):
    order_details = Confirm_order.objects.all()
    context = {
        'order_details': order_details
    }
    return render(request, 'admin/order_received.html', context)


def base2(request):
    return render(request, 'admin/base2.html')


def update_order_status(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = get_object_or_404(Place_to_order, id=order_id)
        order.status = status
        order.save()
        return redirect('ecommerce_admin_app:order_received')
