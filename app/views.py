from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import models 
from django.forms import modelformset_factory
from .models import CampaignGroup, Campaign, GroupCampaign, Feedback
from .forms import CampaignGroupForm, GroupCampaignForm, FeedbackForm, SignUpForm
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after signup
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'There was an error with your signup. Please try again.')
    else:
        form = SignUpForm()
    
    return render(request, 'app/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check if the username exists in the database
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "The username does not exist.")
                return render(request, 'app/login.html', {'form': form})

            # Proceed with authentication if username exists
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, "Invalid password.")
        else:
            messages.error(request, "Invalid username or password.")
    
    form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})


# Custom logout view
def custom_logout(request):
    logout(request)
    return redirect('login')


# Home view (Optional)
@login_required
def home(request):
    return render(request, 'app/home.html')


@login_required
def create_group(request):
    if request.method == 'POST':
        form = CampaignGroupForm(request.POST)
        if form.is_valid():
            # Save the group
            campaign_group = form.save(commit=False)
            campaign_group.created_by = request.user  # Assign the current user as the creator
            campaign_group.save()

            if campaign_group.total_budget > 200:
                messages.error(request, 'Budget has to be less than 200.')
                return redirect('create_group')

            # Save the selected campaign in the intermediary model
            GroupCampaign.objects.create(
                group=campaign_group,
                campaign=form.cleaned_data['campaign'],
                budget=campaign_group.total_budget  # Assume group budget is applied to the campaign
            )

            messages.success(request, 'Campaign group created successfully.')
            return redirect('manage_groups')
        else:
            messages.error(request, 'There was an error creating the campaign group. Please check the form.')
    else:
        form = CampaignGroupForm()

    return render(request, 'app/create_group.html', {'form': form})


@login_required
def manage_groups(request):
    groups = CampaignGroup.objects.filter(created_by=request.user)  # Only show user's own groups
    total_budget = groups.aggregate(total=models.Sum('total_budget'))['total'] or 0  # Calculate total budget

    return render(request, 'app/manage_groups.html', {
        'groups': groups,
        'total_budget': total_budget
    })



# View to assign campaigns to a group
@login_required
def assign_campaign(request, group_id):
    group = get_object_or_404(CampaignGroup, id=group_id, created_by=request.user)
    
    if request.method == 'POST':
        form = GroupCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.cleaned_data['campaign']
            budget = form.cleaned_data['budget']
            GroupCampaign.objects.create(group=group, campaign=campaign, budget=budget)
            messages.success(request, f'Campaign "{campaign.name}" assigned successfully.')
            return redirect('manage_groups')
    else:
        form = GroupCampaignForm()

    # Fetch campaigns that haven't been assigned to the group
    campaigns = Campaign.objects.exclude(groupcampaign__group=group)
    return render(request, 'app/assign_campaign.html', {'form': form, 'group': group, 'campaigns': campaigns})


# View to delete a campaign group
@login_required
def delete_group(request, group_id):
    group = get_object_or_404(CampaignGroup, id=group_id, created_by=request.user)
    
    if request.method == 'POST':
        group.delete()
        messages.success(request, f'Group "{group.name}" deleted successfully.')
        return redirect('manage_groups')

    return render(request, 'app/delete_group.html', {'group': group})


# Feedback view
@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Attach the feedback to the current user
            feedback.save()
            messages.success(request, 'Thank you for your feedback.')
            return redirect('home')
    else:
        form = FeedbackForm()

    return render(request, 'app/feedback.html', {'form': form})

@login_required
def edit_group(request, group_id):
    campaign_group = get_object_or_404(CampaignGroup, id=group_id, created_by=request.user)

    # Get the related GroupCampaign (assuming one campaign per group)
    group_campaign = GroupCampaign.objects.filter(group=campaign_group).first()

    if request.method == 'POST':
        form = CampaignGroupForm(request.POST, instance=campaign_group)

        if form.is_valid():
            # Update the group details
            campaign_group = form.save()

            # Update the selected campaign and budget
            if group_campaign:
                group_campaign.campaign = form.cleaned_data['campaign']
                group_campaign.budget = campaign_group.total_budget  # Assume group budget is applied to campaign
                group_campaign.save()
            else:
                # Create a new GroupCampaign entry if none exists
                GroupCampaign.objects.create(
                    group=campaign_group,
                    campaign=form.cleaned_data['campaign'],
                    budget=campaign_group.total_budget
                )

            messages.success(request, 'Campaign group updated successfully.')
            return redirect('manage_groups')
    else:
        # Prepopulate the form with the group details
        form = CampaignGroupForm(instance=campaign_group)
        if group_campaign:
            form.initial['campaign'] = group_campaign.campaign  # Prepopulate campaign

    return render(request, 'app/edit_group.html', {'form': form, 'group': campaign_group})

