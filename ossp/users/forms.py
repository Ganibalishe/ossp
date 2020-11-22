from django import forms

from road.models import Point
from users.models import Commissioner


class ChangePointCommissionerForm(forms.ModelForm):
    class Meta:
        model = Commissioner
        fields = ['point']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChangePointCommissionerForm, self).__init__(*args, **kwargs)
        point_choices = [(x.id, x.get_name_with_section) for x in
                         Point.objects.filter(section=user.commissioner.section).order_by('name')]
        self.fields['point'].choices = point_choices
