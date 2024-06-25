from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from .models import product,CartItem,ProductVariation,inc
from .models import UserActivity
from .filters import ProductFilter
from .forms import SignUpForm ,order
from accounts .models import customer
from .models import gust,order as o
from .context_processors import items_count
from django.shortcuts import get_object_or_404
import datetime

def capture_user_activity(request):
    ip_address = request.META.get('REMOTE_ADDR')  # Get user's IP address
    phone_percentage = request.POST.get('phone_percentage')  # Example: if sent via a form
    # Ensure phone_percentage is an integer before saving
    
    # Create and save the UserActivity instance
    activity = UserActivity.objects.create(
        ip_address=ip_address,
        phone_percentage=phone_percentage,
    )
    
    # Optionally, you can now use 'activity' to perform additional tasks
    
    return render(request, 'some_template.html', {'activity': activity})




def get_arabic_day_name(date):
    arabic_days = {
        0: "الإثنين",
        1: "الثلاثاء",
        2: "الأربعاء",
        3: "الخميس",
        4: "الجمعة",
        5: "السبت",
        6: "الأحد"
    }
    return arabic_days[date.weekday()]

def get_expected_delivery_date():
    today = datetime.date.today()
    if today.weekday() == 4:  # Friday
        expected_date = today + datetime.timedelta(days=2)
    elif today.weekday() == 5:  # Saturday
        expected_date = today + datetime.timedelta(days=1)
    else:
        expected_date = today + datetime.timedelta(days=2)
    
    return get_arabic_day_name(expected_date)

#________________________________________________________________________________________________________________________________________________________
def checkout(requset):
    form = order()
    if requset.GET.get('number'):
        print (requset.GET.get('number'))
    if requset.method == "POST": 
        form = order(requset.POST)
        if form.is_valid():
            if requset.user.is_authenticated:
                form.instance.user = requset.user
                cart_items = CartItem.objects.filter(user=requset.user)
                print (cart_items)
                tn_mon_list = []
                for obj in cart_items:
                    tn_mon_list.append(str(obj))
                    form.instance.iteams = tn_mon_list
                    tn = []
                for obj in cart_items:
                 tn.append(str(obj))
                 form.save()
                 return redirect ("done")
            else:
                device = requset.COOKIES['device']
                form.instance.deuvice = device
                cart_items = CartItem.objects.filter(device=device)
                tn_mon_list = []
                for obj in cart_items:
                    tn_mon_list.append(str(obj))
                    form.instance.iteams = tn_mon_list
                    tn = []
                for obj in cart_items:
                    tn.append(str(obj))
                    form.save()
                    return redirect ("done")
        else:
            messages.error(requset,("please Enter a Valid informaion and Try again"))
            return redirect ("check")
            
    cart_items = ()
    if requset.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=requset.user)
    else:
         device = requset.COOKIES['device']
         cart_items = CartItem.objects.filter(device=device)

    r =  (item.quantity * item.product.discount for item in cart_items)
    total_price = sum(item.ProductVariation.discount * item.quantity for item in cart_items)
    return render (requset,"html/checkout.html",{'form':form , 'cart_items': cart_items, 'total_price': total_price,"totalr":r})
#________________________________________________________________________________________________________________________________________________________
def register_usr(requset):
    form = SignUpForm()
    if requset.method == "POST": 
        form = SignUpForm(requset.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate (username=username,password=password,)
            login(requset,user )
            messages.success(requset,"regstiration done succ")
            return redirect ("home")
        else:
            messages.error(requset,("please Enter a Valid informaion and Try again"))
            return redirect ("reg")
    else:
        return render (requset,"html/register.html",{"form":form})
#___________________________________________________________________________________

def catagory(requset):
    count = items_count(requset)
    a = ProductVariation.objects.filter(ava=True)
    f = ProductFilter(requset.GET, queryset=a)
    #s = product.objects.filter(name__icontains="tobakco")
    if requset.method == 'POST':
        search_query = requset.POST['search_query']
        return redirect('search',pk=search_query)
    context = {"filter":f,
               "p":a,
                'offer':count['offer'],     
               }
    return render (requset,"html/category.html",context)

#___________________________________________________________________________________
def search(requset,pk):
    if pk == "":
        return redirect ("home")
    f = product.objects.get(name__icontains=pk)
    ts = ProductVariation.objects.get(product=f,ava=True)
    print (ts)
    context = {"filterr":ts}
    return render (requset,"html/search.html",context)
#___________________________________________________________________________________
def producct(requst,pk):
    expected_delivery_date = get_expected_delivery_date()
    count = items_count(requst)
    prodcu = product.objects.get(id=pk)
    ts = ProductVariation.objects.get(product=prodcu,ava=True)
    pv = ProductVariation.objects.filter(product=prodcu)
    ch = ProductVariation.objects.filter(product=prodcu,ava=True)
    a = (ts.genders)
    ge=ProductVariation.objects.filter(genders=a,ava=True).exclude(id=pk)[:6]
    original_price = ts.price
    discounted_price = ts.discount
    def calculate_discount_percentage(original_price, discounted_price):
           discount_amount = original_price - discounted_price
           discount_rate = discount_amount / original_price
           discount_percentage = discount_rate * 100
           return discount_percentage
    discounted =  (calculate_discount_percentage(original_price, discounted_price))
    d = round(discounted)
    context= {
        'pk':prodcu,
        'rl':ge,
        'discount':d,
        "pv":pv,
        "ch":ch,
        'offer':count['offer'], 
        "d_days":expected_delivery_date,
    }
    return render(requst,"html/product.html",context)
#___________________________________________________________________________________
def index(requst):   
    ip_address = requst.META.get('REMOTE_ADDR')  # Get user's IP address
    phone_percentage = requst.POST.get('phone_percentage')  # Example: if sent via a form
    # Ensure phone_percentage is an integer before saving
    if phone_percentage == None:

        phone_percentage = 1
    # Create and save the UserActivity instance
        existing_activity = UserActivity.objects.filter(ip_address=ip_address).first()
        
        if existing_activity:
            # Handle the case where a record already exists with this IP address
            error_message = "This IP address already has an associated activity."
        else:
            activity = UserActivity.objects.create(
        ip_address=ip_address,
        phone_percentage=phone_percentage,
    )
    prodcu = ProductVariation.objects.filter(ava=True)[:4]
  
    activities = UserActivity.objects.all()
    return render(requst,"html/index.html",{'product':prodcu,
                                            'activities': activities
                                            })
#___________________________________________________________________________________
def login_usr(requst):
    if requst.method == "POST":
        username1 = requst.POST.get("username")
        password1 = requst.POST.get("password")
        user = authenticate(requst,username=username1,password=password1)
        if user is not None:
            login(requst,user)
            messages.success(requst,("You have been logged in ..."))
            return redirect("home")
        else:
            messages.success(requst,"خطا في الاسم او كلمة المرور ")
            return redirect("login")
    else:
       return render(requst,"html/login.html")
#___________________________________________________________________________________
def logout_usr(requst):
    logout(requst)
    #messages.success(requst,("You have been logged out ..."))
    return redirect ("home")
#___________________________________________________________________________________
def view_cart(request):
    cart_items = ()
    #device = request.COOKIES['device']
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        device = request.COOKIES['device']
        cart_items = (CartItem.objects.filter(device=device))
       
    total_price = sum(item.ProductVariation.discount * item.quantity for item in cart_items)
    return render(request, 'html/cart.html', {'cart_items': cart_items, 'total_price': total_price})
 #___________________________________________________________________________________
def add_to_cart(request):
   pk = request.GET.get('id')
   qty = 1
   if request.GET.get('qty'):
       qty = request.GET.get('qty')
   Product = ProductVariation.objects.get(id=pk)
   if request.user.is_authenticated:
       cart_item, created = CartItem.objects.get_or_create(ProductVariation=Product, user=request.user)
       cart_item.quantity += (int(qty))
       cart_item.save()
       count = items_count(request)
      # messages.success(request,'تم اضافة المنتج بنجاح')
       return JsonResponse ( {'items_count':count['items_count'],'offer':count['offer']})
       #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

   else :
         devive = request.COOKIES['device']
         costumer , create = customer.objects.get_or_create(device=devive)
         cart_item, created = CartItem.objects.get_or_create(ProductVariation=Product, device=devive)
         cart_item.quantity += (int(qty))
         cart_item.save()
         count = items_count(request)
         #messages.error(request,"من فضلك قم بتسجيل الدخول اولا")
         return JsonResponse ( {'items_count':count['items_count'],'offer':count['offer']})
#___________________________________________________________________________________
def remove_iteam(request):
    id = request.GET.get("id")
    count = items_count(request)
    Product = ProductVariation.objects.get(id=id)
    if request.user.is_authenticated:
         cart_item, created = CartItem.objects.get_or_create(ProductVariation=Product, user=request.user)
         if cart_item.quantity == 1:
            cart_item.delete()
            return JsonResponse ( {'items_count':cart_item.quantity,'offer':count['offer']})
         else:
          cart_item.quantity -= 1
          cart_item.save()
          return JsonResponse ( {'items_count':cart_item.quantity,'offer':count['offer']})
         
    else:
         device = request.COOKIES['device']
         cart_item, created = CartItem.objects.get_or_create(ProductVariation=Product, device=device)
         if cart_item.quantity == 1:
            cart_item.delete()
            return JsonResponse ( {'items_count':cart_item.quantity,'offer':count['offer']})
         else:
          cart_item.quantity -= 1
          cart_item.save()
          return JsonResponse ( {'items_count':cart_item.quantity,'offer':count['offer']})
#___________________________________________________________________________________

def add_iteam(request):
    count = items_count(request)
    if request.user.is_authenticated:
        id = request.GET.get("id")
        Product = ProductVariation.objects.get(id=id)
        cart_item, created = CartItem.objects.get_or_create(ProductVariation=Product, user=request.user)
        cart_item.quantity += 1 
        cart_item.save()
        return JsonResponse ( {'ittems_count':cart_item.quantity,'offer':count['offer']})
    
    else:
        device = request.COOKIES['device']
        id = request.GET.get("id")
        Product = ProductVariation.objects.get(id=id)
        cart_item, created = CartItem.objects.get_or_create(ProductVariation=Product, device=device)
        cart_item.quantity += 1 
        cart_item.save()
        return JsonResponse ( {'ittems_count':cart_item.quantity,'offer':count['offer']})
#___________________________________________________________________________________

def delete_cart_item(request):
  count = items_count(request)
  if request.method == 'GET':
        try:
            cart_item_id = request.GET.get('cart_item_id')
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            cart_item.delete()
            count = items_count(request)
            return JsonResponse({'success': True,'items_count':count['items_count'],'offer':count['offer']})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'CartItem does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
  else:
      return JsonResponse({'error': 'Invalid request method'}, status=405)
#___________________________________________________________________________________
def order_placed(request):
     return render(request,'html/order_placed.html')
def google(request):
    return HttpResponseRedirect("https://www.facebook.com/waled.diab.779/")
from django.http import JsonResponse

def innc(requset):
    if requset.GET.get("phone"):
        number = (int(requset.GET.get("phone")))
        inc.objects.create(phone=number)
        return JsonResponse ( {'items_count':number})
    
    else:
        return JsonResponse ( {'items_count':cart_item.quantity,'items_count':number})
#___________________________________________________________________________________
def checkrn(request,pk):
    prodcu = ProductVariation.objects.get(id=pk)
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(ProductVariation=prodcu, user=request.user)
        cart_item.quantity += 1 
        cart_item.save()
        return redirect ("check")
    else:
         device = request.COOKIES['device']
         cart_item, created = CartItem.objects.get_or_create(ProductVariation=prodcu, device=device)
         cart_item.quantity += 1 
         cart_item.save()
         return redirect ("check")
#___________________________________________________________________________________
def getprice(requset):
    if requset.GET.get("id"):
        id  = (requset.GET.get("id"))
        pv = ProductVariation.objects.get(id=id)
        price = pv.discount
        return JsonResponse ( {'price':price})
    
    else:
        return JsonResponse ( {'items_count':cart_item.quantity,'items_count':number})

#___________________________________________________________________________________
from .models import UserActivity

def capture_user_activity(request):
    ip_address = request.META.get('REMOTE_ADDR')  # Get user's IP address
    phone_percentage = request.POST.get('phone_percentage')  # Example: if sent via a form
    # Ensure phone_percentage is an integer before saving
    
    # Create and save the UserActivity instance
    activity = UserActivity.objects.create(
        ip_address=ip_address,
        phone_percentage=phone_percentage,
    )
    
    # Optionally, you can now use 'activity' to perform additional tasks
    
    return render(request, 'some_template.html', {'activity': activity})




def display_user_activity(request):
    activities = UserActivity.objects.all()
    return render(request, 'activity_list.html', {'activities': activities})