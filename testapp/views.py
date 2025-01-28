from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Booking
from .serializers.room_serializers import RoomSerializer, BookingSerializer
from .serializers.user_serializers import UserRegisterationSerializer, UserLoginSerializer, LogoutSerializer, UserProfileSerializer                                                      

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import  IsAuthenticated, AllowAny  
from django.contrib.auth import authenticate 
from django.shortcuts import render, get_object_or_404    
# To Book a room
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
                        

#******** Room CRUD operation STARTS here ********************
                                                                                                                                                                                                                                                                                                                         
# For listing all the rooms
class ListAPIView(APIView):
    def get(self, request):
        queryset = Room.objects.all()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# To create a new Room
class CreateAPIView(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# To retrieve a single Room by ID
class RetrieveAPIView(APIView):                 
    def get(self, request, id):
        try:
            room = Room.objects.get(pk=id)
            serializer = RoomSerializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


# To update an existing Room
class UpdateAPIView(APIView):
    def put(self, request, id):
        try:
            room = Room.objects.get(pk=id)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


class CancelAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            booking = Booking.objects.get(pk=id, user=request.user)  # Ensure the booking belongs to the user
            booking.delete()
            return Response({"message": "Booking canceled successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

#******** Room CRUD operation ENDS here ********************


#******** Room Search and Filter Functionality STARTS here **********

class FilterAPIView(APIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        qs = Room.objects.all()

        # Fetch query parameters from the request
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        location = self.request.GET.get('location')

        # Filter by price_min (if provided) - Ensure price is converted to float
        if price_min:
            try:
                price_min = float(price_min)
                qs = qs.filter(price__gte=price_min)
            except ValueError:
                return Response({"error": "Invalid price format for 'price_min'"}, status=400)

        # Filter by price_max (if provided) - Ensure price is converted to float
        if price_max:
            try:
                price_max = float(price_max)
                qs = qs.filter(price__lte=price_max)
            except ValueError:
                return Response({"error": "Invalid price format for 'price_max'"}, status=400)

        # Filter by location (if provided) using 'icontains' for case-insensitive matching
        if location:
            qs = qs.filter(location__icontains=location)

        return qs

    def get(self, request, *args, **kwargs):
        # Get filtered rooms based on query parameters
        rooms = self.get_queryset()

        # Serialize the filtered queryset
        serializer = self.serializer_class(rooms, many=True)
        return Response(serializer.data)

#******** Room Search and Filter Functionality ENDS here **********



#****************************
# Room Booking STARTS here 
# ***************************
class BookingAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            room = Room.objects.get(pk=id)
            data = {
                "user": request.user.id,  # Get the logged-in user's ID
                "room": room.id,
            }

            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


    
# To get all the booked rooms
# class AllBookingAPIView(APIView):
#     def get(self, request):
#         bookings = Booking.objects.filter(user=request.user)  # Filter bookings by the logged-in user
#         serializer = BookingSerializer(bookings, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)



# ******************************
# USER Authentication Starts here
# *******************************

from rest_framework_simplejwt.tokens import RefreshToken
# To generate token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
# User Registeration view
class UserRegisterationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Serialize and validate user registration data
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user and generate tokens
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': "Registration successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
# User Login view 
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Serialize the login data
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({
                    'token': token,
                    'msg': "Login Successfully",
                    'is_admin': user.is_superuser
                }, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {'non_field_errors': ['Email or password is not valid']}}, status=status.HTTP_401_UNAUTHORIZED)
        
        
# User Logout view
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract the refresh token from the request data
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Blacklist the refresh token (you can use `RefreshToken` to revoke it)
            token = RefreshToken(refresh_token)
            token.blacklist()  # This requires the `blacklist` feature to be enabled in `rest_framework_simplejwt`
            
            return Response({"msg": "Logout Successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
# User Profile View
class UserProfileView(APIView):
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        
          
        
#08254f color description : Very dark blue. FRONT END BACKGRound Color


# Django templates displaying starts form here
def homepage(request):
    return render(request, 'testapp/homepage.html')


# Views to Fetch the data
def room_listing(request):
    # Fetch all rooms from the database
    rooms = Room.objects.all()
    return render(request, 'testapp/room_listing.html', {'rooms': rooms})



def room_details(request, id):
    room = get_object_or_404(Room, pk=id)
    user_booking = None
    if request.user.is_authenticated:
        user_booking = Booking.objects.filter(user=request.user, room=room).first()
    return render(request, "testapp/room_details.html", {"room": room, "user_booking": user_booking})


# View to cancel the booked room
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def room_booking(request, id):
    room = get_object_or_404(Room, pk=id)
    
    # Restrict superusers from booking rooms
    if request.user.is_superuser:
        messages.error(request, "Superusers cannot book rooms.")
        return redirect("room_listing")

    if request.method == "POST":
        # Check if the user has already booked the room
        if Booking.objects.filter(user=request.user, room=room).exists():
            messages.error(request, "You have already booked this room.")
        else:
            Booking.objects.create(user=request.user, room=room)
            messages.success(request, "Room booked successfully!")
        return redirect("room_details", id=id)  # Redirect to room details page
    return redirect("room_listing")  # Redirect to room listing if accessed incorrectly



# @login_required
def cancel_booking(request, id):
    booking = get_object_or_404(Booking, pk=id, user=request.user)
    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking canceled successfully!")
        return redirect("room_details", id=booking.room.id)  # Redirect to room details
    return redirect("room_listing")  # Redirect to room listing if accessed incorrectly


#*********************************
# Integration for BACKEND to FRONTEND
# ************************************
import json
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm

# Registration function
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = {
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "password": form.cleaned_data['password'],
                "password2": form.cleaned_data['confirm_password'],
                "tc": form.cleaned_data['tc']
            }

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/user_register/api/",
                    data=json.dumps(data),
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 201:
                    messages.success(request, "Registration successful! Please log in.")
                    return redirect('login user')
                else:
                    error_message = response.json().get('msg', 'Something went wrong.')
                    messages.error(request, error_message)

            except requests.exceptions.RequestException as e:
                messages.error(request, f"Error communicating with the server: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = RegisterForm()

    return render(request, 'testapp/register_form.html', {'form': form})


import json
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm

# Login function
# In your login view
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                "email": form.cleaned_data['email'],
                "password": form.cleaned_data['password']
            }

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/user_login/api/",
                    data=json.dumps(data),
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 200:
                    user_data = response.json()
                    request.session['access_token'] = user_data.get('token').get('access')
                    request.session['refresh_token'] = user_data.get('token').get('refresh')
                    request.session['is_admin'] = user_data.get('is_admin', False)  # Store admin role in session
                    messages.success(request, "Login successful!")

                    # Pass the session status to the template
                    return redirect('homepage')  # Replace with user homepage route
                else:
                    error_message = response.json().get('errors', 'Invalid email or password.')
                    messages.error(request, error_message)

            except requests.exceptions.RequestException as e:
                messages.error(request, f"Error communicating with the server: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = LoginForm()

    return render(request, 'testapp/login.html', {'form': form})



# Logout function
def logout(request):
    if request.method == "POST":
        # Retrieve the access and refresh tokens from the session
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')

        if not access_token or not refresh_token:
            messages.error(request, "No valid tokens found. Please log in again.")
            return redirect('login user')

        try:
            # Prepare the headers for the logout request
            headers = {
                'Authorization': f"Bearer {access_token}",  # Include access token in the header
                'Content-Type': 'application/json'  # Ensure the correct header for JSON data
            }

            # Send logout request to the API
            response = requests.post(
                "http://127.0.0.1:8000/user_logout/api/",
                headers=headers,  # Send the headers here
                data=json.dumps({'refresh': refresh_token})  # Include the refresh token in the body
            )

            if response.status_code == 200:
                # Logout successful
                request.session.flush()  # Clear session
                messages.success(request, "Logout successful!")
                return redirect('login user')
            else:
                messages.error(request, response.json().get('detail', 'Logout failed.'))

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Server communication error: {e}")

    return render(request, 'testapp/homepage.html')



