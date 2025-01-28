from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, CancelAPIView, FilterAPIView, UserRegisterationView, UserLoginView, UserLogoutView, UserProfileView, BookingAPIView
# from . import views
from testapp.views import homepage, room_listing, room_details, room_booking, cancel_booking
from .views import register, login, logout



urlpatterns = [
    
    # URLs for APIs
    path('rooms/api/', ListAPIView.as_view(), name='list_rooms'),
    path('rooms/api/create/', CreateAPIView.as_view(), name='create_room'),
    path('rooms/api/<int:id>/', RetrieveAPIView.as_view(), name='retrieve_room'),
    path('rooms/api/<int:id>/update/', UpdateAPIView.as_view(), name='update_room'),
    path('rooms/api/<int:id>/delete/', CancelAPIView.as_view(), name='delete_room'),
    path('rooms/api/<int:id>/delete/', BookingAPIView.as_view(), name='booking_room'),
    path('search/', FilterAPIView.as_view(), name='Search_filter'),
    path('user_register/api/', UserRegisterationView.as_view(), name='register'),
    path('user_login/api/', UserLoginView.as_view(), name='login'),
    path('user_logout/api/', UserLogoutView.as_view(), name='logout'),
    path('user_profile/api', UserProfileView.as_view(), name='profile'),
    
    
    
    # URLs for TEMPLATES
    path('', homepage, name='homepage'),
    
    # Urls for fectching the data
    path('rooms/', room_listing, name='room_listing'),  # Room listing URL
    path('room_details/<int:id>/', room_details, name='room_details'), # Room Details URL
    path('room_booking/<int:id>/', room_booking, name='room_booking'),
    path('cancel_booking/<int:id>/', cancel_booking, name='cancel_booking'),
    
    
    
    # URLs for Authentication Register Login, Logut
    path('register/', register, name='register user'),
    path('login/', login, name='login user'),
    path('logout/', logout, name='logout user'),  # For web-based logout
  
       
    
]

# Adding media URL configuration for serving uploaded files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
