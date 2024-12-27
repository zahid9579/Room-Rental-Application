from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers.room_serializers import RoomSerializer


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



#********** Room Booking STARTS here *****************
# class BookingAPIView(APIView):
#     def post(self, request, id):
        