from .models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email","username", "password","auth_type"]
        extra_kwargs = {
                'password': {'write_only':True}
        }

    def save(self):
      print(self.validated_data)
      user = User(
          email = self.validated_data['email'],
          username = self.validated_data['username'],
          auth_type = self.validated_data['auth_type'],
      )
      password = self.validated_data['password']
      user.set_password(password)
      user.save()
      return user




