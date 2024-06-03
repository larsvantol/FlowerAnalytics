import os

cwd = os.getcwd()
VENV_ACTIVATION_SCRIPT = os.path.join(cwd, "venv", "Scripts", "activate")

# Activate the virtual environment
os.system(VENV_ACTIVATION_SCRIPT)

# Start the Flow Analytics application
os.system("python manage.py runserver")
