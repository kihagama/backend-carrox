# urls.py
from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path("home/", views.home, name="home"),
    path("teams/", views.team, name="Team"),
    path("cars/", views.cars, name="Cars"),
    path("hire/", views.hire_car, name="HireCar"),
    path("wash/", views.book_car_wash, name="BookCarWash"),
    path("register/", views.register, name="Register"),
    path("my-bookings/", views.user_bookings, name="UserBookings"),
    path("delete-booking/<str:booking_type>/<int:pk>/", views.delete_booking, name="DeleteBooking"),
    path("sendmails/", views.sendemails, name="Mails"),
    path("pay/", views.simulate_payment, name="SimulatePayment"),
    path("profile/", views.get_profile, name="GetProfile"),
    path("profile/update/", views.update_profile, name="UpdateProfile"),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
