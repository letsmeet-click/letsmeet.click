from .base import *

DEBUG = True

AUTH_PASSWORD_VALIDATORS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'test_shahng3oothai4Eaneehai4Eiquohv6quohkouzah8aibeehiupieSieBohCub7d'

SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# SHACKSPACE = True

try:
    from .local import *
except ImportError:
    pass
