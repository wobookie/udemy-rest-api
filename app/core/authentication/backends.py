from django.contrib.auth.backends import BaseBackend
from core.models import User

from ldap3.core.exceptions import LDAPException

from .services.ldapauth import get_ldap_user

import logging

logger = logging.getLogger('app_logger')


class LdapAuthenticationBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug('MyApp: LdapAuthenticationBackend - username %s', username)

        # Authenticate user and get user email and groups
        try:
            email, groups = get_ldap_user(username, password)
        except LDAPException as error:
            logger.debug('LDAPException: %s', error)
            return None

        logger.debug('User %s authenticated', username)

        # Create user object
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None