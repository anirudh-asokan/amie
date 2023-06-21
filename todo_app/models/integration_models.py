import logging
from django.db import models
from .user_models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)


class ThirdPartyApp(models.Model):
    name = models.CharField(max_length=100)
    service_key = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ThirdPartyAppIntegration(models.Model):
    """
    Represents the integration of a third-party app with a user's account.

    Note:
        Technically, it is possible for a single user to have multiple integrations
        with the same third-party app (e.g., multiple accounts or profiles).
        However, for the purpose of this demo, it is assumed that a user will have
        only one integration with each third-party app.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='app_integrations')
    third_party_app = models.ForeignKey(
        ThirdPartyApp, on_delete=models.CASCADE)
    auth_token = models.ForeignKey(AuthToken, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class ThirdPartyEntityMapping(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    trackable_entity = GenericForeignKey('content_type', 'object_id')

    third_party_id = models.CharField(max_length=255)
    integration = models.ForeignKey(
        ThirdPartyAppIntegration, on_delete=models.CASCADE)
    last_synced_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_mapping(trackable_entity, third_party_id, integration):
        if not trackable_entity:
            return
        if ThirdPartyEntityMapping.get_trackable_entity(third_party_id, integration):
            return
        content_type = ContentType.objects.get_for_model(
            type(trackable_entity))
        mapping = ThirdPartyEntityMapping.objects.create(
            content_type=content_type,
            object_id=trackable_entity.pk,
            third_party_id=third_party_id,
            integration=integration
        )
        return mapping

    @staticmethod
    def get_third_party_id(trackable_entity, integration):
        try:
            content_type = ContentType.objects.get_for_model(
                type(trackable_entity))
            mapping = ThirdPartyEntityMapping.objects.get(
                content_type=content_type,
                object_id=trackable_entity.pk,
                integration=integration
            )
            return mapping.third_party_id
        except ThirdPartyEntityMapping.DoesNotExist:
            # If no mapping found, return None
            return None

    @staticmethod
    def get_trackable_entity(third_party_id, integration):
        try:
            # Try to get the mapping object from the database
            mapping = ThirdPartyEntityMapping.objects.get(
                third_party_id=third_party_id,
                integration=integration
            )
            return mapping.trackable_entity
        except ThirdPartyEntityMapping.DoesNotExist:
            # If no mapping found, return None
            return None
