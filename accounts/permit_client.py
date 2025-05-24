import os
from dotenv import load_dotenv
from permit import Permit

# Load environment variables from .env file
load_dotenv()

# Check if the required environment variables are present
if not os.getenv("PERMIT_API_KEY"):
    raise ValueError("PERMIT_API_KEY is required in the environment variables.")

# Initialize the Permit client
permit = Permit(
    token=os.getenv("PERMIT_API_KEY"),
    pdp=os.getenv("PERMIT_PDP_URL", "http://localhost:7766")  # Use local PDP URL or adjust as needed
)

# Further code to interact with Permit API, such as assigning roles, syncing users, etc., can be added here.
