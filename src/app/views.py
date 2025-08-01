from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Team, Car, CarHiring, CarWashBooking, Payment, UserProfile
from .serializers import (
    TeamSerializer,
    CarSerializer,
    CarHiringSerializer,
    CarWashBookingSerializer,
    PaymentSerializer,
    UserProfileSerializer
)

@api_view(["GET"])
def home(request):
    return Response("Welcome to Car Booking API!", status=status.HTTP_200_OK)

@api_view(["GET"])
def team(request):
    query = request.GET.get("name")
    if query:
        teams = Team.objects.filter(name__icontains=query)
    else:
        teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def cars(request):
    query = request.GET.get("title")
    if query:
        cars = Car.objects.filter(title__icontains=query)
    else:
        cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def hire_car(request):
    if request.method == "POST":
        serializer = CarHiringSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(status="pending")  # Use lowercase 'pending'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    status_filter = request.GET.get("status")
    if status_filter:
        bookings = CarHiring.objects.filter(status=status_filter)
    else:
        bookings = CarHiring.objects.all()

    serializer = CarHiringSerializer(bookings, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def book_car_wash(request):
    if request.method == "POST":
        serializer = CarWashBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status="pending")  # Use lowercase 'pending'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    status_filter = request.GET.get("status")
    if status_filter:
        bookings = CarWashBooking.objects.filter(status=status_filter)
    else:
        bookings = CarWashBooking.objects.all()

    serializer = CarWashBookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    if User.objects.filter(username=username).exists():
        raise ValidationError({"message": "User already exists"})

    User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    return Response({"message": "User registered successfully!"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_bookings(request):
    username = request.user.username

    carhires = CarHiring.objects.filter(customer_name=username)
    carhires_serializer = CarHiringSerializer(carhires, many=True, context={'request': request})

    carwashes = CarWashBooking.objects.filter(customer_name=username)
    carwashes_serializer = CarWashBookingSerializer(carwashes, many=True)

    return Response({
        "car_hires": carhires_serializer.data,
        "car_washes": carwashes_serializer.data
    }, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_booking(request, booking_type, pk):
    username = request.user.username

    if booking_type == "carhire":
        booking = CarHiring.objects.filter(pk=pk, customer_name=username).first()
    elif booking_type == "carwash":
        booking = CarWashBooking.objects.filter(pk=pk, customer_name=username).first()
    else:
        return Response({"error": "Invalid booking type"}, status=status.HTTP_400_BAD_REQUEST)

    if not booking:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    booking.delete()
    return Response({"message": "Booking deleted successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def sendemails(request):
    subject = request.data.get("usersname")
    message = request.data.get("message")
    email = request.data.get("email")
    full_message = f"Send Email: {email}\n\nMessage: {message}"
    send_mail(
        subject, full_message, settings.EMAIL_HOST_USER, ["ismaelkihagama@gmail.com"],
        fail_silently=False
    )
    return Response({"message": "Email submitted successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def simulate_payment(request):
    booking_type = request.data.get("booking_type")  # 'carhire' or 'carwash'
    booking_id = request.data.get("booking_id")
    amount = request.data.get("amount")
    user = request.user
    if not booking_type or not booking_id or not amount:
        return Response({"error": "booking_type, booking_id, and amount are required"}, status=400)

    if booking_type == "carhire":
        booking = get_object_or_404(CarHiring, pk=booking_id)
        booking.status = "confirmed"
        booking.save()
        content_type = ContentType.objects.get_for_model(CarHiring)
        serializer = CarHiringSerializer(booking, context={'request': request})
    elif booking_type == "carwash":
        booking = get_object_or_404(CarWashBooking, pk=booking_id)
        booking.status = "confirmed"
        booking.save()
        content_type = ContentType.objects.get_for_model(CarWashBooking)
        serializer = CarWashBookingSerializer(booking)
    else:
        return Response({"error": "Invalid booking_type"}, status=400)

    Payment.objects.create(
        user=user,
        amount=amount,
        content_type=content_type,
        object_id=booking_id
    )

    return Response(serializer.data, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile, context={'request': request})
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
