
from django.forms.models import inlineformset_factory
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .form import OrderForm, CreateUserForm, CustomerForm
from .filter import OrderFilter
from accounts.models import Customer, Order, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # write in signals.py
            # group = Group.objects.get(name="customer")
            # user.groups.add(group)
            # Customer.objects.create(
            #     user = user,
            #     name = user.username,
            #     email=user.email
            # )
            
            messages.success(request,"Account was created for "+ username)
            return redirect('/login')
        
    context = {"form":form }
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
            
        user = authenticate(request, username = username , password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"Username or Passsword is incorrect")      
    context = {}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allow_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    context = {'form':form}
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    
    return render(request,'accounts/account_settings.html',context)


@login_required(login_url='login')
@admin_only
def home(request):
    order = Order.objects.all().order_by('-id') 
    customer = Customer.objects.all()
    total_customer = customer.count()
    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    
    context = {"orders":order,"customers":customer,"total_customer":total_customer,"total_order":total_order,
               "delivered":delivered,"pending": pending}
    
    return render(request,"accounts/dashboard.html",context)

@login_required(login_url='login')
@allowed_users(allow_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all().order_by('-id') 
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {"order":orders,"total_order":total_order,
               "delivered":delivered,"pending": pending}
    return render(request,"accounts/userpage.html",context)

@login_required(login_url='login')
@allowed_users(allow_roles=['Admin'])
def product(request):
    product = Product.objects.all()
    return render(request,"accounts/product.html",{"products":product})

@login_required(login_url='login')
@allowed_users(allow_roles=['Admin'])
def customer(request,pk): 
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all().order_by('-id')  # querying the customers child object fro models field
    order_count = order.count()
    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs
    context = {'customer':customer,"order":order,'order_count':order_count,"myFilter":myFilter}
    
    return render(request,"accounts/customer.html",context)

@login_required(login_url='login')
@allowed_users(allow_roles=['Admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        # print("Printing Post: ",request.POST)
        form = OrderFormSet(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context={
        'form':formset
    }
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allow_roles=['Admin'])
def updateOrder(request,pk):
    
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == "POST":
        # print("Printing Post: ",request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={
        'form':form
    }
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allow_roles=['Admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context={'item':order}
    
    return render(request,'accounts/delete.html',context)
