from commands.base import BaseStemAppCommand


class SetupStemAppCommand(BaseStemAppCommand):
    def __init__(self, setup_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_type = setup_type
        # TODO: check that we have the settings for this

    def run(self):
        context = {
            "secret_key": random_string()
        }
        # Check if postgres and redis are not installed and offer to install them
        # Install npm and python dependencies
        # Create files in .gitignore (local_settings.py)
        # Generate a new DB, if needed
        # Ask if user wants to import a DB from somewhere
        # Apply migrations to DB
        # Create a new superuser account (if desired)
        # Build the js
        # [production] install fail2ban, nginx, etc.
        # [production] setup sysctl.conf and security limits
        # [production] generate a HTTPS key
