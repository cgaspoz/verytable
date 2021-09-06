from django.urls import path

from .views import (
    MenuDetail, ReservationDetail, NewReservationCreate
)

app_name = "menus"

urlpatterns = [
    path("<int:pk>", MenuDetail.as_view(), name="menus"),
    path("<int:pk>/reserve", NewReservationCreate.as_view(), name="new-reservation"),
    path("reservation/<int:pk>/<uuid:code>", ReservationDetail.as_view(), name="reservation-uuid"),
    path("reservation/<int:pk>", ReservationDetail.as_view(), name="reservation"),
]
