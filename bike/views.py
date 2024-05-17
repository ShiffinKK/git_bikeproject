import razorpay
from django.shortcuts import render,redirect
from django.views.generic import View
from bike.form import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from bike.models import Bike,WishlistItem,Service,Order,Category,PriceRange
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from bike.decorators import signin_required
from django.views.decorators.csrf import csrf_exempt

KEY_ID="rzp_test_zZEPSidnmoQj3D"
KEY_SECRET="nuad5JpBkJGAFMNDhrCeryo7"

@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):  
   def post(self,request,*args,**kwargs):
      client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
      data=request.POST
      print("hgfhgfjghjgjj====",data)
     
      try:
         client.utility.verify_payment_signature(data)
         print(data)
         order_obj=Order.objects.get(order_id=data.get("razorpay_order_id"))
         order_obj.is_paid=True
         order_obj.save()
         print("******Transaction completed*****")
        

      except:
         print("!!!!!!!Transaction Failed!!!")
      
      return render(request,"sucess2.html")



class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect("signin")
        else:
           return render(request,"login.html",{"form":form})
        

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
          u_name=form.cleaned_data.get("username")
          pwd=form.cleaned_data.get("password")
          user_object=authenticate(request,username=u_name,password=pwd)
          if user_object:
              login(request,user_object)
              return redirect("all")
        messages.error(request,"invalid credentials")
        return render(request,"login.html",{"form":form})

   
class StartWebView(View):
    def get(self,request,*args,**kwargs):
        return render (request,"start.html")


@method_decorator(signin_required,name="dispatch")
class ListView(View):
    def get(self,request,*args,**kwargs):
        print("dfxcghbknlmrzsdfcghbjkmlfd")
        if not request.user.is_authenticated:
            return redirect("signin")
        print(request.user.is_authenticated)
        qs=Bike.objects.filter(is_placed=False)
        categories=Category.objects.all()
        selected_category=request.GET.get("category")
        if selected_category:
          qs=qs.filter(category_object__name=selected_category)
        
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            qs=qs.filter(price__gte=min_price)
        if max_price:
            qs=qs.filter(price__lte=max_price)

        #tags=PriceRange.objects.all()
        
        return render (request,"all.html",{"data":qs,"categories":categories})
    

    
    

    
@method_decorator([signin_required,never_cache],name="dispatch")
class BikeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Bike.objects.get(id=id)
        return render(request,"bike_detail.html",{"data":qs})
@method_decorator([signin_required,never_cache],name="dispatch")
   
class AddToWishListView(View):
    def post(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")

        bike_obj=Bike.objects.get(id=id)
        WishlistItem.objects.create(
        
          
          Bike_object=bike_obj,
          Cart_object=request.user.wish

        )
        return redirect("all")
    
@method_decorator([signin_required,never_cache],name="dispatch")    
class WishListItemView(View):
        def get(self,request,*args,**kwargs):
            qs=request.user.wish.wishitem.filter(is_order_placed=False)
            return render(request,"compare_list.html",{"data":qs})

@method_decorator([signin_required,never_cache],name="dispatch")
class ServiceListView(View):
      def get(self,request,*args,**kwargs):
         qs=Service.objects.filter(owner=request.user)
         return render (request,"service.html",{"data":qs})
         
@method_decorator([signin_required,never_cache],name="dispatch")
class CompareItemRemoveView(View):
   def get(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      Wish_item_object=WishlistItem.objects.get(id=id)
      Wish_item_object.delete()
      return redirect("wish-list")
   
@method_decorator([signin_required,never_cache],name="dispatch")
class CheckOutView(View):
   
   
    def get(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      qs=Bike.objects.get(id=id)
      return render(request,"checkout.html" ,{"data":qs})
    
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
      if payment_method=="online" and order_create:
          
          client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
          data = { "amount":total*100, "currency": "INR", "receipt": "order_rcptid_11" }
          payment = client.order.create(data=data)
          order_create.order_id=payment.get("id")
          order_create.save()
          
          print("payment initiate",payment)
          context={
             "key":KEY_ID,
             "order_id":payment.get("id"),
             "amount":payment.get("amount")
          }
          print(context)
          return render(request,"payment.html",{"context":context})
        
      return redirect("sucess")
    
@method_decorator([signin_required,never_cache],name="dispatch")
class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):
         qs=Order.objects.filter(user_object=request.user).exclude(status="cancelled")
         return render(request,"order_summary.html",{"data":qs})

class SignOutView(View):


   def get(self,request,*args,**kwargs):
      logout(request)
      return redirect("start")
   
class SucessView(View):
   def get(self,request,*args,**kwargs):
       return render(request,"sucess.html")
   
class OrderItemRemoveView(View):
    def get(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       order_objk=Order.objects.get(id=id)
       bike_obj=order_objk.Bike_object
       bike_obj.is_placed=False
       bike_obj.save()
       Order.objects.get(id=id).delete()
       return redirect("summary")
       
    
class WhyUsView(View):
   def get(self,request,*args,**kwargs):
       return render(request,"why.html")



