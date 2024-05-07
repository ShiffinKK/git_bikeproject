from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from bike.models import Bike,WishlistItem,Service,Order
from bike.serializers import ProductSerializer
from bike.serializers import UserSerializer,CompareSerializer,ServiceSerializer,CompareItemSerializer,OrderSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions,authentication
from rest_framework.response import Response

class SignUpView(CreateAPIView):
   serializer_class=UserSerializer
   queryset=User.objects.all() 

class ProductListview(ListAPIView):
    serializer_class=ProductSerializer
    queryset=Bike.objects.all()

class ProductDetailView(RetrieveAPIView):
    serializer_class=ProductSerializer
    queryset=Bike.objects.all()

class AddTOCompare(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Bike_obj=Bike.objects.get(id=id)
        compare_obj=request.user.cart
        WishlistItem.objects.create(
            Bike_object=Bike_obj,
            Cart_object=compare_obj
        )
        return Response(data={"message":"created"})

class CompareListView(APIView):
       authentication_classes=[authentication.TokenAuthentication]
       permission_classes=[permissions.IsAuthenticated]
       def get(self,request,*args,**kwargs):
           qs=request.user.cart
           serializer_instance=CompareSerializer(qs)
           return Response(data=serializer_instance.data)
       
       
class CompareItemRemoveView(DestroyAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CompareItemSerializer
    queryset=WishlistItem.objects.all()

class ServiceListView(ListAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ServiceSerializer
    queryset=Service.objects.all()
    def get_queryset(self):
        return Service.objects.filter(owner=self.request.user)
    
class CheckOutView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,*args,**kwargs):
      
      email=request.POST.get("email")
      phone=request.POST.get("phone")
      address=request.POST.get("address")
      payment_method=request.POST.get("payment")
      id=kwargs.get("pk")
      Bike_object_obj=Bike.objects.get(id=id)
      total=Bike_object_obj.price

      order_create=Order.objects.create(
         user_object=request.user,
         delivery_address=address,
         phone=phone,
         email=email,
         Bike_object=Bike_object_obj,
         total=total,
         payment=payment_method
          )
      Bike_object_obj.is_placed=True
      Bike_object_obj.save()
      if payment_method=="cod":
          order_create.save()
          return Response(data={"message":"created"})
      
class OrderSummaryView(ListAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OrderSerializer
    queryset=Order.objects.all()
    def get_queryset(self):
       return Order.objects.filter(user_object=self.request.user)
    
class OrderRemoveView(DestroyAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OrderSerializer
    queryset=Order.objects.all()
      



          
      

    

       