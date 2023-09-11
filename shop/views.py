from django.views import generic
from django.http import JsonResponse, Http404
from django.urls import reverse, resolve, reverse_lazy
from urllib.parse import urlparse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from stock import models
from .models import Staff
from .forms import StaffUpdateForm, StaffNewForm, StaffUpdateCredentialForm
import json

# Create your views here.
class HomeView(LoginRequiredMixin, generic.TemplateView):
    login_url = '/accounts/login/'
    template_name = 'shop_home.html'


class CartView(LoginRequiredMixin, generic.ListView):
    back_url = '/shop/'
    login_url = '/accounts/login/'
    model = models.Product
    queryset = models.Product.objects.all()
    template_name = 'cart.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(CartView, self).get_context_data(*args, **kwargs)
        ctx['back_url'] = self.back_url
        return ctx


class CheckoutDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    model = models.Bill
    queryset = models.Bill.objects.all()
    template_name = 'checkout_detail.html'


class StaffListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = {'shop.view_staff',}
    back_url = '/shop/'
    login_url = '/accounts/login/'
    model = Staff
    queryset = Staff.objects.all()
    template_name = 'staff_list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(StaffListView, self).get_context_data(*args, **kwargs)
        ctx['staff_count'] = Staff.objects.count()
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


class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    permission_required = {'shop.view_staff',}
    back_url = '/shop/staffs/'
    login_url = '/accounts/login/'
    model = Staff
    queryset = Staff.objects.all()
    template_name = 'staff_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(StaffDetailView, self).get_context_data(*args, **kwargs)
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


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = {'shop.delete_staff',}
    model = Staff
    template_name = 'staff_delete.html'
    success_url = reverse_lazy('staffs')
    login_url = '/accounts/login/'

    def delete(self, request, *args, **kwargs):
        staff = self.get_object()
        user = staff.user
        staff.user = None
        staff.save()
        user.delete()
        return super().delete(request, *args, **kwargs)


class NewStaffView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = {'shop.add_staff',}
    model = Staff
    form_class = StaffNewForm
    template_name = 'staff_new.html'
    login_url = '/accounts/login/'


class StaffEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = {'shop.change_staff',}
    model = Staff
    form_class = StaffUpdateForm
    template_name = 'staff_edit.html'
    login_url = '/accounts/login/'

    def get_initial(self):
        data = super().get_initial()
        # Extra fields must be populated manually
        data['first_name'] = self.get_object().first_name
        data['last_name'] = self.get_object().last_name
        data['email'] = self.get_object().email
        return data


class StaffCredentialEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = {'shop.change_staff',}
    model = Staff
    form_class = StaffUpdateCredentialForm
    template_name = 'staff_credential_edit.html'
    login_url = '/accounts/login/'

    def get_initial(self):
        data = super().get_initial()
        # Extra fields must be populated manually
        data['username'] = self.get_object().username
        return data


class AccountDetailView(LoginRequiredMixin, generic.DetailView):
    back_url = '/shop/'
    login_url = '/accounts/login/'
    model = Staff
    template_name = 'account_detail.html'

    def get_object(self):
        return self.request.user.staff

    def get_context_data(self, *args, **kwargs):
        ctx = super(AccountDetailView, self).get_context_data(*args, **kwargs)
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


class AcocuntEditView(LoginRequiredMixin, generic.UpdateView):
    model = Staff
    form_class = StaffUpdateForm
    template_name = 'account_edit.html'
    login_url = '/accounts/login/'

    def get_object(self):
        return self.request.user.staff

    def get_initial(self):
        data = super().get_initial()
        # Extra fields must be populated manually
        data['first_name'] = self.get_object().first_name
        data['last_name'] = self.get_object().last_name
        data['email'] = self.get_object().email
        return data


class AccountCredentialEditView(LoginRequiredMixin, generic.UpdateView):
    model = Staff
    form_class = StaffUpdateCredentialForm
    template_name = 'account_credential_edit.html'
    login_url = '/accounts/login/'

    def get_object(self):
        return self.request.user.staff

    def get_initial(self):
        data = super().get_initial()
        # Extra fields must be populated manually
        data['username'] = self.get_object().username
        return data


@csrf_exempt
@login_required
def checkout_response(request):
    response = {
        'checkout': False,
        'url': '',
        'message': ''
    }
    if(request.method == 'POST'):
        cart = request.POST.get('cart')
        if cart != None:
            try:
                print(cart)
                cart = json.loads(cart)
                if(len(cart.keys()) == 0):
                    response['message'] = 'Cart is empty! Add at least one item.'
                else:
                    valid = True
                    # Validating requested JSON-data
                    for key, val in cart.items():
                        item = models.Product.objects.get(pk=int(key))
                        qty = int(val[1])
                        if item is not None and item.quantity >= qty:
                            pass
                        else:
                            valid = False
                            print('Invalid for', key)
                            break
                    # Applying to Database if valid
                    if valid:
                        bill = models.Bill()
                        bill.save()
                        for key, val in cart.items():
                            item = models.Product.objects.get(pk=int(key))
                            qty = int(val[1])
                            sale_item = models.ProductSale(quantity=qty, product=item, bill=bill)
                            sale_item.save()
                        response['url'] = reverse('checkout-detail', args=[str(bill.id)])
                    response['checkout'] = valid
                    response['message'] = 'Checkout successful.' if valid else 'Data Error! Please reset cart & try again.'
            except ValueError:
                response['message'] = 'Data Error! Malformed data.'
            except:
                response['message'] = 'Internal error! Cannot prepare for checkout.'
        else:
            response['message'] = 'Request error! Invalid data in request.'
    return JsonResponse(data=response)
