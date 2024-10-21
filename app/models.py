from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CampaignGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    campaigns = models.ManyToManyField(Campaign, through='GroupCampaign')  # Many-to-many with GroupCampaign intermediary
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Group-level total budget

    def __str__(self):
        return self.name

class GroupCampaign(models.Model):
    group = models.ForeignKey(CampaignGroup, related_name='group_campaigns', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, related_name='campaign_groups', on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2)  # Budget for each campaign in the group

    class Meta:
        unique_together = ('group', 'campaign')  # Ensure each campaign is unique within a group

    def __str__(self):
        return f"{self.campaign.name} in {self.group.name} with budget {self.budget}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - {self.rating}/5"
