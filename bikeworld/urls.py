"""
URL configuration for bikeworld project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bike import views
from django.conf.urls.static import static
from django.conf import settings
from bike import BikeApi
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/',views.SignUpView.as_view(),name="signup"),
    path('signin/',views.SignInView.as_view(),name="signin"),
    path('all/',views.ListView.as_view(),name="all"),
    path('',views.StartWebView.as_view(),name="start"),
    path("detail/<int:pk>/",views.BikeDetailView.as_view(),name="bike-detail"),
    path('bike/<int:pk>/add_to_compare/',views.AddToWishListView.as_view(),name="addto-Wish"),
    path('compare/items/all/',views.WishListItemView.as_view(),name="wish-list"),
    path('service/',views.ServiceListView.as_view(),name="service"),
    path('wish/items/<int:pk>/remove/',views.CompareItemRemoveView.as_view(),name="remove"),
    path('checkout/<int:pk>/',views.CheckOutView.as_view(),name="checkout"),
    path('order/summary/',views.OrderSummaryView.as_view(),name="summary"),
    path('signout/',views.SignOutView.as_view(),name="signout"),
    path('sucess/',views.SucessView.as_view(),name="sucess"),
    path('why/',views.WhyUsView.as_view(),name="why"),

    path('ordetitem/<int:pk>remove/',views.OrderItemRemoveView.as_view(),name="item-delete"),
    path('payment/verification/',views.PaymentVerificationView.as_view(),name="verification"),

    path("api/v1/register/",BikeApi.SignUpView.as_view()),
    path('api/v1/token/',ObtainAuthToken.as_view()),
    path("api/all/",BikeApi.ProductListview.as_view()),
    path('api/v1/Bike/<int:pk>/',BikeApi.ProductDetailView.as_view()),
    path("api/v1/addcompare/<int:pk>/",BikeApi.AddTOCompare.as_view()),
    path("api/v1/comparelist/",BikeApi.CompareListView.as_view()) ,
    path("api/v1/compareitem/remove/<int:pk>",BikeApi.CompareItemRemoveView.as_view()),
    path("api/v1/servicelist/",BikeApi.ServiceListView.as_view()),
    path('api/v1/order/<int:pk>',BikeApi.CheckOutView.as_view()),
    path('api/v1/order/summary/',BikeApi.OrderSummaryView.as_view()),
    path('api/v1/order/remove/<int:pk>',BikeApi.OrderRemoveView.as_view())


    










]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

