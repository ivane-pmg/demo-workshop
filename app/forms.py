from django import forms
from .models import CampaignGroup, GroupCampaign, Feedback, Campaign
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# User Signup Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CampaignGroupForm(forms.ModelForm):
    campaign = forms.ModelChoiceField(
        queryset=Campaign.objects.all(),  # Allow selection of only one campaign
        widget=forms.Select,
        required=True,
        help_text="Select a campaign."
    )
    
    class Meta:
        model = CampaignGroup
        fields = ['name', 'description', 'total_budget', 'campaign']  # Include the fields
        widgets = {
            'total_budget': forms.NumberInput(attrs={'placeholder': 'Enter the total budget'}),
        }

# GroupCampaign Form (assigning campaign and setting its budget)
class GroupCampaignForm(forms.ModelForm):
    class Meta:
        model = GroupCampaign
        fields = ['campaign', 'budget']  # Campaign and budget fields
        widgets = {
            'budget': forms.NumberInput(attrs={'placeholder': 'Enter budget for this campaign'}),
        }

# Feedback Form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
