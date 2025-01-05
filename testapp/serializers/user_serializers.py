from rest_framework import serializers
from ..models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


# Registeration Seralizers
class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_Kwargs = {
            'password': {'write_only': True}
        }
        
    # Validating password and confirm password while registeration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Both password are not same , password must be same")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
# Login Serializer
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta: 
        model = User
        fields = ['email', 'password']
        
       
# Logout Serializer 
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': 'Token expired or invalid',
    }
        
    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs
    
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            self.fail('bad_token')
        
        
 # User Profile Serialzer       
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']