from django.contrib import admin
from .models import Team, Car, CarHiring, CarWashBooking, Payment, UserProfile
#my models
admin.site.register(Team)
admin.site.register(Car)
admin.site.register(CarHiring)
admin.site.register(CarWashBooking)
admin.site.register(Payment)
admin.site.register(UserProfile)