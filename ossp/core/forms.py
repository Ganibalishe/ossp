from django import forms

from users.models import Dispatcher, Commissioner


class AuthorizationForm(forms.Form):
    phone = forms.CharField(max_length=11)
    password = forms.CharField()

    def clean(self):
        cleaned_data = super(AuthorizationForm, self).clean()
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        if not phone and not password:
            return cleaned_data
        if len(phone) == 10:
            cleaned_data['phone'] = '7' + phone
        if phone[0] == '8':
            cleaned_data['phone'] = '7' + phone[1:]
        if len(phone) != 10 and len(phone) != 11:
            self.add_error('phone', 'введите корректный номер телефона')
        elif not (
                Dispatcher.objects.filter(phone=phone, password=password).exists() and not
                Commissioner.objects.filter(phone=phone, password=password).exists()
        ):
            self.add_error('phone', 'нет работника с таким номером телефона или неверный пароль')
        return cleaned_data
