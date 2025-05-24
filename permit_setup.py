from permit import Permit
import os

def sync_permit_roles_and_permissions():
    try:
        # Initialize Permit SDK with API Key and PDP URL from environment variables
        permit = Permit(
            token=os.getenv("PERMIT_API_KEY"),  # Replace with your actual Permit API Key from environment variables
            pdp=os.getenv("PERMIT_PDP_URL", "http://localhost:7766"),  # Adjust if needed
            log={"level": "debug", "enable": True},  # Optional: Debugging log
        )

        # Create roles in Permit
        admin_role = permit.api.roles.create(
            {
                "key": "admin",
                "name": "Admin",
                "description": "Admin role with full access",
                "permissions": ["document:create", "document:read", "document:update", "document:delete"]
            }
        )

        student_role = permit.api.roles.create(
            {
                "key": "student",
                "name": "Student",
                "description": "Student role with limited access",
                "permissions": ["document:read"]
            }
        )

        # Create resources in Permit (e.g., document)
        permit.api.resources.create(
            {
                "key": "document",
                "name": "Document",
                "urn": "prn:gdrive:document",
                "actions": {
                    "create": {},
                    "read": {},
                    "update": {},
                    "delete": {},
                },
                "attributes": {
                    "private": {
                        "type": "bool",
                        "description": "Whether the document is private",
                    },
                },
            }
        )

        print("✅ Roles and Resources synced successfully.")
    except Exception as e:
        print(f"❌ Error syncing roles and resources: {e}")

# Run this script to sync roles and resources
if __name__ == "__main__":
    if not os.getenv("PERMIT_API_KEY"):
        print("❌ PERMIT_API_KEY environment variable is missing.")
    else:
        sync_permit_roles_and_permissions()
