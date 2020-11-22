from django.shortcuts import redirect
from django.views.generic import FormView

from road.models import Point
from users.forms import ChangePointCommissionerForm


class ChangePointCommissionerView(FormView):
    form_class = ChangePointCommissionerForm
    template_name = 'application/com_change_point.html'

    def get_form_kwargs(self):
        user = self.request.user
        form_kwargs = super(ChangePointCommissionerView, self).get_form_kwargs()
        form_kwargs.update({'user': user})
        return form_kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        commissioner = self.request.user.commissioner
        print(cleaned_data)
        commissioner.point = Point.objects.get(name=cleaned_data['point'])
        commissioner.save(update_fields=['point'])
        return redirect('application:commissioner_list')