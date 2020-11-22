from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from application.models import ApplicationByCommissioner, RefusalOfApplicationByDispatcher, ApplicationByDispatcher, \
    Decision, ClosedApplication, PhotoForApplicationByCommissioner
from road.models import Point
from django.forms import widgets, SelectDateWidget, SplitDateTimeWidget

from users.models import Dispatcher, Commissioner


def clean_data(self, obj):
    cleaned_data = super(obj, self).clean()
    if cleaned_data['location'] < 10 or cleaned_data['location'] > 999:
        self.add_error('location', 'неверное значение')
    if cleaned_data['comment'] == '':
        self.add_error('comment', 'комментарий обязателен')
    return cleaned_data


class CreateDispatcherApplicationsForm(forms.Form):
    point = forms.ChoiceField(label='Точка', choices=[], required=True)
    comment = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        max_length=1000,
    )
    come_from_user = forms.BooleanField(required=False)
    location = forms.IntegerField()

    class Meta:
        widgets = {
            'comment': widgets.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateDispatcherApplicationsForm, self).__init__(*args, **kwargs)
        point_choices = [(x.id, x.get_name_with_section()) for x in
                         Point.objects.filter(section=user.dispatcher.section).order_by('name')]
        self.fields['point'].choices = point_choices

    def clean(self):
        return clean_data(self, CreateDispatcherApplicationsForm)


class ApplicationByCommissionerCreateForm(forms.ModelForm):
    class Meta:
        model = ApplicationByCommissioner
        fields = ['need_ambulance', 'need_police', 'need_mchs', 'need_tow_truck', 'comment', 'location']
        widgets = {
            'comment': widgets.Textarea(),
        }

    def clean(self):
        return clean_data(self, ApplicationByCommissionerCreateForm)


class PhotoForApplicationByCommissionerForm(forms.Form):
    images = forms.ImageField(widget=widgets.FileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(PhotoForApplicationByCommissionerForm, self).__init__(*args, **kwargs)

    def clean_images(self):
        # Остаются только картинки
        images = [photo for photo in self.request.FILES.getlist('images') if 'image' in photo.content_type]
        # Если среди загруженных файлов картинок нет, то исключение
        if len(images) == 0:
            raise forms.ValidationError(u'Not found uploaded photos.')
        return images

    def save_for(self, app):
        for photo in self.clean_images():
            PhotoForApplicationByCommissioner(image=photo, application_by_commissioner=app).save()


class RefusalOfApplicationByDispatcherCreateForm(forms.ModelForm):
    class Meta:
        model = RefusalOfApplicationByDispatcher
        fields = '__all__'
        widgets = {
            'comment': widgets.Textarea(),
        }

    def clean(self):
        cleaned_data = super(RefusalOfApplicationByDispatcherCreateForm, self).clean()
        if cleaned_data['comment'] == '':
            self.add_error('comment', 'комментарий обязателен')
        return cleaned_data


class ChangePointInApplicationByDispatcherForm(forms.ModelForm):
    class Meta:
        model = ApplicationByDispatcher
        fields = ['point']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChangePointInApplicationByDispatcherForm, self).__init__(*args, **kwargs)
        point_choices = [(x.id, x.get_name_with_section()) for x in
                         Point.objects.filter(section=user.dispatcher.section).order_by('name')]
        self.fields['point'].choices = point_choices


class DecisionCreateForm(forms.ModelForm):

    class Meta:
        model = Decision
        fields = ['called_ambulance', 'called_police', 'called_mchs', 'called_tow_truck', 'comment']
        widgets = {
            'comment': widgets.Textarea(),
        }


class CloseCommissionerApplicationForm(forms.ModelForm):

    class Meta:
        model = ClosedApplication
        fields = ['comment']
        widgets = {
            'comment': widgets.Textarea(),
        }


class GetReportForm(forms.Form):
    date_from = forms.DateField(required=True, widget=SelectDateWidget())
    date_to = forms.DateField(required=True, widget=SelectDateWidget())
    status = forms.ChoiceField(
        label=u'Статуы',
        choices=[
            ('', ''),
            (ApplicationByCommissioner.STATUS.NEW, 'новая'),
            (ApplicationByCommissioner.STATUS.SENT, 'отправлена'),
            (ApplicationByCommissioner.STATUS.IN_WORK, 'в работе'),
            (ApplicationByCommissioner.STATUS.DECISION, 'принято решение'),
            (ApplicationByCommissioner.STATUS.SERVICE_PROVIDED, 'услуга оказана'),
            (ApplicationByCommissioner.STATUS.CLOSED, 'закрыта')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    def clean(self):
        cleaned_data = super(GetReportForm, self).clean()
        if cleaned_data['date_from'] > cleaned_data['date_to']:
            self.add_error('date_from', 'неверно заданы даты')
        return cleaned_data
