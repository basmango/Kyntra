from django.db.models.deletion import PROTECT
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, request
from django.views.generic.list import ListView
from ecommerce.models import Buyer, ProductImage, Seller, ShippingAddress, UserProfile, Product, Category
from django.db.models import Q
from .forms import AddressForm, BuyerSignUpForm, SellerSignUpForm,AddProductForm,SellerRemoveProductsForm


class SearchProductListView(ListView):
	model = Product
	paginate_by = 15
	template_name = 'general/home.html'

	def get_queryset(self): # new
		query = self.request.GET.get('product')
		if not(query):
			return  Product.objects.all()
		object_list = Product.objects.filter(
			Q(name__icontains=query) )
		
		return object_list

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		query = self.request.GET.get('product')
		if query==None:
			query=""
			
		context['title'] = f"Search results for '{query}' "
		context['additional_q_params_for_pagination']  = f"product={query}"
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


def buyer_signup(request):
	if request.method == 'POST':
		form = BuyerSignUpForm(request.POST)
		address_form = AddressForm(request.POST)
		if form.is_valid() and address_form.is_valid():
			user = form.save()
			address = address_form.save()
			user.refresh_from_db()
			Buyer.objects.create(user=user, address=address)
			user.save()
			address.save()
			raw_password = form.cleaned_data.get('password1')
			# login user after signing up
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)            
			return redirect('index')
	else:
		form = BuyerSignUpForm()
		address_form = AddressForm()

	return render(request,'registration/buyer_signup.html',{'form': form, "address_form": address_form})

def seller_signup(request):
	if request.method == 'POST':
		form = SellerSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			Seller.objects.create(user=user, company_name=form.cleaned_data.get('company_name'), gst_number=form.cleaned_data.get('gst_number'))
			user.save()
			raw_password = form.cleaned_data.get('password1')
			# login user after signing up
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			# TODO Change to seller registration for document upload etc.
			return redirect('index')
	else:
		form = SellerSignUpForm()

	return render(request,'registration/seller_signup.html', {'form': form})



def index(request):
	return render(request, 'general/home.html')


def admin_dashboard(request):
	buyers = Buyer.objects.all()
	sellers = Seller.objects.all()
	pending = sellers.filter(applied = True, application_status = False )
	products = Product.objects.all()
	b = len(buyers)
	s = len(sellers)
	pen = len(pending)
	p = len(products)

	return render(request, 'admin/admin_dashboard.html', {
		'name': 'admin_dashboard',
		'buyer_count':b,
		'seller_count':s,
		'pending_count':pen,
		'product_count':p})


def admin_buyers(request, option = 'all'):
	buyers = Buyer.objects.all()
	buyer_count = len(buyers)
	# buyer_count = option
	return render(request, 'admin/admin_buyers.html', {
		'name': 'admin_buyers', 
		'option':option, 
		'buyers': buyers, 
		'buyer_count':buyer_count
		})


def admin_sellers(request, option="all"):
	sellers = Seller.objects.all()
	pending = sellers.filter(applied = True, application_status = False )
	approved = sellers.filter(applied = True, application_status = True )
	unapproved = sellers.filter(applied = False )

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
		'option':option, 
		'sellers':sellerlist, 
		'seller_count':seller_count,
		'pending_count':pending_count,
		'approved_count':approved_count,
		'unapproved_count':unapproved_count,
		})

# def admin_sellerapplication	(request):
# 	if request.method == "POST":
# 		request.
# 	# return admin_sellers(request, )


def admin_products(request, option="all"):
	products = []
	product_count = []
	curr = 0

	products.append(Product.objects.all())
	categories = Category.objects.all()

	i=0
	for c in categories:
		i+=1
		products.append(Product.objects.filter(category=Category.objects.filter(name=c.name).get()))
		if c.name == option:
			curr = i
	# product_count = len(sellers)
	for p in products:
		product_count.append(len(p))


	
	return render(request, 'admin/admin_products.html', {
		'name': 'admin_products',
		'option':option, 
		'products':products[curr], 
		'product_count':product_count,
		'categories':categories,
		})



    # http://127.0.0.1:8000/kyntra/seller/all_products/search?query=pho  
def seller_registration(request):
    return render(request, 'seller/seller_registration.html', {'name': 'seller_registration'})

# class SellerAllView(ListView):
#     model=Product
#     template_name='seller/all_products.html'
#     def get_queryset(self): # new
#         return  Product.objects.all()
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "All Products"
#         return context
def showAllProducts(request):
	return render(request, 'seller/all_products.html', {"object_list":Product.objects.all()})

class SellerSearchView(ListView):
    model =Product
    template_name='seller/all_products.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        return Product.objects.filter(name__icontains=query)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = "query"
        return context

def addProductFormView(request):
    form =AddProductForm(request.POST or None)
    if(form.is_valid()):
        model =form.save(commit=False)
        model.seller=Seller.objects.filter(id__exact=request.user.id)[0]
        
        model.save()
        form =AddProductForm()
        return redirect('seller_all_products')

    context={
        'form':form,
        'editing':False
    }
    return render(request, "seller/add_product.html", context)

def editProductFormView(request, id):
    instance=get_object_or_404(Product, id=id)
    form =AddProductForm(request.POST or None, instance=instance)
    if(form.is_valid()):
        model =form.save(commit=False)
        model.seller=Seller.objects.filter(id__exact=request.user.id)[0]
        model.save()
        form =AddProductForm()
        return redirect('seller_all_products')

    context={
        'form':form,
        'editing':True,
        'id':id
    }
    return render(request, "seller/add_product.html", context)


def logoutView(request):
    logout(request)
    return HttpResponse("Logout Successful")

def seller_removeproduct(request):
	if request.method == 'POST':
		form = SellerRemoveProductsForm(request.POST)
		if form.is_valid():
			Product.objects.filter(id=request.POST['id']).delete()
			return HttpResponseRedirect("/kyntra/seller/all_products/")

	return showAllProducts(request)

