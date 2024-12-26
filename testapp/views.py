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