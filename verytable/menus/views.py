import io
import json
import os
import mimetypes
from datetime import date
from urllib.parse import urlparse
import tempfile

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin,
)
from django.forms.models import model_to_dict
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from django.db.models import Q

from . import models, forms


class Homepage(ListView):
    model = models.Menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_menu = models.Menu.objects.current().first()
        if first_menu:
            context["next_menu"] = first_menu
        else:
            context["next_menu"] = False
        return context

    def get_queryset(self):
        return (
            super(Homepage, self)
                .get_queryset().current()
        )


class MenuDetail(DetailView):
    model = models.Menu


class ReservationDetail(UserPassesTestMixin, DetailView):
    model = models.Reservation

    def test_func(self):
        if self.request.user.is_staff:
            return True
        elif 'code' in self.kwargs:
            reservation = self.get_object()
            if reservation.code == self.kwargs['code']:
                return True
        else:
            reservation = self.get_object()
            if reservation.user == self.request.user:
                return True
        return False


class NewReservationCreate(CreateView):
    model = models.Reservation
    form_class = forms.ReservationForm

    def get_form(self):
        menu = get_object_or_404(models.Menu, pk=self.kwargs['pk'])
        if self.request.POST:
            return forms.ReservationForm(menu.free_seats, self.request.POST)
        else:
            return forms.ReservationForm(menu.free_seats)

    def form_valid(self, form):
        menu = get_object_or_404(models.Menu, pk=self.kwargs['pk'])
        form.instance.menu = menu
        form.instance.pax = int(form.instance.pax)
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user

        messages.add_message(
            self.request, messages.SUCCESS, _("The reservation has been successfully registered. You must confirm this reservation by clicking on the link in the message.")
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = get_object_or_404(models.Menu, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse("home")

