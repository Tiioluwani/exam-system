# accounts/permit_utils.py

import asyncio
import os
from permit import Permit

# Initialize Permit SDK
permit = Permit(token=os.getenv("PERMIT_API_KEY"))

async def async_sync_user_with_permit(user):
    try:
        if not hasattr(user, "role") or not user.role:
            print(f"[Permit Sync ❌] Skipping user {user.email if hasattr(user, 'email') else 'Unknown'} — Role missing")
            return

        user_data = {
            "key": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "attributes": {
                "role": user.role,
            }
        }
        print(f"[DEBUG SYNC] Sending user to Permit: {user_data}")

        await permit.api.users.sync(user_data)
        print(f"[Permit Sync ✅] Synced {user.email}")

    except Exception as e:
        print(f"[Permit Sync ❌] Failed: {e}")

def sync_user_with_permit(user):
    # Wrapper to run async inside Django
    try:
        asyncio.run(async_sync_user_with_permit(user))
    except RuntimeError:
        # If already inside event loop (very rare), just schedule it
        loop = asyncio.get_event_loop()
        loop.create_task(async_sync_user_with_permit(user))
