from django.conf import settings
from django.contrib import auth
from django.db.models.deletion import PROTECT
from django.http.response import Http404, HttpResponseBase
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, request, HttpResponseNotFound
from django.views.generic.list import ListView
from ecommerce.models import Buyer, Order, ProductImage, Seller, ShippingAddress, UserProfile, Product, Category
from django.db.models import Q
from django.views.generic.edit import DeleteView, UpdateView
from .forms import AddressForm, BuyerSignUpForm, EditProductForm, SellerRemoveProductsForm, SellerSignUpForm, BuyerProfileForm, SellerProfileForm

from django.views.generic.detail import DetailView
from django.http import HttpResponse
from .forms import AddressForm, BuyerSignUpForm, SellerSignUpForm, AddProductForm, OTPForm, AdminAddProductsForm, AdminRemoveProductsForm, AdminRemoveBuyersForm, AdminSellerActionsForm
import random
import stripe
import datetime
from django.core.mail import send_mail


def getRandomNumber():
    return random.randint(100000, 999999)


def int_or_0(value):
    try:
        return int(value)
    except:
        return 0

# http://127.0.0.1:8000/kyntra/seller/edit_product/13/
class ProductDetailView(DetailView):
    model = Product
    template_name = 'general/individual_item.html'


class SearchProductListView(ListView):
    model = Product
    paginate_by = 15
    template_name = 'general/home.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('product')
        category = self.request.GET.get('category')
        object_list = Product.objects.all()

        if query:
            object_list = Product.objects.filter(
                Q(name__icontains=query))
        if category:
            object_list = object_list.filter(category__name=category)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('product')
        category = self.request.GET.get('category')

        if query == None:
            query = ""
            if category:
                context['title'] = f"Products in {category} "

        else:
            if query:
                context['title'] = f"Search results for  {query} "
            if category:
                context['title'] += f"in  {category} "
        context['additional_q_params_for_pagination'] = ""
        if query:
            context['additional_q_params_for_pagination'] = f"product={query}"
        if category:
            context['additional_q_params_for_pagination'] += f"&category={category}"

        return context


class ProductCategoryListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'general/home.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('category')
        if not(query):
            return None
        object_list = Product.objects.filter(
            Q(category=query))
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category == None:
            category = ""

        context['title'] = f"{category} products"
        context['additional_q_params_for_pagination'] = f"category={category}"
        return context

    def get_queryset(self):  # new
        query = self.request.GET.get('product')
        if not(query):
            return Product.objects.all()
        object_list = Product.objects.filter(
            Q(name__icontains=query))

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('product')
        if query == None:
            query = ""

        context['title'] = f"Search results for '{query}' "
        context['additional_q_params_for_pagination'] = f"product={query}"
        return context


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'general/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Product Catalog"
        return context


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def update_user_data(user, phone):
    UserProfile.objects.update_or_create(user=user, defaults={'phone': phone})


def signup(request):
    return render(request, 'registration/signup.html')


def otp_verification(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            email = form.cleaned_data.get('email')
        user = UserProfile.objects.get(user__email=email)
        tzinfo = datetime.timezone(datetime.timedelta(0))
        currTime = datetime.datetime.now(tzinfo)
        if otp == user.otp and currTime < user.otp_expiry and user.is_verified == False:
            user.is_verified = True
            user.otp_expiry = currTime
            user.save()
            return redirect('login')
        else:
            user.delete()
            return HttpResponse("Invalid OTP! User is requested to sign up again to get another OTP.")
    else:
        form = OTPForm()
    return render(request, 'registration/otp_verification.html', {'form': form})


def Purchase(request):
    if not request.user.is_authenticated:
        return redirect('login')

    product_id = request.POST.get('product_id')
    quantity = request.POST.get('item_count')
    quantity = int_or_0(quantity)

    try:
        q_set = Product.objects.all().filter(id=product_id)

        if len(q_set) != 1:
            return HttpResponse(status=404)
        if q_set[0].quantity < quantity or quantity == 0:
            return HttpResponse(status=404)

        # create payment intent and send to checkout page
        product = q_set[0]
        # multiply by 100 to get in paise
        amount = (int)(product.price * quantity * 100)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
            payment_method_types=['card'],
            receipt_email=request.user.email,
            description=product.name
        )
        # create order based on payment intent
        buyer = Buyer.objects.get(user=request.user)
        order = Order.objects.create(
            user=buyer,
            product=product,
            quantity=quantity,
            amount=amount,
            stripe_payment_intent=intent.id,
            stripe_client_secret=intent.client_secret,
            payment_completed=False,
            payment_failed=False,
            order_date=datetime.datetime.now(datetime.timezone.utc),
        )
        order.save()
        product.quantity -= quantity
        product.save()
        
        LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Product).pk, object_id=product.id, object_repr=product.name, action_flag=2)

        return render(request, 'payment/checkout.html',
                    {
                        'client_secret': intent.client_secret,
                        'public_key': settings.STRIPE_PUBLIC_KEY,
                        'object': {
                            'name': product.name,
                            'price': product.price,
                            'quantity': quantity,
                            'amount': amount/100,
                        }
                    }
                    )
    except (Product.DoesNotExist, Buyer.DoesNotExist, Seller.DoesNotExist):
        raise Http404()


def payment_complete(request):
    if not request.user.is_authenticated:
        return HttpResponse("You are not logged in!", status=401)

    buyer = Buyer.objects.get(user=request.user)
    if request.method == 'GET':
        # get users order
        orders = Order.objects.filter(user=buyer).order_by('-order_date')
        if orders == []:
            return HttpResponse("You have no pending orders!", status=404)
        # confirm payment
        first = True
        curr_order_status = ""
        for order in orders:
            if order.payment_completed or order.payment_failed:
                continue
            stripe.api_key = settings.STRIPE_SECRET_KEY
            obj = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)
            if first == True:
                first = False
                curr_order_status = obj.status

            if obj.status == 'succeeded':
                order.payment_completed = True
                order.payment_failed = False
                order.save()
            elif obj.status == "processing":
                pass
            elif obj.status == "requires_payment_method":
                order.payment_failed = True
                order.save()
                product = order.product
                product.quantity += order.quantity
                product.save()
            else:
                order.payment_failed = True
                order.save()
                product = order.product
                product.quantity += order.quantity
                product.save()

        if first:
            return redirect("index")
        if curr_order_status == 'succeeded':
            return render(request, 'payment/payment_success.html')
        elif curr_order_status == "processing":
            return render(request, 'payment/payment_processing.html')
        elif curr_order_status == "requires_payment_method":
            return render(request, 'payment/payment_failed.html')
        else:
            return render(request, 'payment/payment_failed.html')
    else:
        return HttpResponse("Invalid request!", status=400)


def buyer_signup(request):
    if request.method == 'POST':
        form = BuyerSignUpForm(request.POST)
        address_form = AddressForm(request.POST)
        if form.is_valid() and address_form.is_valid():
            user = form.save()
            address = address_form.save()
            user.refresh_from_db()
            nextTime = datetime.datetime.now() + datetime.timedelta(minutes=15)
            otp = getRandomNumber()
            Buyer.objects.create(user=user, address=address,
                                 otp=otp, otp_expiry=nextTime, is_buyer=True)
            send_mail('Your OTP for verification (Kyntra): ', 'Your OTP is {}'.format(
                otp), settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            user.save()
            address.save()
            LogEntry.objects.log_action(user_id=user.id, content_type_id=ContentType.objects.get_for_model(Buyer).pk, object_id=user.id, object_repr=user.username, action_flag=1)
            return redirect('otp_verification')
    else:
        form = BuyerSignUpForm()
        address_form = AddressForm()

    return render(request, 'registration/buyer_signup.html', {'form': form, "address_form": address_form})


def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            nextTime = datetime.datetime.now() + datetime.timedelta(minutes=15)
            otp = getRandomNumber()
            Seller.objects.create(user=user, otp=otp, otp_expiry=nextTime, company_name=form.cleaned_data.get(
                'company_name'), gst_number=form.cleaned_data.get('gst_number'), is_seller=True, document=request.FILES['document'], applied=True)
            send_mail('Your OTP for verification (Kyntra): ', 'Your OTP is {}'.format(
                otp), settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            LogEntry.objects.log_action(user_id=user.id, content_type_id=ContentType.objects.get_for_model(Seller).pk, object_id=user.id, object_repr=user.username, action_flag=1)
            return redirect('otp_verification')
    else:
        form = SellerSignUpForm()

    return render(request, 'registration/seller_signup.html', {'form': form})

def redirect_user(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.is_verified:
                if user_profile.is_buyer:
                    return redirect('index')
                elif user_profile.is_seller:
                    return redirect('seller_all_products')
                elif user_profile.is_admin:
                    return redirect('admin_dashboard')
                else:
                    return Http404()
            else:
                return redirect('otp_verification')
        except UserProfile.DoesNotExist:
            raise Http404()
    else:
        return redirect('login')


def index(request):
    return render(request, 'general/home.html')


def admin_check(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return user_profile.is_admin

        except UserProfile.DoesNotExist:
            raise Http404()
    else:
        return False


def admin_dashboard(request):
    if admin_check(request):
        buyers = Buyer.objects.all()
        sellers = Seller.objects.all()
        pending = sellers.filter(applied=True, approved=False)
        products = Product.objects.all()
        b = len(buyers)
        s = len(sellers)
        pen = len(pending)
        p = len(products)

        return render(request, 'admin/admin_dashboard.html', {
            'name': 'admin_dashboard',
            'buyer_count': b,
            'seller_count': s,
            'pending_count': pen,
            'product_count': p})
    else:
        return redirect_user(request)


def admin_buyers(request, option='all'):
    if admin_check(request):
        buyers = Buyer.objects.all()
        buyer_count = len(buyers)
        # buyer_count = option
        return render(request, 'admin/admin_buyers.html', {
            'name': 'admin_buyers',
            'option': option,
            'buyers': buyers,
            'buyer_count': buyer_count
        })
    else:
        return redirect_user(request)


def admin_removebuyer(request):
    if admin_check(request):
        if request.method == 'POST':
            form = AdminRemoveBuyersForm(request.POST)
            if form.is_valid():
                buyer = Buyer.objects.get(user=User.objects.get(id =form.cleaned_data['id']))
                LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Buyer).pk, object_id=buyer.user.id, object_repr=buyer.user.username, action_flag=3)
                User.objects.filter(id = buyer.user.id).delete()
                buyer.delete()

                return redirect('admin_buyers')

        return admin_buyers(request)
    else:
        return redirect_user(request)


def admin_sellers(request, option="all"):
    if admin_check(request):
        sellers = Seller.objects.all()
        pending = sellers.filter(applied=True, approved=False)
        approved = sellers.filter(applied=True, approved=True)
        unapproved = sellers.filter(applied=False)

        # seller_count = len(sellers)
        seller_count = len(sellers)
        pending_count = len(pending)
        approved_count = len(approved)
        unapproved_count = len(unapproved)

        sellerlist = []
        if option == 'pending':
            sellerlist = pending
        elif option == 'approved':
            sellerlist = approved
        elif option == 'unapproved':
            sellerlist = unapproved
        else:
            sellerlist = sellers

        return render(request, 'admin/admin_sellers.html', {
            'name': 'admin_sellers',
            'option': option,
            'sellers': sellerlist,
            'seller_count': seller_count,
            'pending_count': pending_count,
            'approved_count': approved_count,
            'unapproved_count': unapproved_count,
        })
    else:
        return redirect_user(request)


def admin_selleractions(request):
    if admin_check(request):
        if request.method == 'POST':
            form = AdminSellerActionsForm(request.POST)
            if form.is_valid():
                seller = Seller.objects.get(user=User.objects.get(id =form.cleaned_data['id']))
                if('approveButton' in request.POST):
                    LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Seller).pk, object_id=seller.user.id, object_repr=seller.user.username, action_flag=2)
                    seller.approved=True
                    seller.save()

                if('rejectButton' in request.POST):
                    LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Seller).pk, object_id=seller.user.id, object_repr=seller.user.username, action_flag=2)
                    seller.approved=False
                    seller.applied=False
                    seller.save()

                if('deleteButton' in request.POST):
                    LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Seller).pk, object_id=seller.user.id, object_repr=seller.user.username, action_flag=3)
                    User.objects.filter(id = seller.user.id).delete()
                    seller.delete()

                return redirect('admin_sellers')

        return admin_sellers(request)
    else:
        return redirect_user(request)


def admin_products(request, option="all"):
    if admin_check(request):
        products = []
        product_count = []
        curr = 0

        products.append(Product.objects.all())
        categories = Category.objects.all()

        i = 0
        for c in categories:
            i += 1
            products.append(Product.objects.filter(
                category=Category.objects.filter(name=c.name).get()))
            if c.name == option:
                curr = i
        # product_count = len(sellers)
        for p in products:
            product_count.append(len(p))

        form = AdminAddProductsForm()

        return render(request, 'admin/admin_products.html', {
            'name': 'admin_products',
            'option': option,
            'products': products[curr],
            'product_count': product_count,
            'categories': categories,
            'form': form,
        })
    else:
        return redirect_user(request)


def admin_addproduct(request):
    if admin_check(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = AdminAddProductsForm(request.POST,request.FILES)
            # check whether it's valid:
            if form.is_valid():
                product = form.save()
                product.save()
                LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Product).pk, object_id=product.id, object_repr=product.name, action_flag=1)

                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return redirect('admin_products')

        # if a GET (or any other method) we'll create a blank form
            # remove
        # else:
            # add line in admin products
            # form = AdminAddProductsForm()

        # return render(request, 'admin/name.html', {'form': form})
        return admin_products(request)
    else:
        return redirect_user(request)


def admin_removeproduct(request):
    if admin_check(request):

        if request.method == 'POST':
            form = AdminRemoveProductsForm(request.POST)
            if form.is_valid():
                prod = Product.objects.get(id=form.cleaned_data['id'])
                LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Product).pk, object_id=prod.id, object_repr=prod.name, action_flag=3)
                Product.objects.filter(id=form.cleaned_data['id']).delete()
                
                return redirect('admin_products')

        return admin_products(request)
    else:
        return redirect_user(request)

      
def admin_logs(request):
    if admin_check(request):
        logs = LogEntry.objects.all()
        # buyer_count = option
        return render(request, 'admin/admin_logs.html', {
            'name': 'admin_logs',
            'logs': logs,
        })
    else:
        return redirect_user(request)


def seller_registration(request):
    return render(request, 'seller/seller_registration.html', {'name': 'seller_registration'})

def seller_check(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return user_profile.is_seller
        except UserProfile.DoesNotExist:
            raise Http404()
    else:
        return False 
  
def showAllProducts(request):
    if(seller_check(request=request)):
        authenticated_seller= Seller.objects.get(user=request.user)
        if(authenticated_seller.approved and authenticated_seller.applied ):
            if(seller_check(request)):
                return render(request, 'seller/all_products.html', {"object_list":Product.objects.filter(Q(seller=authenticated_seller))})
            else:   
                return redirect_user(request)
        elif(not authenticated_seller.approved):
            return redirect("unapproved")
        else:
            return redirect("rejected")
    else: return redirect_user(request=request)   
        

def addProductFormView(request):
    if(seller_check(request=request)):   
        form =AddProductForm(request.POST or None,request.FILES)
        if(form.is_valid()):
            model =form.save(commit=False)
        
            model.seller=Seller.objects.get(Q(user = request.user))
            model.save()
            form =AddProductForm()
            LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Product).pk, object_id=model.id, object_repr=model.name, action_flag=1)

            return redirect('seller_all_products')

        context={
            'form':form,
            'editing':False
        }
        return render(request, "seller/add_product.html", context)
    else :
      return redirect_user(request=request )
    
def editProductFormView(request, id):
    if(seller_check(request)):
        authenticated_seller= Seller.objects.get(user=request.user)
        if(authenticated_seller.approved and authenticated_seller.applied ):
            form =AddProductForm(request.POST or None,request.FILES)
            if(form.is_valid()):
                if(current_product.seller==authenticated_seller):
                    model =form.save(commit=False)
                    model.seller=Seller.objects.filter(id__exact=request.user.id)[0]
                    model.save()
                    form =AddProductForm()
                model =form.save(commit=False)
            
                model.seller=Seller.objects.get(Q(user = request.user))
                model.save()
                form =AddProductForm()
                return redirect('seller_all_products')

            context={
                'form':form,
                'editing':False
            }
            return render(request, "seller/add_product.html", context)
        else: redirect_user(request=request)
    else :
      return redirect_user(request=request )
    
class EditProductView(UpdateView) :
    model = Product
    fields=['name','price','description', 'quantity','category', 'image1','image2']
    template_name="seller/add_product.html"
    success_url =reverse_lazy('seller_all_products') 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editing"]=True
        return context
    def get_object(self):
        obj = super().get_object()
        if obj.seller.user != self.request.user:
            raise Http404
        obj.save()
        return obj
    def form_valid(self, form):
        # The super call to form_valid creates a model instance
        # under self.object.
        response = super(EditProductView, self).form_valid(form)

        # Do custom stuff here...
        LogEntry.objects.log_action(user_id=self.request.user.id, content_type_id=ContentType.objects.get_for_model(Product).pk, object_id=self.object.id, object_repr=self.object.name, action_flag=2)

        return response
  
class RemoveProductView(DeleteView) :
    model = Product
    
    template_name="seller/remove_product.html"
    success_url =reverse_lazy('seller_all_products') 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editing"]=True
        return context

    def get_object(self):
        obj = super().get_object()
        if obj.seller.user != self.request.user:
            raise Http404
        if self.request.method == 'POST':
            LogEntry.objects.log_action(user_id=self.request.user.id, content_type_id=ContentType.objects.get_for_model(Product).pk, object_id=obj.id, object_repr=obj.name, action_flag=3)
        return obj
     
        

def logoutView(request):
    logout(request)
    return redirect('login')


def seller_removeproduct(request):
    if(seller_check(request=request) and request.method == 'POST'):
        auth_seller=Seller.objects.get(user=request.user)
        form = SellerRemoveProductsForm(request.POST)
        product=Product.objects.get(id=request.POST['pk'])
        if(product.seller==auth_seller):
            if form.is_valid():
                if(product.seller==auth_seller):
                    Product.objects.filter(id=request.POST['id']).delete()

                return redirect("seller_all_products")
            return redirect_user(request)
        else:
          return redirect_user(request)
    else:
      return redirect_user(request)
    
def editProfileView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_verified:
            return redirect('login')
        address_form = None
        if request.method == 'POST':
            if user_profile.is_seller:
                form = SellerProfileForm(request.POST, instance=user_profile)
                seller = Seller.objects.get(user=request.user)
                if form.is_valid():
                    # form.save()
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    company_name = form.cleaned_data['company_name']
                    gst_number = form.cleaned_data['gst_number']
                    if first_name != '':
                        seller.user.first_name = first_name
                    if last_name != '':
                        seller.user.last_name = last_name
                    if company_name != '':
                        seller.company_name = company_name
                    if gst_number != '':
                        seller.gst_number = gst_number
                    seller.user.save()
                    seller.save()
                    LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Seller).pk, object_id=seller.user.id, object_repr=seller.user.username, action_flag=2)

                    return redirect('edit_profile')
            elif user_profile.is_buyer:
                form = BuyerProfileForm(request.POST, instance=user_profile)
                buyer = Buyer.objects.get(user=request.user)
                address_form = AddressForm(
                    request.POST, instance=buyer.address)
                if address_form.is_valid():
                    address_form.save()
                if form.is_valid():
                    # form.save()
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    if first_name != '':
                        buyer.user.first_name = first_name
                    if last_name != '':
                        buyer.user.last_name = last_name
                    buyer.user.save()
                    buyer.save()
                    LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Buyer).pk, object_id=buyer.user.id, object_repr=buyer.user.username, action_flag=2)
                    return redirect('edit_profile')
            else:
                return HttpResponseNotFound()
        else:
            if user_profile.is_seller:
                seller = Seller.objects.get(user=request.user)
                form = SellerProfileForm(initial={
                    'email': seller.user.email,
                    'username': seller.user.username,
                    'first_name': seller.user.first_name,
                    'last_name': seller.user.last_name,
                    'company_name': seller.company_name,
                    'gst_number': seller.gst_number
                })
            elif user_profile.is_buyer:
                buyer = Buyer.objects.get(user=request.user)
                form = BuyerProfileForm(initial={
                    'email': buyer.user.email,
                    'username': buyer.user.username,
                    'first_name': buyer.user.first_name,
                    'last_name': buyer.user.last_name
                })
                address = buyer.address
                address_form = AddressForm(initial={
                    "address1": address.address1,
                    "address2": address.address2,
                    "city": address.city,
                    "zipcode": address.zipcode,
                    "country": address.country
                })
            else:
                return HttpResponseNotFound()
    except (UserProfile.DoesNotExist, Buyer.DoesNotExist, Seller.DoesNotExist):
        raise Http404()
    return render(request, 'general/edit_profile.html',
                  {
                      'form': form,
                      'address_form': address_form,
                      'is_buyer': user_profile.is_buyer
                  })


def deleteAccountRequest(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_verified:
            return redirect('login')
        if request.method == 'POST':
            # send mail to user with new otp and link to verify
            otp = getRandomNumber()
            user_profile.otp = otp
            nextTime = datetime.datetime.now() + datetime.timedelta(minutes=15)
            user_profile.otp_expiry = nextTime
            send_mail('Your OTP for account deletion (Kyntra): ', 'OTP to delete your account is {}'.format(
                otp), settings.EMAIL_HOST_USER, [request.user.email], fail_silently=False)
            user_profile.save()
            return render(request, 'general/delete_account.html')
        else:
            return HttpResponseNotFound()
    except UserProfile.DoesNotExist:
        raise Http404()
def deleteAccount(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_verified:
            return redirect('login')
        if request.method == 'POST':
            if str(user_profile.otp) == str(request.POST['otp']) and user_profile.otp_expiry > datetime.datetime.now(datetime.timezone.utc):
                if user_profile.is_seller:
                    seller = Seller.objects.get(user=request.user)
                    LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Seller).pk, object_id=seller.user.id, object_repr=seller.user.username, action_flag=3)
                    logout(request)
                    user_profile.user.delete()
                    user_profile.delete()
                    seller.delete()
                elif user_profile.is_buyer:
                    buyer = Buyer.objects.get(user=request.user)
                    LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(Buyer).pk, object_id=buyer.user.id, object_repr=buyer.user.username, action_flag=3)
                    logout(request)
                    user_profile.user.delete()
                    user_profile.delete()
                    buyer.address.delete()
                    buyer.delete()
                return redirect('login')
            else:
                user_profile.otp_expiry = datetime.datetime.now(
                    datetime.timezone.utc)
                user_profile.save()
                return redirect('edit_profile')
    except (UserProfile.DoesNotExist, Seller.DoesNotExist, Buyer.DoesNotExist):
        raise Http404()
    return render(request, 'general/delete_account.html')
# rejected_seller

def rejected_seller(request):
    return render(request, 'seller/unapproved_user.html',{"heading":"Application Rejected","message":"Please note: Your Application has been rejected. Please revise your application and apply again.","reject":True})
def unapproved_seller(request):
    return render(request, 'seller/unapproved_user.html',{"heading":"Not Verified!","message":"Please wait till our admin accepts your request!!!","reject":False})