
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),    
    path('ViewCakes/<cid>',views.viewCakes),
    path('ViewDetails/<id>',views.ViewDetails),
    path('login',views.login),    
    path('register',views.register),
    path('logout',views.logout),   
    path('cart',views.showAllCartItems),
    path('makepayment',views.makepayment),
    path('MyOrders',views.MyOrders),
]
