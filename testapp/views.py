from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Booking
from .serializers.room_serializers import RoomSerializer, BookingSerializer
from .serializers.user_serializers import UserRegisterationSerializer, UserLoginSerializer, LogoutSerializer, UserProfileSerializer                                                      

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny   
from django.contrib.auth import authenticate 
from django.shortcuts import render                              

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


# To delete a Room
class CancelAPIView(APIView):
    def delete(self, request, id):
        try:
            room = Room.objects.get(pk=id)
            room.delete()
            return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

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

# To Book a room
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
class AllBookingAPIView(APIView):
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)  # Filter bookings by the logged-in user
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# ******************************
# USER Authentication Starts here
# *******************************

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
        serializer = UserRegisterationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': "Registeration successfully"}, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
# User Login view 
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, "msg": "Login Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {'non_field_errors': ['Email or passowrd is not valid']}}, status=status.HTTP_401_UNAUTHORIZED)
            
        
        
# User Logout view
class UserLogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Logout Successfully"}, status=status.HTTP_200_OK)
    

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