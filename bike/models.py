from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Bike(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(null=True)
    image=models.ImageField(upload_to="bike_images",default="default.jpg",null=True,blank=True)
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="item")
    Model_year=models.PositiveIntegerField()
    price=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    km=models.PositiveBigIntegerField()
    is_placed=models.BooleanField(default=False)
    
      
    def __str__(self):
        return self.title
    
class Wishlist(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property
    def wish_item(self):
        return self.cartitem.filter(is_order_placed=False)
    
   

    
    @property
    def recoment(self):
        #bike_price=self.wish_item
        #for i in bike_price:
        resilt=([i.item_total for i in self.wish_item])
        #return resilt
        result=[]
        
        for i in resilt:
            result.append(i)
        result.sort()
        for i in self.wish_item:
            if i.item_total==result[0]:
                rec_bike=i.item_title
        return (f"recoments {rec_bike}")

   
     

class WishlistItem(models.Model):
    Bike_object=models.ForeignKey(Bike,on_delete=models.CASCADE)
    Cart_object=models.ForeignKey(Wishlist,on_delete=models.CASCADE,related_name="cartitem")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_order_placed=models.BooleanField(default=False)

    @property
    def item_total(self):
        return self.Bike_object.price
    @property
    def item_title(self):
        return self.Bike_object.title
    

class Order(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    Bike_object=models.ForeignKey(Bike,on_delete=models.CASCADE,related_name="bike")
    delivery_address=models.CharField(max_length=200)
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=200,null=True)
    is_paid=models.BooleanField(default=False)
    total=models.PositiveIntegerField()
    order_id=models.CharField(max_length=200,null=True)
    options=(
        ("cod","cod"),
        ("online","online")
    )
    payment=models.CharField(max_length=200,choices=options,default="cod")
    option=(
        ("order-placed","order-placed"),
        ("intransit","intransit"),
        ("dispatched","dispatched"),
        ("delivered","delivered"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=option,default="order-placed")
     
    @property
    def orderstatus(self):
        if self.status=="order-placed":
            placed=True
            return placed
    @property
    def orderstatus1(self):
        if self.status=="intransit":
            shipped=True
            return shipped
        

class PriceRange(models.Model):
    range=models.PositiveIntegerField()
   

   
 
          
        
       

   



class Service(models.Model):
    name=models.CharField(max_length=200)
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="repair")
    date=models.DateTimeField()
    description=models.CharField(max_length=200)
    serviced=models.BooleanField(default=False)
    comment=models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.name
    @property
    def status(self):
        if self.serviced==True:
            return "Completed"
        else:
            return "pending"
        



def create_Wishlist(sender,instance,created,**kwargs):
    if created:
        Wishlist.objects.create(owner=instance)
post_save.connect(create_Wishlist,sender=User)
