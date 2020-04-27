from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from ldap3.core.exceptions import LDAPException

from .services.ldapauth import get_ldap_user

import logging

logger = logging.getLogger('app_logger')


class LdapAuthenticationBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug('MyApp: LdapAuthenticationBackend - username %s', username)

        # Authenticate user and get user groups
        try:
            user_email, user_groups = get_ldap_user(username, password)
        except LDAPException as error:
            logger.debug('LDAPException: %s', error)
            return None

        logger.debug('User %s authenticated', username)

        # Create user object
        try:
            user = get_user_model().objects.get(name=username)
        except get_user_model().objects.DoesNotExist:
            user = get_user_model().objects.create_user(name=username)
        return user

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None