from django.shortcuts import render, get_object_or_404, redirect
from basket_app.forms import CustomerForm,OrderForm

from django.conf import settings
from django.utils import timezone
import datetime
  
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView)
from .models import *
# Create your views here.
# class base(ListView):
#     template_name= 'base.html'
#     model= Category
#     context_object_name= "cat"

class index(ListView):
    template_name= 'index.html'
    model= Category
    context_object_name= "cat"

    def get_context_data(self,**kwargs):
        user= self.request.user #how does this work??
        context= super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["count"]= Cart.objects.filter(customer=user).count()#doubt...not efficient
        
        return context

class ProductView(ListView):
    template_name= 'product.html'
    model= Product
    context_object_name= "prod"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        
        slug= self.kwargs.get("slug")
        
        category= Category.objects.get(slug=slug)
        products= Product.objects.filter(category=category)
        

        context["products"]= products
        context["cat"]= Category.objects.all
        context["category"]= category
        context["count"]= Cart.objects.filter(customer= self.request.user).count()

        return context

class CartView(ListView):
    template_name= 'cart.html'
    model= Cart
    context_object_name= "cart_item"

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context["count"]= Cart.objects.filter(customer= self.request.user).count()
        context["cat"]= Category.objects.all

        if Cart.objects.filter(customer= self.request.user).count()==0:
            context["check"]=True
        else:
            context["cartproducts"]= Cart.objects.filter(customer= self.request.user)

            cart= Cart.objects.filter(customer= self.request.user)
            total= 0 
            for c in cart:
                total= total + c.finalprice()

            context["total"]= total

        return context

class OrderView(ListView):
    template_name= 'order.html'
    model= Order

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)

        context["cat"]= Category.objects.all
        context["count"]= Cart.objects.filter(customer= self.request.user).count()
            
        if Order.objects.filter(customer= self.request.user).count()==0:
            context["check"]=True
        else:
            order= Order.objects.filter(customer= self.request.user)
            context["orderr"]= order

        return context

class OrderSummary(DetailView):
    template_name= 'ordered.html'
    model= Order
    context_object_name= "orderr"

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)

        context["cat"]= Category.objects.all
        context["count"]= Cart.objects.filter(customer= self.request.user).count()    

        # order= get_object_or_404(Order,pk= self.kwargs.get('pk'))
        order= Order.objects.filter(pk=self.kwargs.get('pk'))
        order= order[0]
        items= OrderItem.objects.filter(order= order)
        
        context["items"]= items

        total= 0 
        for c in items:
            total= total + c.finalprice()

        context["total"]= total

        return context


# Functionalities
def add_to_cart(request,pk):
    product= get_object_or_404(Product, pk=pk)
    slug= product.category.slug

    cart_list= Cart.objects.filter(product=product, customer=request.user)

    if cart_list.exists():
        cart= cart_list[0]
        cart.qty = cart.qty + 1

        cart.save()
        
    else:
        cart_item= Cart.objects.create(product=product, customer=request.user)
        cart_item.save()

    return redirect('basket_app:product', slug= slug)

def increase_qty(request,pk):
    product= get_object_or_404(Product, pk=pk)
    cartproduct= Cart.objects.filter(customer=request.user, product=product)

    cart= cartproduct[0] 
    cart.qty = cart.qty + 1
    cart.save()

    return redirect('basket_app:cart')

def decrease_qty(request,pk):
    product= get_object_or_404(Product, pk=pk)
    cartproduct= Cart.objects.filter(customer=request.user, product=product)

    cart= cartproduct[0] 
    
    if cart.qty == 1:
        cart.delete()
        
    else:
        cart.qty = cart.qty - 1
        cart.save()

    return redirect('basket_app:cart')

def remove_product(request,pk):
    product= get_object_or_404(Product, pk=pk)
    cartproduct= Cart.objects.filter(customer=request.user, product=product)

    cart= cartproduct[0] 
    cart.delete()

    return redirect('basket_app:cart')
# End Of Functionalities

# Login, Logout, Signup, Forms
def signup(request):

    registered = False

    if request.method == "POST":
        customer_form = CustomerForm(data=request.POST)

        if customer_form.is_valid():
            user = customer_form.save()
            user.set_password(user.password)
            user.save()

            registered=True
            login(request,user)
            return HttpResponseRedirect(reverse('index'))

        else:
            print(customer_form.errors)
    
    else:
        customer_form = CustomerForm()

    return render(request, 'basket_app/register.html', {'customer_form':customer_form, 'registered':registered})

    # def form_valid (self_form ):

    #     obj = get_object_or_404(orderform,pk=form.cleaned_data['id']))

    #     receiver_name = obj.recname

    #     obj = get_object_or_404(User, Username = receiver_name)
    #     address = obj.address



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))

        else:
            print("Someone tried to login and failed!!!")
            print("Username: {} and Password: {}".format(username,password))

            return HttpResponse("invalid login details supplied!!!")

    else:
<<<<<<< HEAD
        return render(request, 'basket_app/login.html', {}) #Y else has render condition
=======
        return render(request, 'basket_app/login.html', {}) #Y else has rendeer condition
>>>>>>> 734c71bab4cca4ce0c233bb063fabc875757f999

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

class Orderform(CreateView):
    model = Receiver
    form_class = OrderForm
    template_name = 'basket_app/fillupform.html'

    def post(self,request):
        receiver = OrderForm(data=request.POST)
        if receiver.is_valid():
            r = receiver.save(commit = False)
            r.save()
            cartobjects= Cart.objects.filter(customer=request.user)

            today= datetime.date.today()
            tdelta= datetime.timedelta(days=1)
            tday= today
            today= today + tdelta
            
            order= Order.objects.create(customer=request.user,receiver=r,arrival_date= today,order_date= tday)
            for cp in cartobjects:
                order_item= OrderItem.objects.create(order=order,product=cp.product,qty=cp.qty)
                order_item.save()

            Cart.objects.filter(customer=request.user).delete()

            return redirect('basket_app:order')
        else:
            print("Invalid Form")

            print(receiver.errors)
            return redirect('basket_app:fillup')
# End Of Login, Logout, Signup, Forms

