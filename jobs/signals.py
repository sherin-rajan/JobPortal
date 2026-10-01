from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Jobs, Notification


@receiver(post_save, sender=Jobs)
def job_created_notification(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        users = User.objects.filter(
            is_active=True,
            is_superuser=False
        )

        notifications = []

        for user in users:

            notifications.append(
                Notification(
                    user=user,
                    message=(
                        f"New job posted: {instance.title}"
                
                    )
                )
            )

        Notification.objects.bulk_create(
            notifications
        )