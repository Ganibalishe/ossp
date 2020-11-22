import csv

from django.core.files.storage import FileSystemStorage
import datetime
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, DetailView

from application.forms import CreateDispatcherApplicationsForm, ApplicationByCommissionerCreateForm, \
    RefusalOfApplicationByDispatcherCreateForm, ChangePointInApplicationByDispatcherForm, DecisionCreateForm, \
    CloseCommissionerApplicationForm, PhotoForApplicationByCommissionerForm, GetReportForm
from application.models import ApplicationByDispatcher, ApplicationByCommissioner, RefusalOfApplicationByDispatcher, \
    Decision, ClosedApplication, PhotoForApplicationByCommissioner
from road.models import Point


class DispatcherApplicationsListView(TemplateView):
    template_name = 'application/dispatcher_application_list.html'

    def get_context_data(self):
        context = super(DispatcherApplicationsListView, self).get_context_data()
        dispatcher = self.request.user.dispatcher
        context['applications_by_dispatcher'] = ApplicationByDispatcher.objects.filter(
            dispatcher=dispatcher
        ).order_by(
            '-created_at'
        )
        dispatcher_point_id = Point.objects.filter(section=dispatcher.section).values_list('id', flat=True)
        context['applications_by_commissioners'] = ApplicationByCommissioner.objects.filter(
            point__id__in=dispatcher_point_id
        ).order_by(
            '-created_at'
        )
        return context


class DispatcherApplicationsCreateView(FormView):
    form_class = CreateDispatcherApplicationsForm
    template_name = 'application/create_disp_app.html'

    def get_form_kwargs(self):
        user = self.request.user
        form_kwargs = super(DispatcherApplicationsCreateView, self).get_form_kwargs()
        form_kwargs.update({'user': user})
        return form_kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        dispatcher = self.request.user.dispatcher
        number = ApplicationByDispatcher.get_number_order()
        ApplicationByDispatcher.objects.create(
            dispatcher=dispatcher,
            number=number,
            point=Point.objects.get(id=cleaned_data['point']),
            location=cleaned_data['location'],
            status=ApplicationByDispatcher.STATUS.SENT,
            comment=cleaned_data['comment'],
            come_from_user=cleaned_data['come_from_user'],
        )
        return redirect('application:dispatcher_list')


class DispatcherApplicationsDetailView(DetailView):
    model = ApplicationByDispatcher
    template_name = 'application/detail_disp_app.html'


class DispatcherApplicationsAcceptedView(DetailView):
    model = ApplicationByDispatcher

    template_name = 'application/disp_app_accepted.html'

    def post(self, request, *args, **kwargs):
        app = self.get_object()
        app = ApplicationByDispatcher.objects.get(id=self.kwargs.get('pk'))
        app.status = ApplicationByDispatcher.STATUS.ACCEPTED
        app.commissioner = self.request.user.commissioner
        app.save(update_fields=['status', 'commissioner'])
        return redirect('application:commissioner_list')


class ApplicationByCommissionerListView(TemplateView):
    template_name = 'application/commissioner_app_list.html'

    def get_context_data(self):
        context = super(ApplicationByCommissionerListView, self).get_context_data()
        commissioner = self.request.user.commissioner
        applications_by_dispatcher = ApplicationByDispatcher.objects.filter(
            Q(point=commissioner.point, status=ApplicationByDispatcher.STATUS.SENT) | Q(commissioner=commissioner)
        ).order_by(
            '-created_at'
        )
        context['applications_by_dispatcher'] = applications_by_dispatcher
        context['applications_by_commissioner'] = ApplicationByCommissioner.objects.filter(
            commissioner=commissioner
        ).order_by(
            '-created_at'
        )
        return context


class ApplicationByCommissionerCreateView(FormView):
    form_class = ApplicationByCommissionerCreateForm
    form_images_class = PhotoForApplicationByCommissionerForm
    template_name = 'application/create_com_app.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form_images = self.form_images_class()
        return render(request, self.template_name, {'form': form, 'form_images': form_images})

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        print(self.request.POST)
        print(self.request.FILES)
        images = self.request.FILES
        commissioner = self.request.user.commissioner
        number = ApplicationByCommissioner.get_number_order()
        app = ApplicationByCommissioner.objects.create(
            status=ApplicationByCommissioner.STATUS.SENT,
            number=number,
            commissioner=commissioner,
            point=commissioner.point,
            need_ambulance=cleaned_data['need_ambulance'],
            need_police=cleaned_data['need_police'],
            need_mchs=cleaned_data['need_mchs'],
            need_tow_truck=cleaned_data['need_tow_truck'],
            comment=cleaned_data['comment'],
            location=cleaned_data['location']
        )
        form_images = self.form_images_class(self.request.POST, self.request.FILES, request=self.request)
        form_images.save_for(app)
        if self.kwargs.get('pk'):
            app_by_dispatcher = ApplicationByDispatcher.objects.get(id=self.kwargs['pk'])
            app.application_by_dispatcher = app_by_dispatcher
            app.number = app_by_dispatcher.number
            app.save(update_fields=['application_by_dispatcher', 'number'])

            app_by_dispatcher.status = ApplicationByDispatcher.STATUS.APPLICATION_BY_COM_CREATED
            app_by_dispatcher.commissioner = commissioner
            app_by_dispatcher.save(update_fields=['status', 'commissioner'])

        return redirect('application:commissioner_list')


class ApplicationByCommissionerDetailView(DetailView):
    model = ApplicationByCommissioner
    template_name = 'application/commissioner_app_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationByCommissionerDetailView, self).get_context_data()
        application_by_commissioner = ApplicationByCommissioner.objects.get(id=self.kwargs.get('pk'))
        decision = Decision.objects.filter(
            application_by_commissioner=application_by_commissioner
        ).first()
        context['decision'] = decision
        closed_app = ClosedApplication.objects.filter(application_by_commissioner=application_by_commissioner).first()
        context['closed_app'] = closed_app
        images = PhotoForApplicationByCommissioner.objects.filter(
            application_by_commissioner=application_by_commissioner
        )
        context['images'] = images
        return context


class RefusalOfApplicationByDispatcherCreateView(FormView):
    form_class = RefusalOfApplicationByDispatcherCreateForm
    template_name = 'application/create_refusal.html'

    def form_valid(self, form):
        app = ApplicationByDispatcher.objects.get(id=self.kwargs.get('pk'))
        cleaned_data = form.cleaned_data
        commissioner = self.request.user.commissioner
        RefusalOfApplicationByDispatcher.objects.create(
            comment=cleaned_data['comment'],
            commissioner=commissioner,
            application_by_dispatcher=app
        )
        app.status = ApplicationByDispatcher.STATUS.RETURNED
        app.point = None
        app.save(update_fields=['status', 'point'])
        return redirect('application:commissioner_list')


class ChangePointInApplicationByDispatcherView(FormView):
    form_class = ChangePointInApplicationByDispatcherForm
    template_name = 'application/change_point_in_app.html'

    def get_form_kwargs(self):
        user = self.request.user
        form_kwargs = super(ChangePointInApplicationByDispatcherView, self).get_form_kwargs()
        form_kwargs.update({'user': user})
        return form_kwargs

    def get_context_data(self, **kwargs):
        ctx = super(ChangePointInApplicationByDispatcherView, self).get_context_data(**kwargs)
        application = ApplicationByDispatcher.objects.get(id=self.request.GET.get('pk'))
        ctx['application'] = application
        ctx['refusals'] = RefusalOfApplicationByDispatcher.objects.filter(application_by_dispatcher=application)
        return ctx

    def form_valid(self, form):
        app = ApplicationByDispatcher.objects.get(id=self.request.POST.get('app_id'))
        app.point = Point.objects.get(id=self.request.POST.get('point'))
        app.status = ApplicationByDispatcher.STATUS.SENT
        app.save(update_fields=['point', 'status'])
        return redirect('application:dispatcher_list')


class DecisionCreateView(FormView):
    form_class = DecisionCreateForm
    template_name = 'application/create_decision.html'

    def form_valid(self, form):
        app = ApplicationByCommissioner.objects.get(id=self.kwargs.get('pk'))
        cleaned_data = form.cleaned_data
        dispatcher = self.request.user.dispatcher
        Decision.objects.create(
            application_by_commissioner=app,
            dispatcher=dispatcher,
            called_mchs=cleaned_data['called_mchs'],
            called_ambulance=cleaned_data['called_ambulance'],
            called_police=cleaned_data['called_police'],
            called_tow_truck=cleaned_data['called_tow_truck'],
            comment=cleaned_data['comment']
        )
        app.status = ApplicationByCommissioner.STATUS.DECISION
        app.save(update_fields=['status'])
        return redirect('application:dispatcher_list')


class CloseCommissionerApplicationView(FormView):
    form_class = CloseCommissionerApplicationForm
    template_name = 'application/close_application.html'

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        app = ApplicationByCommissioner.objects.get(id=self.kwargs.get('pk'))
        ClosedApplication.objects.create(
            application_by_commissioner=app,
            comment=cleaned_data['comment']
        )
        app.status = ApplicationByCommissioner.STATUS.CLOSED
        app.save(update_fields=['status'])
        return redirect('application:commissioner_list')


class GetReportView(FormView):
    template_name = 'application/get_report.html'
    form_class = GetReportForm

    def form_valid(self, form, *args, **kwargs):
        cleaned_data = form.cleaned_data
        section = self.request.user.dispatcher.section
        print(ApplicationByCommissioner.objects.count())
        applications = ApplicationByCommissioner.objects.filter(
            point__section=section,
            created_at__gte=cleaned_data['date_from'],
            created_at__lte=cleaned_data['date_to']
        )
        for a in applications:
            print(a.status)
        print(cleaned_data['status'])
        if cleaned_data['status']:
            applications = applications.filter(status=cleaned_data['status'])


        kwargs = {
            'successful_date_from': cleaned_data['date_from'],
            'successful_date_to': cleaned_data['date_to']
        }

        decisions = Decision.objects.filter(application_by_commissioner__in=applications)
        closed_applications = ClosedApplication.objects.filter(application_by_commissioner__in=applications)
        data = [
            ['Номер заявки', 'Время создания', 'Статус', 'Время заявки диспетчера', 'Комментарий диспетчера',
             'Комиссар', 'Точка', 'Вызов скорой',
             'Вызов полиции', 'Вызов МЧС', 'Вызов эвакуатора', 'Комментарий комиссара', 'Решение принял диспетчер',
             'Время принятия решения', 'Комментария решения', 'Время закрытия заявки', 'Комментарий к закрытию']
        ]
        for app in applications:
            app_dict = {
                'number': str(app.number),
                'time_created': str(app.created_at.strftime('%d.%m.%y %H:%M')),
                'status': str(app.status),
                'app_disp': str(app.application_by_dispatcher.created_at.strftime('%d.%m.%y %H:%M')) if app.application_by_dispatcher else '-',
                'comment_disp': str(app.application_by_dispatcher.comment) if app.application_by_dispatcher else '-',
                'commissioner': str(app.commissioner.get_full_name()),
                'point': str(app.point.get_name_with_section()),
                'need_ambulance': '+' if app.need_ambulance else '-',
                'need_police': '+' if app.need_police else '-',
                'need_mchs': '+' if app.need_mchs else '-',
                'need_tow_truck': '+' if app.need_tow_truck else '-',
                'comment': str(app.comment),
            }
            if decisions.filter(application_by_commissioner=app).exists():
                decision = decisions.filter(application_by_commissioner=app).first()
                app_dict['decision_disp'] = str(decision.dispatcher.get_full_name())
                app_dict['decision_created'] = str(decision.created_at.strftime('%d.%m.%y %H:%M'))
                app_dict['decision_comment'] = str(decision.comment)
            if closed_applications.filter(application_by_commissioner=app).exists():
                closed = closed_applications.filter(application_by_commissioner=app).first()
                app_dict['closed_created'] = str(closed.created_at.strftime('%d.%m.%y %H:%M'))
                app_dict['closed_comment'] = str(closed.comment)
            data.append(list(app_dict.values()))
        with open(f'{cleaned_data["date_from"]}-{cleaned_data["date_to"]}-{datetime.datetime.now().strftime("%H-%M")}.csv', 'w+') as csv_file:
            writer = csv.writer(csv_file)
            for row in data:
                writer.writerow(row)


        return redirect('application:get_report')
