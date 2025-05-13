import sys
import traceback
import os

# Print environment for debugging
print("Current directory:", os.getcwd())
print("Directory contents:", os.listdir())
print("Environment variables:", dict(os.environ))

try:
    print("Attempting to import application...")
    from application import app
    print("Successfully imported application")
    
    # Try to initialize the app without running the server
    print("Application imported successfully")
    print("Application routes:", [route for route in app.routes])
    
except Exception as e:
    print("Exception occurred:", str(e))
    print("Detailed traceback:")
    traceback.print_exc()
    sys.exit(1)

print("All imports successful. Script completed.")
