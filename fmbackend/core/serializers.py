from rest_framework import serializers
from .models import User, FamilyGroup, UserGroup, Asset, Transaction, Document, Notification
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Both email and password are required.")
        
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'first_name', 'last_name', 'date_joined', 'profile_img']
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            role=validated_data['role'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            profile_img=validated_data.get('profile_img', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class FamilyGroupSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = FamilyGroup
        fields = ['id', 'name', 'admin', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserGroupSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = FamilyGroupSerializer(read_only=True)

    class Meta:
        model = UserGroup
        fields = ['user', 'group', 'permissions']
        read_only_fields = ['user', 'group']

    def validate_permissions(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Permissions must be a JSON object.")
        valid_keys = {'assets', 'transactions', 'documents'}
        for key in value:
            if key not in valid_keys:
                raise serializers.ValidationError(f"Invalid permission key: {key}")
            if value[key] not in ['read', 'write', 'none']:
                raise serializers.ValidationError(f"Invalid permission value for {key}: {value[key]}")
        return value

class AssetSerializer(serializers.ModelSerializer):
    group = FamilyGroupSerializer(read_only=True)

    class Meta:
        model = Asset
        fields = ['id', 'group', 'type', 'name', 'value', 'last_updated', 'api_source']
        read_only_fields = ['id', 'last_updated']

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Asset value cannot be negative.")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    group = FamilyGroupSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'asset', 'group', 'amount', 'category', 'description', 'date', 'is_unusual']
        read_only_fields = ['id']

    def validate_amount(self, value):
        if value is None:
            raise serializers.ValidationError("Amount is required.")
        return value

class DocumentSerializer(serializers.ModelSerializer):
    group = FamilyGroupSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'group', 'name', 'file', 'file_url', 'type', 'expiry_date', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size must not exceed 10MB.")
        return value

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'type', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value

class UserGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['permissions']

class DocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'type', 'expiry_date']

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']