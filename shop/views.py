from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate, SlidesImgaes 
from math import ceil
import json
from paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test




# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = '###############'

@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def  login_check(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        user = authenticate(username=username, password=password)
        

        if user is not None:
            thank = False
            auth.login(request,user)
            return HttpResponseRedirect(reverse('index'))
            
        else:
            thank  = True
            return render(request,'shop/Login.html',{'thank':thank})
            # return render(request,'shop/Login.html',{'msg':'Incorrect Username/Password. Try Again!'})
             

        
    else:
        return render(request, 'shop/Login.html', {})




def registration(request):
   if request.method =='POST':
       username=request.POST['username']
       email=request.POST['email']
       psw=request.POST['psw']
       psw_repeat=request.POST['psw-repeat']
       username_check=User.objects.filter(username = username).exists()
       email_check=User.objects.filter(email = email).exists()
       if psw==psw_repeat:
           psw_check=False
       else:
           psw_check=True
     
       if username_check and email_check and psw_check:
           messages.info(request,"Password Doesn't match!")
           messages.info(request,'Username Taken!')
           messages.info(request,'E-mail Taken!')
           return render(request,'shop/registration.html')
       elif username_check and email_check:
           messages.info(request,'Username Taken!')
           messages.info(request,'E-mail Taken!')
           return render(request,'shop/registration.html')
       elif username_check and psw_check:
           messages.info(request,"Password Doesn't match!")
           messages.info(request,'Username Taken!')
           return render(request,'shop/registration.html')
       elif email_check and psw_check:
           messages.info(request,"Password Doesn't match!")
           messages.info(request,'E-mail Taken!')
           return render(request,'shop/registration.html')
       elif email_check:
            messages.info(request,'E-mail Taken!')
            return render(request,'shop/registration.html')
       elif username_check:
           messages.info(request,'UserName Taken')
           return render(request,'shop/registration.html')
          # return render(request,'Register.html',{'msgemail':' E-mail Taken!'})
       elif psw_check:
           messages.info(request,"Password Doesn't match!")
           return render(request,'shop/registration.html')
       else:
           user=User.objects.create_user(username=username,password=psw,email=email)
           user.save()
           return render(request,'shop/Login.html',{'s_msg':'Account Successfully Created!'}) 
       
   else:
      return render(request,'shop/registration.html')

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    Slidesimgaes = SlidesImgaes.objects.all()
    params = {'allProds':allProds , 'slidesimgaes':Slidesimgaes }

    
    
    
   




    return render(request, 'shop/index.html', params)




def searchMatch(query,item):
    "retrun true only query mathes items"
    "Here we are use lower bcz its convert caps to lower also."
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower() :
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query , item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:

            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds,'msg':""}
    
    if len(allProds) == 0  or len(query)<4:
        params = {'msg':"Please Make Sure To Enter Relevent search query"}

    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact1.html',{'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')
 

def prodView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})


# @login_required
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id =int(order.order_id)
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': '#############',
                # 'Username' : user_passes_test.username,
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': str(email),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        if User.is_authenticated :
        # <h2>Hello {{ user.username }}</h2>
            return render(request, 'shop/paytm.html', {'param_dict': param_dict})
        else: 
            # <h2>Register or Login if you'd like to</h2>
            print("Plx erigiter or login")
        
        
        
    return render(request, 'shop/checkout.html')

 
# @login_required 
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})  
    















    
