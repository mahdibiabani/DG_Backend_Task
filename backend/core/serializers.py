from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

# Custom serializer for user creation, extending Djoser's base user creation serializer
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']
        ref_name = 'DjoserUserCreateSerializer'

# Custom serializer for user representation, extending Djoser's base user serializer
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        ref_name = 'DjoserUserSerializer'