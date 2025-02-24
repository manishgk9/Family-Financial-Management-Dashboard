from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from decimal import Decimal
import pandas as pd  # Required for AI insights
from .models import User, FamilyGroup, UserGroup, Asset, Transaction, Document, Notification
from .serializers import (
    UserSerializer, FamilyGroupSerializer, UserGroupSerializer, AssetSerializer,
    TransactionSerializer, DocumentSerializer, NotificationSerializer,
    UserGroupUpdateSerializer, DocumentUpdateSerializer, NotificationUpdateSerializer, LoginSerializer
)

# Custom token generation function
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['role'] = user.role  # Add role to token payload
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Optional index view (remove if not needed)
def index(request):
    return Response({'message': 'This is the new page!'}, status=status.HTTP_200_OK)

# Refresh Token View
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

# Custom Permission for Group Access
class HasGroupPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.role == 'admin' or UserGroup.objects.filter(user=request.user).exists()

# Authentication Views
class LoginView(APIView):
    """Custom login endpoint using LoginSerializer."""
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Get authenticated user
            tokens = get_tokens_for_user(user)
            return Response({
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(APIView):
    """Register a new user (admin only)."""
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Management Views
class UserDetailView(APIView):
    """Get or update user details."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        if request.user.role != 'admin' and request.user != user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        if request.user.role != 'admin' and request.user != user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Family Group Views
class FamilyGroupListView(APIView):
    """List or create family groups."""
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        groups = FamilyGroup.objects.all()
        serializer = FamilyGroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FamilyGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User-Group Permissions Views
class UserGroupPermissionsView(APIView):
    """Update user permissions in a group."""
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def put(self, request, group_id):
        group = get_object_or_404(FamilyGroup, id=group_id)
        user_id = request.data.get('user_id')
        user_group = get_object_or_404(UserGroup, user_id=user_id, group=group)
        serializer = UserGroupUpdateSerializer(user_group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Asset Views
class AssetListView(APIView):
    """List or create assets."""
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_groups = UserGroup.objects.filter(user=request.user)
        assets = Asset.objects.filter(group__in=[ug.group for ug in user_groups])
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AssetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            group = UserGroup.objects.filter(user=request.user).first().group
            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetDetailView(APIView):
    """Get or update an asset."""
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        asset = get_object_or_404(Asset, id=id)
        if not self._has_permission(request.user, asset.group):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    def put(self, request, id):
        asset = get_object_or_404(Asset, id=id)
        if not self._has_permission(request.user, asset.group, 'write'):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = AssetSerializer(asset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _has_permission(self, user, group, permission='read'):
        user_group = UserGroup.objects.filter(user=user, group=group).first()
        if not user_group or user_group.permissions.get('assets', 'none') == 'none':
            return False
        return user.role == 'admin' or user_group.permissions.get('assets') in [permission, 'write']

# Dashboard View
class DashboardView(APIView):
    """Fetch aggregated data for the dashboard."""
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_groups = UserGroup.objects.filter(user=request.user)
        groups = [ug.group for ug in user_groups]
        
        assets = Asset.objects.filter(group__in=groups).aggregate(total_value=Sum('value'))
        transactions = Transaction.objects.filter(group__in=groups)
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        
        data = {
            'total_asset_value': assets['total_value'] or Decimal('0.00'),
            'recent_transactions': TransactionSerializer(transactions[:5], many=True).data,
            'notifications': NotificationSerializer(notifications, many=True).data
        }
        return Response(data)

# Transaction Views
class TransactionListView(APIView):
    """List or create transactions."""
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_groups = UserGroup.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(group__in=[ug.group for ug in user_groups])
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            group = UserGroup.objects.filter(user=request.user).first().group
            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Document Views
class DocumentListView(APIView):
    """List or upload documents."""
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_groups = UserGroup.objects.filter(user=request.user)
        documents = Document.objects.filter(group__in=[ug.group for ug in user_groups])
        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            group = UserGroup.objects.filter(user=request.user).first().group
            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentDetailView(APIView):
    """Get or update a document."""
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        document = get_object_or_404(Document, id=id)
        if not self._has_permission(request.user, document.group):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = DocumentSerializer(document, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id):
        document = get_object_or_404(Document, id=id)
        if not self._has_permission(request.user, document.group, 'write'):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = DocumentUpdateSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _has_permission(self, user, group, permission='read'):
        user_group = UserGroup.objects.filter(user=user, group=group).first()
        if not user_group or user_group.permissions.get('documents', 'none') == 'none':
            return False
        return user.role == 'admin' or user_group.permissions.get('documents') in [permission, 'write']

# Notification Views
class NotificationListView(APIView):
    """List notifications for the user."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class NotificationUpdateView(APIView):
    """Mark a notification as read."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, id):
        notification = get_object_or_404(Notification, id=id, user=request.user)
        serializer = NotificationUpdateSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# AI-Driven Insights Views
class BudgetInsightView(APIView):
    """Get budget recommendations."""
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_groups = UserGroup.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(group__in=[ug.group for ug in user_groups])
        
        total_income = transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0
        budget_recommendation = total_income * Decimal('0.8')
        
        return Response({
            'total_income': str(total_income),
            'total_expense': str(total_expense),
            'recommended_budget': str(budget_recommendation)
        })

class TrendInsightView(APIView):
    """Get expense trends."""
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_groups = UserGroup.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(group__in=[ug.group for ug in user_groups])
        
        df = pd.DataFrame(list(transactions.values('date', 'amount', 'category')))
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            monthly_trends = df.groupby([df['date'].dt.to_period('M'), 'category'])['amount'].sum().unstack().fillna(0)
            return Response(monthly_trends.to_dict())
        return Response({"message": "No transactions available"})