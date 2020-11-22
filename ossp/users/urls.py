from django.urls import path

from users.views import ChangePointCommissionerView

app_name = 'users'

urlpatterns = [
    path(
        r'commissioner/<pk>/change-point/',
        ChangePointCommissionerView.as_view(),
        name='commissioner_change_point'
    ),
]
