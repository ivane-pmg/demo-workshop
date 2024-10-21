from django.contrib import admin
from .models import CampaignGroup, Campaign, GroupCampaign, Feedback

# Registering the CampaignGroup model with custom admin display
@admin.register(CampaignGroup)
class CampaignGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by']  # Customize fields displayed in the admin list
    search_fields = ['name']  # Allow searching by name
    list_filter = ['created_by']  # Add filters for created_by and created_at

# Registering the Campaign model
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# Registering the GroupCampaign model
@admin.register(GroupCampaign)
class GroupCampaignAdmin(admin.ModelAdmin):
    list_display = ['group', 'campaign', 'budget']  # Customize fields displayed
    search_fields = ['group__name', 'campaign__name']  # Allow searching by group name or campaign name
    list_filter = ['group', 'campaign']  # Filter by group and campaign

# Registering the Feedback model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating']  # Ensure created_at exists in the model
    search_fields = ['user__username']  # Allow searching by username
    list_filter = ['rating']  # Add filters for rating and creation date
