from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("contactus/", views.contactus, name="contactus"),
    path("tracker", views.tracker, name="tracker"),
    path("productview/<int:myid>", views.productview, name="productview"),
    path("search/", views.search, name="search"),
    path("checkout/", views.checkout, name="checkout"),
]