from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, CancelAPIView, FilterAPIView, BookingAPIView, AllBookingAPIView, UserRegisterationView, UserLoginView, UserLogoutView, UserProfileView
from . import views
from testapp.views import room_listing



urlpatterns = [
    path('rooms/api/', ListAPIView.as_view(), name='list_rooms'),
    path('rooms/api/create/', CreateAPIView.as_view(), name='create_room'),
    path('rooms/api/<int:id>/', RetrieveAPIView.as_view(), name='retrieve_room'),
    path('rooms/api/<int:id>/update/', UpdateAPIView.as_view(), name='update_room'),
    path('rooms/api/<int:id>/delete/', CancelAPIView.as_view(), name='delete_room'),
    path('search/', FilterAPIView.as_view(), name='Search_filter'),
    path('rooms/api/<int:id>/booking/', BookingAPIView.as_view(), name='booking'),
    path('allBookings/api/',AllBookingAPIView.as_view(), name="getAllBookings"),
    path('user_register/api/', UserRegisterationView.as_view(), name='register'),
    path('user_login/api/', UserLoginView.as_view(), name='register'),
    path('user_logout/api/', UserLogoutView.as_view(), name='logout'),
    path('user_profile/api', UserProfileView.as_view(), name='profile'),
    
    
    
    # URLs for TEMPLATES
    path('', views.homepage, name='homepage'),
    
    # Urls for fectching the data
    path('rooms/', room_listing, name='room_listing'),  # Room listing URL
    
       
    
]

# Adding media URL configuration for serving uploaded files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
