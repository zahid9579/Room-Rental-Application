from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, CancelAPIView, FilterAPIView, BookingAPIView, AllBookingAPIView, UserRegisterationView, UserLoginView, UserLogoutView, UserProfileView




urlpatterns = [
    path('rooms/', ListAPIView.as_view(), name='list_rooms'),
    path('rooms/create/', CreateAPIView.as_view(), name='create_room'),
    path('rooms/<int:id>/', RetrieveAPIView.as_view(), name='retrieve_room'),
    path('rooms/<int:id>/update/', UpdateAPIView.as_view(), name='update_room'),
    path('rooms/<int:id>/delete/', CancelAPIView.as_view(), name='delete_room'),
    path('search/', FilterAPIView.as_view(), name='Search_filter'),
    path('rooms/<int:id>/booking/', BookingAPIView.as_view(), name='booking'),
    path('allBookings/',AllBookingAPIView.as_view(), name="getAllBookings"),
    path('user_register/', UserRegisterationView.as_view(), name='register'),
    path('user_login/', UserLoginView.as_view(), name='register'),
    path('user_logout/', UserLogoutView.as_view(), name='logout'),
    path('user_profile/', UserProfileView.as_view(), name='profile'),
       
    
]

# Adding media URL configuration for serving uploaded files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
