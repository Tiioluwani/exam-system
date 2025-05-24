from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from asgiref.sync import async_to_sync
from .models import User
from permit import Permit

permit = Permit(
    pdp=settings.PERMIT_PDP_URL,
    token=settings.PERMIT_API_KEY
)

@receiver(post_save, sender=User)
def sync_user_to_permit(sender, instance, created, **kwargs):
    if created:
        print(f"[Permit Sync] Syncing user {instance.email}")
        
        # Sync the user with Permit
        try:
            async_to_sync(permit.api.users.sync)({
                "key": str(instance.id),
                "email": instance.email,
                "first_name": instance.first_name,
                "last_name": instance.last_name
            })
        except Exception as e:
            print(f"[Permit Sync] Error syncing user: {e}")
        
        # Check if the user is a superuser and assign the correct role
        role = "admin" if instance.is_superuser else instance.role  # Set 'admin' role for superuser
        
        # Log the role before assigning
        print(f"[Permit Sync] Assigning role: {role} to user {instance.email}")
        
        # Assign the role to the user in Permit
        try:
            async_to_sync(permit.api.users.assign_role)({
                "user": str(instance.id),
                "role": role,  # Assign the role (either 'admin' or the user's assigned role)
                "tenant": "default"  # You can change this to use your own tenant/organization logic
            })
        except Exception as e:
            print(f"[Permit Sync] Error assigning role: {e}")
