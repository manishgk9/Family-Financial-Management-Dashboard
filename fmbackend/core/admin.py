from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FamilyGroup, UserGroup, Asset, Transaction, Document, Notification

# Custom User Admin
class UserAdmin(BaseUserAdmin):
    """Admin interface for the custom User model."""
    model = User
    list_display = ('email', 'role', 'first_name', 'last_name', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_img')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'first_name', 'last_name', 'profile_img', 'is_active', 'is_staff'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')

# Inline for UserGroup to show in FamilyGroup admin
class UserGroupInline(admin.TabularInline):
    """Inline display of UserGroup within FamilyGroup."""
    model = UserGroup
    extra = 1  # Number of empty rows to display
    fields = ('user', 'permissions')
    autocomplete_fields = ('user',)

# Family Group Admin
@admin.register(FamilyGroup)
class FamilyGroupAdmin(admin.ModelAdmin):
    """Admin interface for FamilyGroup."""
    list_display = ('name', 'admin_email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'admin__email')
    inlines = [UserGroupInline]
    fieldsets = (
        (None, {'fields': ('name', 'admin')}),
        ('Metadata', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
    
    def admin_email(self, obj):
        return obj.admin.email
    admin_email.short_description = 'Admin Email'

# UserGroup Admin
@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    """Admin interface for UserGroup."""
    list_display = ('user_email', 'group_name', 'permissions_display')
    list_filter = ('group__name',)
    search_fields = ('user__email', 'group__name')
    fieldsets = (
        (None, {'fields': ('user', 'group', 'permissions')}),
    )
    autocomplete_fields = ('user', 'group')
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def group_name(self, obj):
        return obj.group.name
    group_name.short_description = 'Group Name'
    
    def permissions_display(self, obj):
        return str(obj.permissions)
    permissions_display.short_description = 'Permissions'

# Asset Admin
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """Admin interface for Asset."""
    list_display = ('name', 'type', 'group_name', 'value', 'last_updated', 'api_source')
    list_filter = ('type', 'group__name', 'last_updated')
    search_fields = ('name', 'group__name', 'api_source')
    fieldsets = (
        (None, {'fields': ('group', 'type', 'name', 'value', 'api_source')}),
        ('Metadata', {'fields': ('last_updated',)}),
    )
    readonly_fields = ('last_updated',)
    autocomplete_fields = ('group',)
    
    def group_name(self, obj):
        return obj.group.name
    group_name.short_description = 'Group Name'

# Inline for Transaction to show in Asset admin
class TransactionInline(admin.TabularInline):
    """Inline display of Transaction within Asset."""
    model = Transaction
    extra = 1
    fields = ('amount', 'category', 'description', 'date', 'is_unusual')
    readonly_fields = ('date',)

# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction."""
    list_display = ('description', 'group_name', 'asset_name', 'amount', 'category', 'date', 'is_unusual')
    list_filter = ('category', 'is_unusual', 'date', 'group__name')
    search_fields = ('description', 'group__name', 'asset__name')
    fieldsets = (
        (None, {'fields': ('asset', 'group', 'amount', 'category', 'description', 'is_unusual')}),
        ('Metadata', {'fields': ('date',)}),
    )
    readonly_fields = ('date',)
    autocomplete_fields = ('asset', 'group')
    
    def group_name(self, obj):
        return obj.group.name
    group_name.short_description = 'Group Name'
    
    def asset_name(self, obj):
        return obj.asset.name
    asset_name.short_description = 'Asset Name'

# Document Admin
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin interface for Document."""
    list_display = ('name', 'group_name', 'type', 'file_url', 'expiry_date', 'uploaded_at')
    list_filter = ('type', 'expiry_date', 'uploaded_at', 'group__name')
    search_fields = ('name', 'group__name')
    fieldsets = (
        (None, {'fields': ('group', 'name', 'file', 'type', 'expiry_date')}),
        ('Metadata', {'fields': ('uploaded_at',)}),
    )
    readonly_fields = ('uploaded_at',)
    autocomplete_fields = ('group',)
    
    def group_name(self, obj):
        return obj.group.name
    group_name.short_description = 'Group Name'
    
    def file_url(self, obj):
        return obj.file.url if obj.file else 'No file'
    file_url.short_description = 'File URL'

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification."""
    list_display = ('message_preview', 'user_email', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at', 'user__role')
    search_fields = ('message', 'user__email')
    fieldsets = (
        (None, {'fields': ('user', 'message', 'type', 'is_read')}),
        ('Metadata', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
    autocomplete_fields = ('user',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def message_preview(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    message_preview.short_description = 'Message'

# Register custom User model with UserAdmin
admin.site.register(User, UserAdmin)