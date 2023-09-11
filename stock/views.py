from django.http.response import Http404
from django.views import generic
from django.urls import reverse, reverse_lazy, resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from urllib.parse import urlparse
from . import models, forms
from datetime import date

# Create your views here.
class HomeView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    permission_required = {'stock.view_product', 'stock.view_category', 'stock.view_productsale', 'stock.view_bill',}
    back_url = '/'
    login_url = '/accounts/login/'
    template_name = 'stock_home.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(HomeView, self).get_context_data(*args, **kwargs)
        ctx['back_url'] = self.back_url
        return ctx


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = {'stock.view_category',}
    back_url = '/stock/'
    login_url = '/accounts/login/'
    model = models.Category
    queryset = models.Category.objects.all()
    template_name = 'category_list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(CategoryListView, self).get_context_data(*args, **kwargs)
        ctx['category_count'] = models.Category.objects.count()
        ctx['categories_max_product'] = sorted(list(category for category in models.Category.objects.all()), key=lambda x:x.product_count, reverse=True)[:5]
        ctx['categories_max_value'] = sorted(list(category for category in models.Category.objects.all()), key=lambda x:x.weight, reverse=True)[:5]
        # Back url
        back = self.request.GET.get('back', None)
        if back:
            try:
                parsed = urlparse(back)
                b = resolve(parsed.path)
                path = reverse(b.url_name, kwargs=b.kwargs)
                if path:
                    self.back_url = path
                    if parsed.query:
                        self.back_url += ('?' + parsed.query)
            except Http404:
                pass
        ctx['back_url'] = self.back_url
        return ctx


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = {'stock.view_product', 'stock.view_productsale',}
    back_url = '/stock/'
    login_url = '/accounts/login/'
    model = models.Product
    queryset = models.Product.objects.all()
    template_name = 'product_list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(ProductListView, self).get_context_data(*args, **kwargs)
        ctx['product_count'] = models.Product.objects.count()
        available_count = len(list(product for product in models.Product.objects.all() if product.available))
        ctx['available_product_count'] = available_count
        ctx['unavailable_product_count'] = ctx['product_count'] - available_count
        ctx['total_stock_cost'] = sum(product.cost*product.quantity for product in models.Product.objects.all())
        ctx['total_stock_price'] = sum(product.price*product.quantity for product in models.Product.objects.all())
        ctx['total_profit'] = ctx.get('total_stock_price', 0.0) - ctx.get('total_stock_cost', 0.0)
        ctx['top_sold_products'] = sorted(list(product for product in models.Product.objects.all()), key=lambda x:x.weight, reverse=True)[:10]
        # Back url
        back = self.request.GET.get('back', None)
        if back:
            try:
                parsed = urlparse(back)
                b = resolve(parsed.path)
                path = reverse(b.url_name, kwargs=b.kwargs)
                if path:
                    self.back_url = path
                    if parsed.query:
                        self.back_url += ('?' + parsed.query)
            except Http404:
                pass
        ctx['back_url'] = self.back_url
        return ctx


class BillListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = {'stock.view_bill',}
    back_url = '/stock/'
    login_url = '/accounts/login/'
    model = models.Bill
    queryset = models.Bill.objects.all()
    template_name = 'bill_list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(BillListView, self).get_context_data(*args, **kwargs)
        # Today
        today = date.today()
        qbill_today = models.Bill.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)
        qsale_today = models.ProductSale.objects.filter(bill__date__year=today.year, bill__date__month=today.month, bill__date__day=today.day)
        ctx['today_bill_count'] = qbill_today.count()
        ctx['today_sale_count'] = qsale_today.count()
        ctx['today_total_cost'] = sum(list(sale.cost*sale.quantity for sale in qsale_today))
        ctx['today_total_price'] = sum(list(sale.price*sale.quantity for sale in qsale_today))
        ctx['today_profit'] = ctx.get('today_total_price', 0.0) - ctx.get('today_total_cost', 0.0)
        # Month
        qbill_month = models.Bill.objects.filter(date__year=today.year, date__month=today.month)
        qsale_month = models.ProductSale.objects.filter(bill__date__year=today.year, bill__date__month=today.month)
        ctx['month_bill_count'] = qbill_month.count()
        ctx['month_sale_count'] = qsale_month.count()
        ctx['month_total_cost'] = sum(list(sale.cost*sale.quantity for sale in qsale_month))
        ctx['month_total_price'] = sum(list(sale.price*sale.quantity for sale in qsale_month))
        ctx['month_profit'] = ctx.get('month_total_price', 0.0) - ctx.get('month_total_cost', 0.0)
        # All time
        ctx['bill_count'] = models.Bill.objects.count()
        ctx['sale_count'] = models.ProductSale.objects.count()
        ctx['total_cost'] = sum(list(sale.cost*sale.quantity for sale in models.ProductSale.objects.all()))
        ctx['total_price'] = sum(list(sale.price*sale.quantity for sale in models.ProductSale.objects.all()))
        ctx['profit'] = ctx.get('total_price', 0.0) - ctx.get('total_cost', 0.0)
        # Back url
        back = self.request.GET.get('back', None)
        if back:
            try:
                parsed = urlparse(back)
                b = resolve(parsed.path)
                path = reverse(b.url_name, kwargs=b.kwargs)
                if path:
                    self.back_url = path
                    if parsed.query:
                        self.back_url += ('?' + parsed.query)
            except Http404:
                pass
        ctx['back_url'] = self.back_url
        return ctx


class CategoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    permission_required = {'stock.view_category',}
    back_url = '/stock/categories/'
    login_url = '/accounts/login/'
    model = models.Category
    queryset = models.Category.objects.all()
    template_name = 'category_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        ctx['product_list'] = self.object.product_set.all()
        ctx['product_sales'] = models.ProductSale.objects.filter(product__category = self.object).all()
        # Back url
        back = self.request.GET.get('back', None)
        if back:
            try:
                parsed = urlparse(back)
                b = resolve(parsed.path)
                path = reverse(b.url_name, kwargs=b.kwargs)
                if path:
                    self.back_url = path
                    if parsed.query:
                        self.back_url += ('?' + parsed.query)
            except Http404:
                pass
        ctx['back_url'] = self.back_url
        return ctx


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    permission_required = {'stock.view_product', 'stock.view_productsale',}
    back_url = '/stock/products/'
    login_url = '/accounts/login/'
    model = models.Product
    queryset = models.Product.objects.all()
    template_name = 'product_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        ctx['product_sales'] = models.ProductSale.objects.filter(product=self.object)
        ctx['stock_cost'] = self.object.cost * self.object.quantity
        ctx['stock_price'] = self.object.price * self.object.quantity
        # Back url
        back = self.request.GET.get('back', None)
        if back:
            try:
                parsed = urlparse(back)
                b = resolve(parsed.path)
                path = reverse(b.url_name, kwargs=b.kwargs)
                if path:
                    self.back_url = path
                    if parsed.query:
                        self.back_url += ('?' + parsed.query)
            except Http404:
                pass
        ctx['back_url'] = self.back_url
        return ctx


class BillDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    permission_required = {'stock.view_bill',}
    back_url = '/stock/bills/'
    login_url = '/accounts/login/'
    model = models.Bill
    queryset = models.Bill.objects.all()
    template_name = 'bill_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(BillDetailView, self).get_context_data(*args, **kwargs)
        # Back url
        back = self.request.GET.get('back', None)
        if back:
            try:
                parsed = urlparse(back)
                b = resolve(parsed.path)
                path = reverse(b.url_name, kwargs=b.kwargs)
                if path:
                    self.back_url = path
                    if parsed.query:
                        self.back_url += ('?' + parsed.query)
            except Http404:
                pass
        ctx['back_url'] = self.back_url
        return ctx


class CategoryEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = {'stock.change_category',}
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'category_edit.html'
    login_url = '/accounts/login/'


class ProductEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = {'stock.change_product', 'stock.change_productsale',}
    model = models.Product
    form_class = forms.ProductUpdateForm
    template_name = 'product_edit.html'
    login_url = '/accounts/login/'


class ProductStockEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = {'stock.change_product', 'stock.change_productsale',}
    model = models.Product
    form_class = forms.ProductStockForm
    template_name = 'product_stock_edit.html'
    login_url = '/accounts/login/'

    def form_valid(self, form):
        if form.is_valid():
            new_instance = form.save(commit=False)
            action = form.cleaned_data.get('action', 'no')
            qty = form.cleaned_data.get('add_qty', 0)
            print(new_instance.quantity, qty, action)
            if action != 'no':
                if action == 'add':
                    new_instance.quantity += qty
                else:
                    new_instance.quantity -= qty
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = {'stock.delete_category',}
    model = models.Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('categories')
    login_url = '/accounts/login/'


class NewCategoryView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = {'stock.add_category',}
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'category_new.html'
    login_url = '/accounts/login/'


class NewProductView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = {'stock.add_product', 'stock.add_productsale'}
    model = models.Product
    form_class = forms.ProductNewForm
    template_name = 'product_new.html'
    login_url = '/accounts/login/'


