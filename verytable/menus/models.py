import uuid


from django.contrib.sites.models import Site, SiteManager
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property

from django.utils.translation import ugettext_lazy as _

from verytable.users.models import User


class MenuQuerySet(models.QuerySet):

    def current(self):
        now = timezone.now()
        return self.filter(date__gte=now)


class MenuManager(models.Manager):

    def get_queryset(self):
        return MenuQuerySet(self.model, using=self._db).annotate(pax=Sum('reservation__pax')).order_by('date')

    def current(self):
        return self.get_queryset().current()


class Menu(models.Model):
    """
    Menu represent a dining date.
    """
    date = models.DateTimeField(verbose_name=_("date"))
    title = models.CharField(max_length=100, verbose_name=_("title"))
    presentation = models.TextField(verbose_name=_("presentation"))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("price"))
    capacity = models.IntegerField(verbose_name=_("capacity"))
    picture = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name=_("picture"))
    flyer = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name=_("flyer"))

    objects = MenuManager()

    class Meta:
        verbose_name = _("menus")
        verbose_name_plural = _("menus")
        ordering = ["date"]

    def __str__(self):
        return "{}-{}".format(self.date, self.title)

    def get_absolute_url(self):
        return reverse("menus:menus", kwargs={"pk": self.id})

    @cached_property
    def free_seats(self):
        if self.pax:
            return self.capacity - self.pax
        else:
            return self.capacity

    @cached_property
    def complete(self):
        if self.free_seats == 0:
            return True
        else:
            return False


class Reservation(models.Model):
    """
    A reservation for a given number of people.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name=_("menus"))
    date = models.DateTimeField(verbose_name=_("date"), auto_now_add=True)
    pax = models.IntegerField(verbose_name=_("pax"))
    name = models.CharField(max_length=150, verbose_name=_("name"))
    email = models.EmailField(max_length=254, verbose_name=_("email"))
    mobile = models.CharField(max_length=20, verbose_name=_("mobile"))
    comments = models.TextField(blank=True, null=True, verbose_name=_("comments"))
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, verbose_name=_("code"))
    reservation_code = models.CharField(max_length=25, verbose_name=_('reservation code'))
    validated = models.BooleanField(default=False, verbose_name=_('validated'))
    confirmed = models.BooleanField(default=False, verbose_name=_('confirmed'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name=_("user"))

    class Meta:
        verbose_name = _("reservation")
        verbose_name_plural = _("reservations")
        ordering = ["-date"]

    def __str__(self):
        return "{} {} ({})".format(self.name, self.menu, self.pax)

    def get_absolute_url(self):
        return reverse("menus:reservation", kwargs={"pk": self.id})


# turn around bug in django / modeltranslation
# where default inherited object manager SiteManager
# is patched before makemigrations and not recognized so
# always added back as a new AlterModelManager migration
# TODO: verify if we miss default SiteManager serialized feature

class NoMigrationSiteManager(SiteManager):
    use_in_migrations = False


class SiteProperty(Site):
    objects = NoMigrationSiteManager()
    reservation_code = models.CharField(max_length=25, verbose_name=_('reservation code'), blank=True, null=True)
