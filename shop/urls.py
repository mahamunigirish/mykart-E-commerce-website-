

from django.urls import path
app_name = 'shop'
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.prodView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("handlerequest/", views.handlerequest, name="handlerequest"),
    path("registration/",views.registration,name='registration'),
    path("Login/",views.login_check,name='Login'),
    path("logout",views.user_logout , name="logout"),
    # pat(r'^special/',views.special,name='special'),
    
    
    # path('logout/', views.user_logout, name='logout'),
    
    
]
