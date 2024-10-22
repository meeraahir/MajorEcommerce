from django.urls import path
from . import views

app_name='ecommerce_admin_app'
urlpatterns = [
      path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
      path('add_category/', views.add_category, name='add_category'),
      path('add_product/',views.add_product,name='add_product'),
      path('view_category/',views.view_category,name='view_category'),
      path('base1/',views.base,name='base1'),
      path('view_product/',views.view_product,name='view_product'),
      path('update_product/<int:id>/',views.update_product,name='update_product'),
      path('delete/<int:id>/',views.delete,name='delete'),
      path('order_received/',views.order_received,name='order_received'),
      path('base2/',views.base2,name='base2'),
      path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),

]