from rest_framework import serializers
from .models import Team, Car, CarHiring, CarWashBooking, Payment, UserProfile

class TeamSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class CarSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class CarHiringSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    car_details = CarSerializer(source='car', read_only=True, context={})

    class Meta:
        model = CarHiring
        fields = '__all__'

    def to_representation(self, instance):
        # Pass request context down to nested serializer
        rep = super().to_representation(instance)
        car_serializer = CarSerializer(instance.car, context=self.context)
        rep['car_details'] = car_serializer.data
        return rep

class CarWashBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashBooking
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user', 'image']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
