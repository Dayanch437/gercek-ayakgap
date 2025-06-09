from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('pending-orders/', views.get_pending_orders, name='pending_orders'),
    # path('api/orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('<int:order_id>/details/',views.order_details,name='order_details'),

    path('deliver_order/',views.deliver_order,name='deliver_order'),

    path('dashboard/',views.dashboard,name='dashboard'),

]