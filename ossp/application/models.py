from django.utils import timezone
from random import randint

from django.db import models

from core.models import CreatedUpdatedMixin, UUIDMixin, CreatedAtMixin


class ApplicationByDispatcher(CreatedUpdatedMixin, UUIDMixin):
    class STATUS:
        NEW = 'new'
        SENT = 'sent'
        RETURNED = 'returned'
        ACCEPTED = 'accepted'
        APPLICATION_BY_COM_CREATED = 'app_by_com_created'

        CHOICES = (
            (NEW, 'новая'),
            (SENT, 'отправлена'),
            (RETURNED, 'возвращена'),
            (ACCEPTED, 'принята'),
            (APPLICATION_BY_COM_CREATED, 'создана заявка комиссаром')
        )

    dispatcher = models.ForeignKey(
        'users.Dispatcher',
        verbose_name='диспетчер',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    number = models.CharField(
        'номер заявки',
        max_length=20,
        blank=True,
        help_text='создается автоматически после создания'
    )
    point = models.ForeignKey('road.Point', verbose_name='точка', blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField('статус', max_length=25, choices=STATUS.CHOICES, default=STATUS.NEW)
    comment = models.TextField('комментарий диспетчера', blank=True)
    commissioner = models.ForeignKey(
        'users.Commissioner',
        verbose_name='дорожный комиссар',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    come_from_user = models.BooleanField('заявка от пользователя', default=False)
    location = models.IntegerField('локация', blank=True, null=True)

    class Meta:
        verbose_name = 'заявка от диспетчера'
        verbose_name_plural = 'заявки от диспетчеров'

    def __str__(self):
        return self.number or self.created_at

    @staticmethod
    def get_number_order():
        number = ApplicationByDispatcher._generate_number()
        check_number = ApplicationByDispatcher._check_number(number)
        while not check_number:
            number = ApplicationByDispatcher._generate_number()
            check_number = ApplicationByDispatcher._check_number(number)
        return number

    @staticmethod
    def _generate_number():
        return f'{timezone.localtime().strftime("%Y%m%d")}-{str(randint(int("1" * 6), int("9" * 6)))}'

    @staticmethod
    def _check_number(number):
        if ApplicationByDispatcher.objects.filter(number=number).exists():
            return False
        return True


class ApplicationByCommissioner(CreatedUpdatedMixin, UUIDMixin):

    class STATUS:
        NEW = 'new'
        SENT = 'sent'
        IN_WORK = 'in_work'
        DECISION = 'decision'
        SERVICE_PROVIDED = 'service_provided'
        CLOSED = 'closed'

        CHOICES = (
            (NEW, 'новая'),
            (SENT, 'отправлена'),
            (IN_WORK, 'в работе'),
            (DECISION, 'принято решение'),
            (SERVICE_PROVIDED, 'услуга оказана'),
            (CLOSED, 'закрыта')
        )

    status = models.CharField('статус', max_length=25, choices=STATUS.CHOICES, default=STATUS.NEW)
    application_by_dispatcher = models.ForeignKey(
        'ApplicationByDispatcher',
        verbose_name='заявка от диспетчера',
        related_name='app_by_com',
        help_text='указывается если заявка пришла от диспетчека',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    number = models.CharField(
        'номер заявки',
        max_length=20,
        blank=True,
        help_text='создается автоматически после создания'
    )
    commissioner = models.ForeignKey(
        'users.Commissioner',
        verbose_name='комиссар',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    point = models.ForeignKey('road.Point', verbose_name='точка', blank=True, null=True, on_delete=models.SET_NULL)
    need_ambulance = models.BooleanField('нужна скорая?', default=False)
    need_police = models.BooleanField('нужна полиция?', default=False)
    need_mchs = models.BooleanField('нужен мчс?', default=False)
    need_tow_truck = models.BooleanField('нужен эвакуатор?', default=False)
    comment = models.TextField('комментарий', blank=True)
    location = models.IntegerField('локация', blank=True, null=True)

    class Meta:
        verbose_name = 'заявка от комиссара'
        verbose_name_plural = 'заявки от комиссаров'

    def __str__(self):
        return self.number or self.created_at

    @staticmethod
    def get_number_order():
        number = ApplicationByCommissioner._generate_number()
        check_number = ApplicationByCommissioner._check_number(number)
        while not check_number:
            number = ApplicationByCommissioner._generate_number()
            check_number = ApplicationByCommissioner._check_number(number)
        return number

    @staticmethod
    def _generate_number():
        return f'{timezone.localtime().strftime("%Y%m%d")}-{str(randint(int("1" * 6), int("9" * 6)))}'

    @staticmethod
    def _check_number(number):
        if ApplicationByCommissioner.objects.filter(number=number).exists():
            return False
        return True


class PhotoForApplicationByCommissioner(CreatedAtMixin):

    application_by_commissioner = models.ForeignKey('ApplicationByCommissioner', on_delete=models.CASCADE)
    image = models.ImageField('изображение', upload_to='photo/%Y/%m/%d/')

    class Meta:
        verbose_name = 'фото к заявлению'
        verbose_name_plural = 'фото к заявлениям'


class Decision(CreatedAtMixin, UUIDMixin):
    application_by_commissioner = models.ForeignKey(
        ApplicationByCommissioner,
        verbose_name='заявка',
        related_name='decision',
        on_delete=models.CASCADE,
    )
    dispatcher = models.ForeignKey(
        'users.Dispatcher',
        verbose_name='диспетчер',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    called_ambulance = models.BooleanField('вызвана скорая?', default=False)
    called_police = models.BooleanField('вызвана полиция?', default=False)
    called_mchs = models.BooleanField('вызван мчс?', default=False)
    called_tow_truck = models.BooleanField('вызван эвакуатор?', default=False)
    comment = models.TextField('комментарий', blank=True)

    class Meta:
        verbose_name = 'решение по заявке'
        verbose_name_plural = 'решения по заявкам'

    def __str__(self):
        return f'{self.application_by_commissioner.number} - {self.created_at}'


class RefusalOfApplicationByDispatcher(CreatedAtMixin):
    commissioner = models.ForeignKey(
        'users.Commissioner',
        verbose_name='комиссар',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    comment = models.TextField('комментарий', blank=True)
    application_by_dispatcher = models.ForeignKey(
        'ApplicationByDispatcher',
        verbose_name='заявка от диспетчера',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'отказ от заявки'
        verbose_name_plural = 'отказы от заявок'

    def __str__(self):
        return f'{self.commissioner} - {self.created_at}'


class ClosedApplication(CreatedAtMixin):
    application_by_commissioner = models.ForeignKey(
        ApplicationByCommissioner,
        verbose_name='заявка',
        on_delete=models.CASCADE
    )
    comment = models.TextField('комментрарий')

    class Meta:
        verbose_name = 'закрытая заявка'
        verbose_name_plural = 'закрытые заявки'

