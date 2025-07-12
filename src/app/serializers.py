from rest_framework import serializers
from .models import Team, Car, CarHiring, CarWashBooking, Payment, UserProfile

class TeamSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)  # Ensure URL is sent

    class Meta:
        model = Team
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Car
        fields = '__all__'


class CarHiringSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    car_details = CarSerializer(source='car', read_only=True)

    class Meta:
        model = CarHiring
        fields = '__all__'


class CarWashBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashBooking
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'image']
