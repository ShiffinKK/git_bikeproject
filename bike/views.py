from django.shortcuts import render,redirect
from django.views.generic import View
from bike.form import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from bike.models import Bike,WishlistItem,Service,Order
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from bike.decorators import signin_required





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
        qs=Bike.objects.all()
        return render (request,"all.html",{"data":qs})
    
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
          Cart_object=request.user.cart

        )
        return redirect("all")
    
@method_decorator([signin_required,never_cache],name="dispatch")    
class WishListItemView(View):
        def get(self,request,*args,**kwargs):
            qs=request.user.cart.cartitem.filter(is_order_placed=False)
            return render(request,"compare_list.html",{"data":qs})

@method_decorator([signin_required,never_cache],name="dispatch")
class ServiceListView(View):
      def get(self,request,*args,**kwargs):
         qs=Service.objects.all()
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
      id=kwargs.get("pk")
      Bike_object_obj=Bike.objects.get(id=id)
      total=Bike_object_obj.price
      Order.objects.create(
         user_object=request.user,
         delivery_address=address,
         phone=phone,
         email=email,
         Bike_object=Bike_object_obj,
         total=total
          )
      return redirect("sucess")
    
@method_decorator([signin_required,never_cache],name="dispatch")
class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):
         qs=Order.objects.filter(user_object=request.user).exclude(status="cancelled")
         return render(request,"order_summary.html",{"data":qs})

class SignOutView(View):


   def get(self,request,*args,**kwargs):
      logout(request)
      return redirect("signin")
   
class SucessView(View):
   def get(self,request,*args,**kwargs):
       return render(request,"sucess.html")
   
class OrderItemRemoveView(View):
    def get(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       Order.objects.get(id=id).delete()
       return redirect("summary")
    
class WhyUsView(View):
   def get(self,request,*args,**kwargs):
       return render(request,"why.html")



   