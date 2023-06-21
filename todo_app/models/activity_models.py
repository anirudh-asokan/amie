from django.db import models
from .user_models import User
from .integration_models import ThirdPartyAppIntegration

class ActivityHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    app_integration = models.ForeignKey(ThirdPartyAppIntegration, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)