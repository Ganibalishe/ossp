from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from core.forms import AuthorizationForm
from users.models import Dispatcher, Commissioner


class AuthorizationView(TemplateView, FormView):
    template_name = 'authorization/authorization.html'
    form_class = AuthorizationForm

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        if data.get('logout'):
            logout(request)
            return super(AuthorizationView, self).get(self.request)
        phone = data['phone']
        password = data['password']
        if Dispatcher.objects.filter(phone=phone, password=password).exists():
            user = Dispatcher.objects.filter(phone=phone, password=password).first().user
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('application:dispatcher_list')
        else:
            user = Commissioner.objects.filter(phone=phone, password=password).first().user
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('application:commissioner_list')
