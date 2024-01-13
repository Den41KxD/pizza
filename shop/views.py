from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from shop.models import Category, Product
from shop.services.services import get_product_by_id, get_filters_by_products, get_filtered_products


def get_default_context():
	extra_context = {'categories': Category.objects.filter(category__isnull=True, hide=False).order_by('position')}
	return extra_context


class CustomBaseView(TemplateView):

	def get_category_by_slug(self):
		return Category.objects.get(slug=self.kwargs['slug'])


class HomePageView(CustomBaseView):
	template_name = 'base.html'

	def get(self, request, *args, **kwargs):
		self.extra_context = get_default_context()
		return super().get(request, *args, **kwargs)


class CategoryPageView(CustomBaseView):
	template_name = 'category.html'

	def get(self, request: WSGIRequest, *args, **kwargs):
		print(request.user)
		self.extra_context = get_default_context()
		self.extra_context['category'] = self.get_category_by_slug()
		category: Category = self.extra_context['category']
		self.extra_context['products'] = category.get_category_products()
		category_breadcrumbs = list(category.get_category_breadcrumbs())
		category_breadcrumbs.reverse()
		self.extra_context['category_breadcrumbs'] = category_breadcrumbs
		self.extra_context['category_filters'] = get_filters_by_products(products=self.extra_context['products'])
		return super().get(request, *args, **kwargs)


class ProductPage(DetailView):
	template_name = 'product_page.html'
	context_object_name = 'product'
	slug_field = 'slug'
	model = Product

	def get(self, request, *args, **kwargs):
		self.extra_context = get_default_context()
		product: Product = self.get_object()
		self.extra_context['category_breadcrumbs'] = product.category.get_category_breadcrumbs()
		self.extra_context['buy_together'] = product.get_buy_together_products()
		response = super().get(request, *args, **kwargs)
		return response


def get_linked_product_info_view(request):
	product_id = int(request.GET.get('product_id'))
	product = get_product_by_id(product_id=product_id)
	return JsonResponse({'price': product.price, 'weight': product.weight}, status=200, safe=False)


def get_filtered_products_view(request):
	filters_ids = request.GET.getlist('active_filters_ids[]')
	category_id = request.GET.get('category_id')
	products = get_filtered_products(category_id=category_id, filter_ids=filters_ids)
	return render(request=request, template_name='includes/products_list_products_only.html', context={'products': products})
