from django.conf import settings

def check():
    """Perform general configuration verifications"""
    if not len(settings.ADMINS):
        raise ConfigurationError("The ADMINS configuration option must be set in settings.py.")

class ConfigurationError(Exception):
    pass
