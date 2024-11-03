from datetime import datetime
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
import razorpay
from .models import Person,Menutbl,Category,Subcategory,Cart,Table_Details,Order,TableReservation,Options,Customization,Reserved_Tables_Details,Selected_customization
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse

from django.core.mail import send_mail
from django.conf import settings


from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone
# from background_task import background
# from django.conf.urls.defaults import url, include, handler404, handler500
# from django.urls import include


# from background_task import background
# from django.conf.urls.defaults import url, include, handler404, handler500

# Create your views here.
def index(request):
    return render(request,'index.html')
def menu(request):
    return render(request,'menu.html')



#@cache_control(no_cash=True,must_validate=True,no_store=True)
def loginpage(request):
    if 'username' in request.session:
        # p=User.objects.get(username='username')
        # pers=Person.objects.get(user_id=p)
        # if(pers.role_id.role_id==1):
        #     return redirect('chome')
        # if(pers.role_id.role_id==2):
        #     return redirect('staffhome')
        # if(pers.role_id.role_id==3):
        #     return redirect('adminhome')
        # print("withemailenter")
        #return render(request,'chome')
        return redirect('chome')
        #return render(request,'chome.html')
    if request.method == 'POST':
        email=request.POST['username']
        password= request.POST['password']
        #user=User.objects.get(email=email)
        #pa=User.objects.get(email_address=email)
        #if pa is not None:
            #user=authenticate(request,email_address=pa.email_address,password=password)
        
        # p=Person.objects.get(email=email)
        p=Person.objects.filter(email=email).exists()
        if p is False:
            messages.error(request,"Invalid Username or password")
            return redirect('loginpage')
        p=Person.objects.get(email=email)
        user=authenticate(request,username=p.name,password=password)
        #p=Person.objects.get(email=email)
        #employee = Employee.objects.get(id=id) 
        #employee = Employee.objects.all() 
        #context["data"] = GeeksModel.objects.get(id = id)
        if user is not None:
            request.session['username']=p.name
            request.session.save()
            if (p.role_id==1):
                login(request, user)
                # subcategory=Subcategory.objects.all()
                # category=Category.objects.all()
                # menu=Menutbl.objects.all()
                #return render(request,'chome.html')
                return redirect('chome')
                #return render(request,'chome.html',{'subcategory':subcategory,'category':category,'menu':menu})
            elif(p.role_id==2):
                login(request, user)
                # return render(request,'staffhome.html')
                return redirect('staffhome')
            elif(p.role_id==3):
                login(request, user)
                return render(request,'adminhome.html')
            else:
                return redirect('chome')
                #return render(request,'chome.html')
        else:
            messages.error(request,"Invalid Username or password")
            return redirect('loginpage')
    else:
        return render(request,'loginpage.html')
    
def signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        #role=request.POST.get('category')
        password=request.POST.get('password')
        #print(username)
        if User.objects.filter(username=username).exists():
            messages.info(request,"User already exists")
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"email taken")
            return redirect('signup')
        elif username != '' and email != '' and phone != '' and password != '':
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save();
            data=Person(user_id=user,name=username,email=email,phone=phone,role_id=1,address=address,password=password)
            data.save()
            messages.info(request,"Successfully registered")
            #data2=Users(USERNAME=username,Email address=email)
            return redirect('loginpage')
        else:
            messages.info(request,"Error occur")
            return redirect('signup')
    else:
        return render(request,'signup.html')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def chome(request):
    #category=Category.objects.filter(status=1)
    if 'username' in request.session:
        subcategory=Subcategory.objects.all()
        category=Category.objects.all()
        menu=Menutbl.objects.all()
        return render(request,'chome.html',{'subcategory':subcategory,'category':category,'menu':menu})
    else :
        return redirect('loginpage')


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def staffhome(request):
    if 'username' in request.session:
        return render(request,'staffhome.html')
    return redirect('loginpage')

    



# def logout_user(request):
#     # if 'username' in request.session:
#     #     #session.objects.all().delete()
#     #     logout(request)
#     #     request.session.flush()
#     #     request.session.clear()
#     #     #del request.session['username']
#     #     return redirect('loginpage')
#     #     #return render(request,'loginpage.html')
#     #     #return render(request,'logout_user.html')
#     logout(request)
#     request.session.flush()
#     request.session.clear()
#     return render(request,'logout_user.html')


#from django.contrib.auth import logout

def logout_user(request):
    if request.user.is_authenticated:
        # Log the user out
        logout(request)
        # Clear the session
        request.session.flush()
        request.session.clear()
        #del request.session['username']
        #return render(request,'loginpage.html')
        return redirect('loginpage')
    else:
        logout(request)
        request.session.flush()
        # Handle the case where the user is not authenticated
        return render(request,'logout_user.html')




    #logout(request)
    #return HttpResponseRedirect(reverse('loginpage'))
    #return render(request,'loginpage.html')
    
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def adminhome(request):
    if 'username' in request.session:
        salads=Menutbl.objects.filter(pk=1)
        pizza=Menutbl.objects.filter(pk=2)
        burger=Menutbl.objects.filter(pk=3)
        return render(request,'adminhome.html',{"salads":salads,"pizza":pizza,"burger":burger})
    return redirect(loginpage)



#def customerprofile(request,):
    #user_profile = get_object_or_404(Person, username=username)
    #return render(request,'customerprofile.html')
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_add_person(request,):
    #user_profile = get_object_or_404(Person, user__name=username)
    #return render(request,'a_add_person.html')

    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        #role=request.POST.get('category')
        password=request.POST.get('password')
        #print(username)
        if User.objects.filter(username=username).exists():
            messages.info(request,"User already exists")
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"email taken")
            return redirect('signup')
        elif username != '' and email != '' and phone != '' and password != '':
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save();
            data=Person(name=username,email=email,phone=phone,role_id=2,address=address,password=password)
            data.save()
            print("data saved")
            messages.info(request,"Saved")
            #data2=Users(USERNAME=username,Email address=email)
            return render(request,'adminhome.html')
    else:
        return render(request,'a_add_person.html')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_view_person(request):
    person=Person.objects.all()
    return render(request,'a_view_person.html',{"person":person})


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def customerprofile(request):

    user_profile = Person.objects.get(name=request.user)
    if user_profile is None:
        return redirect('loginpage')
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        #role=request.POST.get('category')
        #password=request.POST.get('password')
        #print(username)
        if username != '' and email != '' and phone != '':
            user_profile.name=username
            user_profile.phone=phone
            user_profile.address=address
            user_profile.email=email
            #user_profile.save()
            Person.objects.filter(pk=user_profile.pk).update(address=address,phone=phone)
            #data2=Users(USERNAME=username,Email address=email)
            messages.success(request,"Changes are saved successfully !")
            
            return redirect('customerprofile')
        else:
            messages.error(request,"Updation failed !")
    else: 
        return render(request, 'customerprofile.html', {'user_profile': user_profile})
    


def changepassword(request):
    user_profile = Person.objects.get(name=request.user)
    u=User.objects.get(username=user_profile)
    if request.method == 'POST':
        password=request.POST.get('password')
        #print(username)
        if password != '':
            user_profile.password=password
            u.password=password
            u.save()
            user_profile.save()
            #data2=Users(USERNAME=username,Email address=email)
            messages.info(request,"Password Changed")
            
            return redirect('chome')
    else:
        
        return render(request, 'changepassword.html', {'user_profile': user_profile})
    


def delete_user(request,pk):
    
    if pk!=3:
        #records_to_delete = Person.objects.filter(pk=pk)
        # Delete the records that match the criteria
        #records_to_delete.delete()
        messages.success(request,"Changes are saved successfully !")
            
    return redirect('a_view_person')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_add_items(request):
    if request.method == 'POST':
        categoryn=request.POST.get('cat')
        subcategory_name = request.POST.get('subcat')
        name=request.POST.get('name')
        description=request.POST.get('description')
        image = request.FILES['image']
        price=request.POST.get('price')
        lower_name = name.lower()
        cat = Category.objects.filter(cname=categoryn).first()
        subcategory = Subcategory.objects.filter(scname=subcategory_name).first()

        
        if Menutbl.objects.filter(name__iexact=lower_name).exists():
            messages.info(request,"The item already exists")
            return redirect('a_add_items')
        else:
            item=Menutbl(cid=cat,sub_category=subcategory,name=name,description=description,image=image,price=price)
            item.save();
            return redirect('a_view_menu')
    else:
        category=Category.objects.all()
        subcategories = Subcategory.objects.all()
        return render(request, 'a_add_items.html', {"category": category, "subcategories": subcategories})
    
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_view_menu(request):
    items=Menutbl.objects.all()
    return render(request,'a_view_menu.html',{"items":items})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_view_category(request):
    categories=Category.objects.all()
    #subcategory=Subcategory.objects.all()
    return render(request,'a_view_category.html',{"cat":categories})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_view_subcategory(request,item_id):
    category = Category.objects.get(pk=item_id)
    subcats = Subcategory.objects.filter(cid=category)
    if subcats is not None:
        return render(request,'a_view_subcategory.html',{"subcats":subcats,"category":category})
    else:
        return redirect(a_view_category)
    
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_edit_subcategory(request,item_id):
    
    subcat = Subcategory.objects.filter(pk=item_id).first()
    if request.method == 'POST':
        # print("subcat nokkan",item_id)
        sn=request.POST.get('name')

        lower_name = sn.lower()
        if Subcategory.objects.filter(scname__iexact=lower_name).exists():
            messages.info(request,"The subcategory already exists")
        else :
            Subcategory.objects.filter(pk=item_id).update(scname=sn)
            messages.info(request,"The subcategory Edited Successfully")

        
        #return redirect(a_view_subcategory)
    if subcat is not None :
        return render(request,'a_edit_subcategory.html',{"subcat":subcat})
    else :
        return redirect(a_view_subcategory)
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_add_category(request):
    
    if request.method == 'POST':
        name=request.POST.get('name')
        lower_name = name.lower()
        if Category.objects.filter(cname__iexact=lower_name).exists():
            messages.info(request,"The item already exists")
            return redirect('a_add_category')
        else:
            item=Category(cname=name)
            item.save();
            return redirect('a_view_category')
    return render(request,'a_add_category.html')


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_edit_menu_item(request, item_id):
    item = Menutbl.objects.get(pk=item_id)
    category=Category.objects.all()
    subcategory = Subcategory.objects.all()
    if request.method == 'POST':
        categoryn=request.POST.get('catn')
        if categoryn == "" :
            categoryn=item.cid
        if categoryn is None:
            categoryn=item.cid
        subcategoryn=request.POST.get('subcatn')
        if subcategoryn == "" :
            categoryn=item.sub_category
        if subcategoryn is None:
            categoryn=item.sub_category
        
        name=request.POST.get('name')
        if name is None:
            name=item.name
        #print("name",name)
        description=request.POST.get('description')
        if description is None:
            description=item.description
        if 'eimage' in request.FILES:
            print("image bin",request.FILES) 
            #image = request.FILES['eimage']
            image = request.FILES.get('eimage', item.image)
            #image = media/images/image;
        else:
            image = item.image
        price=request.POST.get('price')
        if price is None:
            price=item.price
        cat = Category.objects.filter(cname=categoryn).first()
        subcat=Subcategory.objects.filter(scname=subcategoryn,cid=cat).first()
        if categoryn != ''and name != '' and description !='' and image !='' and price != '' and subcategoryn!='':
            Menutbl.objects.filter(pk=item.pk).update(cid=cat,name=name,description=description,image=image,price=price,sub_category=subcat)
            messages.success(request,"Changes are saved successfully !")
            return redirect('a_edit_menu_item',item.pk)
        else:
            return redirect('adminhome')
        # if form.is_valid():
        #     form.save()
        #     return redirect('a_view_menu')
    # else:
    #     form = MenutblEditForm(instance=item)
    return render(request, 'a_edit_menu_item.html', {'item': item,'category':category, 'subcategory': subcategory})


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def get_category_subcategory_data(request):
    # Query your database to get the category-subcategory data
    category_subcategory_data = {}
    categories = Category.objects.all()

    for category in categories:
        subcategories = Subcategory.objects.filter(cid=category)
        subcategory_names = [subcategory.scname for subcategory in subcategories]
        category_subcategory_data[category.cname] = subcategory_names

    return JsonResponse(category_subcategory_data)
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_add_subcategory(request, item_id):
    cat = Category.objects.filter(pk=item_id).first()
    cid=cat.cid
    if request.method == 'POST':
        name=request.POST.get('name')
        lower_name = name.lower()
        cat = Category.objects.filter(pk=item_id).first()
        if Subcategory.objects.filter(scname__iexact=lower_name,cid=cat).exists():
            messages.info(request,"The subcategory already exists")
            #return redirect(a_add_subcategory)
            return render(request,'a_add_subcategory.html',{"item_id":item_id})
        else:
            itm=Subcategory(scname=name,cid=cat)
            itm.save();
            messages.info(request,"The subcategory is added successfully ")
            return redirect(a_view_category)
            #return render(request,'a_view_subcategory.html',{"item_id":cid})
    else :
        return render(request,'a_add_subcategory.html',{"item_id":item_id})
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def get_subcategories(request):
    if request.method == 'GET':
        category_name = request.GET.get('category')
        subcategories = []

        if category_name:
            # Query your database to get subcategories based on the selected category
            # Replace this with the actual query to retrieve subcategories
            subcategories = [subcat.scname for subcat in Subcategory.objects.filter(cid__cname=category_name)]

        return JsonResponse({'subcategories': subcategories})
    
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_status_menu(request,item_id):
    item = Menutbl.objects.get(pk=item_id)
    if item.status == True:
        Menutbl.objects.filter(pk=item_id).update(status=False)
    else :
        Menutbl.objects.filter(pk=item_id).update(status=True)
    return redirect('a_view_menu')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_edit_category(request,item_id):
    category = Category.objects.get(cid=item_id)
    if request.method == 'POST':
        
        name=request.POST.get('name')
        lower_name = name.lower()
        if name is not None:
            
        
            if Category.objects.filter(cname__iexact=lower_name).exists():
                messages.info(request,"The Category already exists")
            else:
                Category.objects.filter(cid=item_id).update(cname=name)
                messages.info(request,"The category name edited successfully")
                return redirect('a_view_category')
        #return redirect(a_view_subcategory)
    return render(request,'a_edit_category.html',{'category':category})
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_status_category(request,item_id):
    item = Category.objects.get(pk=item_id)
    if item.status == True:
        Category.objects.filter(pk=item_id).update(status=False)
    else :
        Category.objects.filter(pk=item_id).update(status=True)
    return redirect('a_view_category')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_search_menu(request):
    query = request.GET.get('q', '')
    try:
        # Attempt to convert the query to a float, indicating a price search
        price_query = float(query)
        items = Menutbl.objects.filter(price=price_query)
    except ValueError:
        # If conversion to float fails, perform a text-based search by name, category, and subcategory
        items = Menutbl.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(cid__cname__icontains=query) |  # Search by category name
            models.Q(sub_category__scname__icontains=query)  # Search by subcategory name
        )

    return render(request, 'a_view_menu.html', {'items': items, 'search_query': query})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_cart_view(request):
    
    items=Cart.objects.filter(customer_id=request.user,status=True,paid=False,ordered=False)
    customizations=Customization.objects.all()
    options=Options.objects.all()
    selected_customizations=Selected_customization.objects.all()

    selected_customization_ids = Selected_customization.objects.filter(cart_id__in=items).values_list('option_id__pk', flat=True).distinct()


    print("selected_customizations : ")
    print(selected_customization_ids)
    p=0
    for i in items:
        p=p+i.price
    return render(request,'c_cart_view.html',{"items":items,"p":p,"options":options,"customizations":customizations,"selected_customizations":selected_customizations,"selected_option_ids":selected_customization_ids})
    # return render(request,'c_cart_view.html')


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_add_to_cart(request,item_id):
    if request.method == 'POST':
        item = Menutbl.objects.get(pk=item_id)
        user = User.objects.get(username=request.user)
        price=item.price
        order, created = Order.objects.get_or_create(customer_id=user,status=False)
        order.save()
        cart_item,created = Cart.objects.get_or_create(customer_id=user,order_id=order,item=item)
        if cart_item is not None:
            cart_item.quantity += 1
            cart_item.price =cart_item.price+price
            cart_item.incart=True
            cart_item.save()
    return redirect('c_cart_view') 


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_update_cart(request,item_id):
    cart_item=Cart.objects.get(pk=item_id)
    action = request.POST.get('action')
    if action == 'increase':
        if cart_item.quantity <= 10:
            q=cart_item.quantity + 1
            p=cart_item.price+cart_item.item.price
            Cart.objects.filter(pk=item_id).update(quantity=q,price=p)
    elif action == 'decrease':
        if cart_item.quantity == 1:
            Cart.objects.filter(pk=item_id).delete()
        else:
            q=cart_item.quantity - 1
            p=cart_item.price-cart_item.item.price
            Cart.objects.filter(pk=item_id).update(quantity=q,price=p)
    return redirect('c_cart_view')



@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def add_to_order(request):
    # user=User.objects.get(username=request.user)
    # cart=Cart.objects.filter(customer_id=user,status=True)
    # p=0
    # for i in cart:
    #     p=p+i.price
    # Order.objects.filter(c_id=user,status=False).update(status=True)
    # return redirect('chome')

    items=Cart.objects.filter(customer_id=request.user,incart=True,ordered=False)
    customizations=Selected_customization.objects.filter()
    p=0
    for i in items:
        p=p+i.price
        for customization in customizations:
            if customization.cart_id == i:
                p=p+customization.option_id.price
        # print(o_id)
        # print("order set")
    # print(o_id.pk)
    # print("order set")
    # Cart.objects.filter(customer_id=request.user,status=True,paid=False).update(ordered=True)
    

    for_o_id=Cart.objects.filter(customer_id=request.user,incart=True,ordered=False).first()
    order_id=for_o_id.order_id.pk
    order=Order.objects.get(pk=order_id)
    Cart.objects.filter(order_id=order).update(ordered=True)
    # order_id=Order.objects.filter(pk=Order_id)
    Order.objects.filter(pk=order_id).update(status=True,price=p)
    return redirect('c_order_view')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_order_view(request):
    # ordered_items=Cart.objects.filter(customer_id=request.user,ordered=True,paid=False,delivered=False)
    ordered_items = Cart.objects.filter(customer_id=request.user, ordered=True).filter(Q(paid=False) | Q(delivered=False))
    oneitem=Cart.objects.filter(customer_id=request.user, ordered=True).filter(Q(paid=False) | Q(delivered=False)).first()
    # myorders=Order.objects.filter(customer_id=request.user,status=True,old=False)
    orderid=None
    if oneitem is not None:
        order=oneitem.order_id
        prepared=order.ready_to_deliver
        delivered=order.delivered
        ordererstatus=order.status
        orderid=Order.objects.get(pk=oneitem.order_id.pk)
    else:
        order=None
        prepared=False
        delivered=False
        ordererstatus=False
    return render(request,'c_order_view.html',{"ordered_items":ordered_items,"prepared":prepared,"delivered":delivered,"order_id":order,"ordererstatus":ordererstatus,"orderid":orderid})


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def s_profile(request):
    user_profile = Person.objects.get(name=request.user)
    if user_profile is None:
        return redirect('loginpage')
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        #role=request.POST.get('category')
        #password=request.POST.get('password')
        #print(username)
        if username != '' and email != '' and phone != '':
            user_profile.name=username
            user_profile.phone=phone
            user_profile.address=address
            user_profile.email=email
            #user_profile.save()
            Person.objects.filter(pk=user_profile.pk).update(address=address,phone=phone)
            #data2=Users(USERNAME=username,Email address=email)
            messages.success(request,"Changes are saved successfully !")
            
            return redirect('s_profile')
        else:
            messages.error(request,"Updation failed !")
    else: 
        return render(request, 's_profile.html', {'user_profile': user_profile})
    
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def s_view_orders(request):
    orders=Order.objects.filter(old=False,status=True,delivered=False,paid_status=True)
    carts=Cart.objects.filter(ordered=True,delivered=False,paid=True)
    print("selected_customizations are cart: ")
    print(carts)
    selected_customizations=Selected_customization.objects.all()
    
    
    return render(request,'s_view_orders.html', {'orders': orders,'carts':carts,'selected_customizations':selected_customizations})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def ordered_to_prepared(request,item_id):
    cart=Cart.objects.get(pk=item_id)
    Cart.objects.filter(pk=item_id).update(prepared=True)
    order=Order.objects.get(pk=cart.order_id.pk)
    if order.started_to_prepare == False:
        Order.objects.filter(pk=cart.order_id.pk).update(started_to_prepare=True)
    return redirect('s_view_orders')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def prepared_to_ready_to_deliver(request,item_id):
    cart=Cart.objects.get(pk=item_id)
    Cart.objects.filter(pk=item_id).update(ready_to_deliver=True)
    order_id=cart.order_id.pk
    ordered_items_in_cart=Cart.objects.filter(order_id=order_id)
    finished=1
    for ord in ordered_items_in_cart:
        if ord.ready_to_deliver is False:
            finished=0
    if finished == 1:
        Order.objects.filter(pk=order_id).update(ready_to_deliver=True)
    return redirect('s_view_orders')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def deliver_order(request,order_id):
    Order.objects.filter(pk=order_id).update(delivered=True,old=True)
    order=Order.objects.get(pk=order_id)
    Cart.objects.filter(order_id=order).update(delivered=True)
    return redirect('s_view_orders')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_view_previous_orders(request):
    orders=Order.objects.filter(customer_id=request.user,old=True)
    carts=Cart.objects.filter(customer_id=request.user,)
    return render(request,'c_view_previous_orders.html',{'orders': orders,'carts':carts})
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_view_current_orders(request):
    orders=Order.objects.filter(status=True,old=False)
    return render(request,'a_view_current_orders.html',{"orders":orders})
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_view_order_history(request):
    orders=Order.objects.filter(old=True)
    return render(request,'a_view_order_history.html',{"orders":orders})
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def get_cart_details(request, order_id):
    cart_details = Cart.objects.filter(order_id=order_id)
    content = render_to_string('cart_details_modal.html', {'cart_details': cart_details})
    return JsonResponse({'content': content})



@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def make_payment(request, order_id):
    order = Order.objects.get(pk=order_id)

    if request.method == 'POST':
        # Create a Razorpay order
        client = razorpay.Client(auth=("rzp_test_3lwUgvoFZrW6nK", "1uIa50SDFbRfhqd8mxPxMWLh"))
        razorpay_order = client.order.create({'amount': int(order.price * 100), 'currency': 'INR'})


        razorpay_order_id=razorpay_order['id']
        razorpay_order_status=razorpay_order['status']


        if razorpay_order_status == 'created':
            # Update the Order model with the Razorpay Order ID
            Order.objects.filter(pk=order_id).update(razorpay_order_id=razorpay_order['id'])
            # Order.objects.filter(pk=order_id).update(paid_status=True)
            order=Order.objects.get(pk=order_id)
            if order.delivered == True:
                Order.objects.filter(pk=order_id).update(old=True)
            # Cart.objects.filter(order_id=order).update(paid=True)

            razorpay_order['name']=order.customer_id
            # return render(request, 'c_order_view.html', {'razorpay_order_id': razorpay_order['id'], 'order_id': order_id,'payment':razorpay_order})
            # return redirect('c_order_view')
            ordered_items = Cart.objects.filter(customer_id=request.user, ordered=True).filter(Q(paid=False) | Q(delivered=False))


            return render(request, 'c_order_view.html', {'razorpay_order_id': razorpay_order['id'], 'order_id_my': order_id,'order':order,'ordered_items':ordered_items,'payment':razorpay_order})
    else:
        return redirect('c_order_view')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def payment_status(request,order_id):
    Order.objects.filter(pk=order_id).update(paid_status=True)
    Cart.objects.filter(order_id=order_id).update(paid=True)
    return redirect('c_order_view')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_delefe_from_cart(request,item_id):
    Cart.objects.filter(pk=item_id).delete()
    return redirect('c_cart_view')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_table_reservation(request):
    # return render(request,'c_table_reservation.html')
    user_details = Person.objects.get(name=request.user)
    if user_details is None:
        return redirect('loginpage')
    if request.method== 'POST':
        name=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        date=request.POST.get('date')
        timein=request.POST.get('time')
        timeout=request.POST.get('timeout')
        numberofpersons=request.POST.get('numberofpersons')
        numberofpersons = int(numberofpersons)
        date_reservation=TableReservation.objects.filter(date=date)
        timein_obj = datetime.strptime(timein, '%H:%M').time()
        timeout_obj = datetime.strptime(timeout, '%H:%M').time()
        reserved=0
        list_of_occupied_tables=[]
        for x in date_reservation:
            if x.timein > timein_obj and x.timein<timeout_obj and x.reject == False:
                occupied_tables=Reserved_Tables_Details.objects.filter(reservation_id=x)
                for occupied_table in occupied_tables:
                    n=occupied_table.table_id.capacity
                    list_of_occupied_tables.append(occupied_table.table_id.t_no)
                    reserved=reserved+n
            if x.timeout > timein_obj and x.timeout < timeout_obj and x.reject == False:
                occupied_tables=Reserved_Tables_Details.objects.filter(reservation_id=x)
                for occupied_table in occupied_tables:
                    n=occupied_table.table_id.capacity
                    list_of_occupied_tables.append(occupied_table.table_id.t_no)
                    reserved=reserved+n
            if x.timein<timein_obj and x.timeout>timeout_obj and x.reject == False:
                occupied_tables=Reserved_Tables_Details.objects.filter(reservation_id=x)
                for occupied_table in occupied_tables:
                    n=occupied_table.table_id.capacity
                    list_of_occupied_tables.append(occupied_table.table_id.t_no)
                    reserved=reserved+n

        
        available_seats=40-reserved
        print(available_seats)
        if(available_seats < numberofpersons):
            message = f"There are {available_seats} seats available at that time."
            messages.success(request, message)
            return redirect('c_table_reservation')
        
        
        copy_of_numberofpersons=numberofpersons
        for_this_reservation_table_no_is=[]
        while(copy_of_numberofpersons>0):
            
            if copy_of_numberofpersons <= 2:
                flag1=0
                flag2=0
                for table_no in list_of_occupied_tables:
                    if table_no == 1 :
                        flag1=1
                    if table_no == 2 :
                        flag2=1
                if flag1 == 0 :
                    if 1 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(1)
                        copy_of_numberofpersons=copy_of_numberofpersons-2
                elif flag2 == 0:
                    if 2 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(2)
                        copy_of_numberofpersons=copy_of_numberofpersons-2
            if copy_of_numberofpersons > 0 and copy_of_numberofpersons <= 4 :
                flag3=0
                flag4=0
                flag5=0
                for table_no in list_of_occupied_tables:
                    if table_no == 3 :
                        flag3=1
                    if table_no == 4 :
                        flag4=4
                    if table_no == 5 :
                        flag5 =1
                if flag3 == 0 :
                    if 3 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(3)
                        copy_of_numberofpersons=copy_of_numberofpersons-4
                elif flag4 == 0:
                    if 4 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(4)
                        copy_of_numberofpersons=copy_of_numberofpersons-4
                elif flag5 == 0:
                    if 5 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(5)
                        copy_of_numberofpersons=copy_of_numberofpersons-4
            if copy_of_numberofpersons > 0 and copy_of_numberofpersons <= 6:
                flag6=0
                flag7=0
                for table_no in list_of_occupied_tables:
                    if table_no == 6 :
                        flag6=1
                    if table_no == 7 :
                        flag7=1
                if flag6 == 0 :
                    if 6 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(6)
                        copy_of_numberofpersons=copy_of_numberofpersons-6
                elif flag7 == 0:
                    if 7 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(7)
                        copy_of_numberofpersons=copy_of_numberofpersons-6

            if copy_of_numberofpersons > 0 and copy_of_numberofpersons <= 12:
                flag8=0
                for table_no in list_of_occupied_tables:
                    if table_no == 8 :
                        flag8=1
                if flag8 == 0 :
                    if 8 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(8)
                        copy_of_numberofpersons=copy_of_numberofpersons-12

            if copy_of_numberofpersons > 12:
                flag1=0
                flag2=0
                flag3=0
                flag4=0
                flag5=0
                flag6=0
                flag7=0
                flag8=0
                for table_no in list_of_occupied_tables:
                    if table_no == 1 :
                        flag1=1
                    if table_no == 2 :
                        flag2=1
                    if table_no == 3 :
                        flag3=1
                    if table_no == 4 :
                        flag4=1
                    if table_no == 5 :
                        flag5=1
                    if table_no == 6 :
                        flag6=1
                    if table_no == 7 :
                        flag7=1
                    if table_no == 8 :
                        flag8=1
                if flag8 == 0:
                    if 8 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(8)
                        copy_of_numberofpersons=copy_of_numberofpersons-12
                if flag7 == 0 and copy_of_numberofpersons >= 6 :
                    if 7 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(7)
                        copy_of_numberofpersons=copy_of_numberofpersons-6
                if flag6 == 0 and copy_of_numberofpersons >= 6 :
                    if 6 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(6)
                        copy_of_numberofpersons=copy_of_numberofpersons-6
                if flag5 == 0 and copy_of_numberofpersons >= 4:
                    if 5 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(5)
                        copy_of_numberofpersons=copy_of_numberofpersons-4
                if flag4 == 0 and copy_of_numberofpersons >= 4:
                    if 4 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(4)
                        copy_of_numberofpersons=copy_of_numberofpersons-4
                if flag3 == 0 and copy_of_numberofpersons >= 4:
                    if 3 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(3)
                        copy_of_numberofpersons=copy_of_numberofpersons-4
                if flag2 == 0 and copy_of_numberofpersons >= 2:
                    if 2 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(2)
                        copy_of_numberofpersons=copy_of_numberofpersons-2
                if flag1 == 0 and copy_of_numberofpersons >= 4:
                    if 1 not in for_this_reservation_table_no_is:
                        for_this_reservation_table_no_is.append(1)
                        copy_of_numberofpersons=copy_of_numberofpersons-2




            
        if for_this_reservation_table_no_is is None:
            message = f"There is n tables available at that time."
            messages.success(request, message)
            return redirect('c_table_reservation')




        if user_details != '' and email != '' and phone != '' and date != '' and timein != '' and numberofpersons != '' and timeout != '' :
            t_id=Table_Details.objects.get(t_no=1)
            new_reserv=TableReservation(customer_id=request.user,email=email,phone=phone,date=date,timein=timein,timeout=timeout,numberofpersons=numberofpersons,table_id=t_id)
            new_reserv.save()
            for i in for_this_reservation_table_no_is:
                table_id=Table_Details.objects.get(t_no=i)
                new_reserved_table_details=Reserved_Tables_Details(reservation_id=new_reserv,table_id=table_id)
                new_reserved_table_details.save()

            messages.success(request,f"Reservation completed successfully.")
        return redirect('c_table_reservation')
   
    else: 
        return render(request, 'c_table_reservation.html', {'user_details': user_details})
    
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_view_table_reservation(request):
    reservation_details=TableReservation.objects.all()
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    return render(request,'a_view_table_reservation.html',{'reservations':reservation_details,'current_date':current_date,'current_time':current_time})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_table_rejection(request,reservation_id):
    tbd=TableReservation.objects.get(pk=reservation_id)
    # if request.method== 'POST':
    #     tbd.reject=True
    #     tbd.save()
    return render(request,'send_mail_page.html',{'reservation':tbd,'reservation_id':reservation_id})
    # return redirect('a_view_table_reservation')



@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_view_previous_reservations(request):
    # user_det = Person.objects.get(name=request.user)
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    
    print(current_time)
    prevdet=TableReservation.objects.filter(customer_id=request.user)
    res_table_nos=Reserved_Tables_Details.objects.all()
    return render(request,'c_view_previous_reservations.html',{'previous_details':prevdet,'current_date':current_date,'current_time':current_time,'res_table_nos':res_table_nos})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def send_mail_page(request,reservation_id):
    if request.method == "POST":
        title=request.POST['title']
        email=request.POST['email']
        reason=request.POST['reason']
        send_mail(
            title,
            reason,
            settings.EMAIL_HOST_USER,
            [email],
        )
        TableReservation.objects.filter(pk=reservation_id).update(reject=True,reason=reason)
        reservation = get_object_or_404(TableReservation, pk=reservation_id)
        Reserved_Tables_Details.objects.filter(reservation_id=reservation).delete()
    return render(request,'a_view_table_reservation.html')

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_view_specific_date_reservations(request):
    current_date = timezone.now().date()
    if request.method=='POST':
        current_date=request.POST.get('date')
    reservation_details=TableReservation.objects.filter(date=current_date)
    total_no_of_reservation=0
    flag=0
    if reservation_details.exists():
        
        for x in reservation_details:
            if x.reject == False and x.cancel== False:
                flag=1
                total_no_of_reservation=total_no_of_reservation+1
    if flag==0 :
        reservation_details=None
    return render(request,'a_view_specific_date_reservations.html',{'reservations':reservation_details,'no_of_reservations':total_no_of_reservation})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_view_rejected_reservations(request):
    reservations=TableReservation.objects.filter(reject=True)
    return render(request,'a_view_rejected_reservations.html',{'reservations':reservations})


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def c_cancel_reservation(request,reservation_id):
    reservation = get_object_or_404(TableReservation, pk=reservation_id)
    TableReservation.objects.filter(pk=reservation_id).update(cancel=True)
    Reserved_Tables_Details.objects.filter(reservation_id=reservation).delete()
    
    return redirect('c_view_previous_reservations')

# @background(schedule=15*60)  # 15 minutes in seconds
# def send_confirmation_email(reservation_id):
#     reservation = TableReservation.objects.get(pk=reservation_id)
#     subject = 'Confirmation for Table Reservation'
#     message = f'Your reservation on {reservation.date} at {reservation.timein} has been confirmed.'
#     send_mail(subject, message, 'your_email@example.com', [reservation.email])

# @receiver(pre_save, sender=TableReservation)
# def schedule_confirmation_email(sender, instance, **kwargs):
#     if instance.pk:  # Check if the instance is being updated
#         return
    
#     # Calculate the scheduled time for sending the email
#     confirmation_time = instance.timein - timezone.timedelta(minutes=15)
    
#     # Schedule the task to send the confirmation email
#     send_confirmation_email(instance.pk, schedule=confirmation_time)


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def c_calorie_detection(request):
    return render(request,'c_calorie_detection.html')














@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_customization(request):
    menu=Menutbl.objects.all()
    return render(request,'a_customization.html',{'menu':menu})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_view_customization(request, menu_id):
    customizations=Customization.objects.filter(menu_item_id=menu_id)
    options=Options.objects.all()
    menu_item=Menutbl.objects.get(pk=menu_id)
    if not options:
        options="None"
    return render(request,'a_view_customization.html',{'customizations':customizations,'options':options,'menu_id':menu_id,'menu_item':menu_item})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_add_customizations(request,menu_id):
        # messages.success(request, 'Customization added successfully.')
        # return redirect('a_view_customization', menu_id=menu_id)
    return render(request,'a_add_customizations.html',{'menu_id':menu_id})


@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_add_customizations_onclick(request,menu_id):
    if request.method =='POST':
        menu_item=Menutbl.objects.get(pk=menu_id)

        name=request.POST.get('cname')
        description = request.POST.get('description')
        customization_type = request.POST.get('type')
        if customization_type == 'radio':
            type=True
        else :
            type=False
        
        have_customization=Customization.objects.filter(menu_item_id=menu_item,name=name)
        if have_customization :
            messages.success(request, 'This customization is already exists')
            return redirect('a_add_customizations', menu_id=menu_id)

        else:
            if description != None and name != None:
                customization = Customization.objects.create(
                menu_item_id=menu_item,
                name=name,
                description=description,
                type=type  # Set type based on form input
                )

            option_name = request.POST.get('option_name')
            option_price = request.POST.get('option_price')

            if option_name :
                Options.objects.create(
                    customization=customization,
                    name=option_name,
                    price=option_price,
                 # Assuming all options are active by default
                )
        
        # option_names = request.POST.getlist('option_name[]')
        # option_prices = request.POST.getlist('option_price[]')

        # for name, price in zip(option_names, option_prices):
        #     Options.objects.create(
        #         customization=customization,
        #         name=name,
        #         price=price,
        #         status=True  # Assuming all options are active by default
        #     )
            return redirect('a_view_customization', menu_id=menu_id)
    else:
        return redirect('a_add_customizations', menu_id=menu_id)



@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_edit_customization(request,customization_id):
    customization_item=Customization.objects.get(pk=customization_id)
    return render(request,'a_edit_customization.html',{'customization_item':customization_item})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_edit_customization_on_click_btn(request,customization_id):
    customization_item=Customization.objects.get(pk=customization_id)
    menu_id=customization_item.menu_item_id.pk
    menu_item=Menutbl.objects.get(pk=menu_id)
    if request.method =='POST':
        name=request.POST.get('cname')
        description = request.POST.get('description')
        customization_type = request.POST.get('type')
        if customization_type == 'radio':
            type=True
        else :
            type=False
        prev_name=customization_item.name
        prev_description=customization_item.description
        prev_type=customization_item.type

        if prev_name.lower() == name.lower() and prev_description.lower() == description.lower() and prev_type == type :
            messages.success(request, 'There is nothing to change')
            return redirect('a_edit_customization', customization_id=customization_id)
        else :
            have_customization=Customization.objects.filter(menu_item_id=menu_item,name=name)

            if have_customization:
                messages.success(request, 'The customization name is already exists')
                return redirect('a_edit_customization', customization_id=customization_id)
            else:
                Customization.objects.filter(pk=customization_id).update(name=name,description=description,type=type)
                # messages.success(request, 'Customization Edited successfully.')
                return redirect('a_view_customization', menu_id=menu_id)
    else:
        return redirect('a_view_customization', customization_id=customization_id)
    
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_delete_customization(request,customization_id):
    customization = get_object_or_404(Customization, pk=customization_id)
    menu_item_id = customization.menu_item_id.pk
    customization.delete()
    # messages.success(request, 'Customization deleted successfully.')
    return redirect('a_view_customization', menu_id=menu_item_id)

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_delete_option(request,option_id):
    option = get_object_or_404(Options, pk=option_id)
    menu_item_id = option.customization.menu_item_id.pk
    option.delete()
    # messages.success(request, 'Option deleted successfully.')
    return redirect('a_view_customization', menu_id=menu_item_id)

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_edit_option(request,option_id):
    option = get_object_or_404(Options, pk=option_id)
    return render(request,'a_edit_option.html',{'option':option})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True) 
def a_edit_option_on_click_btn(request,option_id):
    if request.method == 'POST':
        name=request.POST.get('option_name')
        price = float(request.POST.get('option_price'))
        option=Options.objects.get(pk=option_id)

        prev_name=option.name
        prev_price=float(option.price)
        customization=option.customization
        if prev_name.lower() == name.lower() and prev_price == price :
            messages.success(request, 'There is nothing to change')
            return redirect('a_edit_option', option_id=option_id)
        else:
            have_option=Options.objects.filter(customization=customization,name=name)
            if have_option and prev_price == price:
                messages.success(request, 'Option name is already exist')
                return redirect('a_edit_option', option_id=option_id)
            
            else:
                Options.objects.filter(pk=option_id).update(name=name,price=price)
                menu_item_id=option.customization.menu_item_id.pk
                return redirect('a_view_customization', menu_id=menu_item_id)
    else :
        return redirect('a_edit_option', option_id=option_id)
    
@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_add_option(request,customization_id):
    return render(request,'a_add_option.html',{'customization_id':customization_id})

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def a_add_option_onclick(request,customization_id):
    if request.method == 'POST':
        customization=Customization.objects.get(pk=customization_id)
        name=request.POST.get('option_name')
        price = request.POST.get('option_price')
        have_option=Options.objects.filter(customization=customization,name=name)
        if not have_option:
            if name:
                option = Options.objects.create(
                    customization=customization,
                    name=name,
                    price=price # Set type based on form input
                )
            menu_item_id=option.customization.menu_item_id.pk
            return redirect('a_view_customization', menu_id=menu_item_id)
        else :
            messages.success(request, 'Option name is already exists')
            return redirect('a_add_option', customization_id=customization_id)
        

@login_required
@cache_control(no_cash=True,must_validate=True,no_store=True)
def c_apply_customization(request,cart_id,customization_id,option_id):

    cart=Cart.objects.get(pk=cart_id)
    customization=Customization.objects.get(pk=customization_id)
    option=Options.objects.get(pk=option_id)
    order_id=cart.order_id
    if request.method == 'POST':
        
        selected_customizations_to_delete = Selected_customization.objects.filter(cart_id=cart, customization_id=customization)
        
        if selected_customizations_to_delete.exists():
            selected_customizations_to_delete.delete()

        options_selected = request.POST.getlist('option')  # Get list of selected options
        for option_name in options_selected:
        # Assuming option_name uniquely identifies each option, retrieve option_id from database
            option_id = Options.objects.get(name=option_name) # Replace Option with your model name
        # Create Selected_customization instance
            Selected_customization.objects.create(
                order_id=order_id,  # Replace with actual order_id
                cart_id=cart,    # Replace with actual cart_id
                customization_id=customization,  # Replace with actual customization_id
                option_id=option_id,
              # Set status as needed
            )
            

    items=Cart.objects.filter(customer_id=request.user,incart=True,ordered=False)
    customizations=Selected_customization.objects.filter()
    p=0
    for i in items:
        p=p+i.price
        for customization in customizations:
            if customization.cart_id == i:
                p=p+customization.option_id.price
    
    items=Cart.objects.filter(customer_id=request.user,status=True,paid=False,ordered=False)
    customizations=Customization.objects.all()
    options=Options.objects.all()
    selected_customizations=Selected_customization.objects.all()

    selected_customization_ids = Selected_customization.objects.filter(cart_id__in=items).values_list('option_id__pk', flat=True).distinct()


    print("selected_customizations : ")
    print(selected_customization_ids)
    return render(request,'c_cart_view.html',{"items":items,"p":p,"options":options,"customizations":customizations,"selected_customizations":selected_customizations,"selected_option_ids":selected_customization_ids})
    # return render(request,'c_cart_view.html')
    return redirect('chome')


def c_apply_radiocustomization(request,cart_id,customization_id,option_id):
    cart=Cart.objects.get(pk=cart_id)
    customization=Customization.objects.get(pk=customization_id)
    option=Options.objects.get(pk=option_id)
    order_id=cart.order_id
    if request.method == 'POST':
        print("After post")
        selected_customizations_to_delete = Selected_customization.objects.filter(cart_id=cart, customization_id=customization)
        
        if selected_customizations_to_delete.exists():
            selected_customizations_to_delete.delete()
        option_id = request.POST.get('option')
        Selected_customization.objects.create(
            order_id=cart.order_id,
            cart_id=cart,
            customization_id=customization,
            option_id=option_id
        )
    
    items=Cart.objects.filter(customer_id=request.user,incart=True,ordered=False)
    customizations=Selected_customization.objects.filter()
    p=0
    for i in items:
        p=p+i.price
        for customization in customizations:
            if customization.cart_id == i:
                p=p+customization.option_id.price
    
    items=Cart.objects.filter(customer_id=request.user,status=True,paid=False,ordered=False)
    customizations=Customization.objects.all()
    options=Options.objects.all()
    selected_customizations=Selected_customization.objects.all()
    selected_customization_ids = Selected_customization.objects.filter(cart_id__in=items).values_list('option_id__pk', flat=True).distinct()
    return render(request,'c_cart_view.html',{"items":items,"p":p,"options":options,"customizations":customizations,"selected_customizations":selected_customizations,"selected_option_ids":selected_customization_ids})

    return redirect('chome')


def c_clear_customization(request):
    print("Enter to this c")
    