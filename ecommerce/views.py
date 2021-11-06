from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.views.generic.list import ListView
from ecommerce.models import Buyer, Seller, ShippingAddress, UserProfile, Product, Category
from django.db.models import Q
from .forms import AddressForm, BuyerSignUpForm, SellerSignUpForm


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
	return render(request, 'admin/admin_dashboard.html', {'name': 'admin_dashboard'})


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
	# seller_count = len(sellers)
	seller_count = 0


	return render(request, 'admin/admin_sellers.html', {
		'name': 'admin_sellers', 
		'option':option, 
		'sellers':sellers, 
		'seller_count':seller_count
		})

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


def seller_all_products(request):
	products = [
		{
			"name": "Phone",
			"price": 100,
			"description":"This is a phone",
			"supertag": "SOLD",
			"image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
		},
		{
			"name": "Phone",
			"price": 100,
			"description":"This is a phone",
			"supertag": "SOLD",
			"image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
		},
		
		{
			"name": "Phone",
			"price": 100,
			"description":"This is a phone",
			"supertag": "SOLD",
			"image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
		},
		{
			"name": "Phone",
			"price": 100,
			"description":"This is a phone",
			"supertag": "SOLD",
			"image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
		},
		{
			"name": "Phone",
			"price": 100,
			"description":"This is a phone",
			"supertag": "SOLD",
			"image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
		},
		{
			"name": "Phone",
			"price": 100,
			"description":"This is a phone",
			"supertag": "SOLD",
			"image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
		},
   
	]
	return render(request, 'seller/all_products.html', {'name': 'seller_all_products',"products":products})
def seller_registration(request):
	return render(request, 'seller/seller_registration.html', {'name': 'seller_registration'})