from django.urls import path

from .import views

urlpatterns = [

    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('product/',views.product,name='product'),
    path('single-product/<int:product_id>/',views.single_product,name='single-product'),
    path('login/',views.user_login,name='login'),
    path('registration/',views.signUp,name='registration'),
    path('logout/',views.logout,name='logout'),
    path('base/',views.base,name='base'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.view_cart,name='view_cart'),
    path('remove_from_cart/<int:id>/',views.remove_from_cart,name='remove_from_cart'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('add_wishlist/<int:id>/',views.add_wishlist,name='add_wishlist'),
    path('delete_wishlist/<int:id>/', views.delete_wishlist, name='delete_wishlist'),
    path('view_wishlist/',views.view_wishlist,name='view_wishlist'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('place_to_order/',views.place_to_order,name='place_to_order'),
    path('confirm_order/',views.confirm_order,name='confirm_order'),
    path('my_order/',views.my_order,name='my_order'),
    path('change_password/',views.change_password,name='change_password'),
    path('change_profile/',views.change_profile,name='change_profile'),

]