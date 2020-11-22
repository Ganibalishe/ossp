from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from application.views import DispatcherApplicationsListView, DispatcherApplicationsCreateView, \
    DispatcherApplicationsDetailView, ApplicationByCommissionerListView, ApplicationByCommissionerCreateView, \
    ApplicationByCommissionerDetailView, RefusalOfApplicationByDispatcherCreateView, \
    ChangePointInApplicationByDispatcherView, DecisionCreateView, DispatcherApplicationsAcceptedView, \
    CloseCommissionerApplicationView, GetReportView
from ossp import settings

app_name = 'application'

urlpatterns = [
    path('dispatcher-list/', DispatcherApplicationsListView.as_view(), name='dispatcher_list'),
    path('dispatcher/create/', DispatcherApplicationsCreateView.as_view(), name='create_dispatcher_app'),
    path(r'dispatcher/<uuid:pk>/app/', DispatcherApplicationsDetailView.as_view(), name='detail_app'),
    path(
        r'dispatcher/<uuid:pk>/app/accepted/',
        DispatcherApplicationsAcceptedView.as_view(),
        name='dispatcher_app_accepted'
    ),
    path(
        r'dispatcher/change/',
        ChangePointInApplicationByDispatcherView.as_view(),
        name='change_app_dispatcher'
    ),
    path(r'dispatcher/create_decision/<pk>/', DecisionCreateView.as_view(), name='create_decision'),
    path('commissioner-list/', ApplicationByCommissionerListView.as_view(), name='commissioner_list'),
    path('commissioner/create/', ApplicationByCommissionerCreateView.as_view(), name='create_commissioner_app'),

    path(r'commissioner/create/<uuid:pk>/',
         ApplicationByCommissionerCreateView.as_view(),
         name='create_commissioner_app_by_disp'),
    path('commissioner/<pk>/close/', CloseCommissionerApplicationView.as_view(), name='close_commissioner_app'),
    path(r'refusal/create/<pk>/',
         RefusalOfApplicationByDispatcherCreateView.as_view(),
         name='refusal_create'),
    path(r'commissioner/<uuid:pk>/app/', ApplicationByCommissionerDetailView.as_view(), name='commissioner_detail_app'),

    path(r'report/', GetReportView.as_view(), name='get_report'),

] + static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns.append(path(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}))
