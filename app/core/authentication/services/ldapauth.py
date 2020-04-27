from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPException
from django.conf import settings
from itertools import chain

import logging
logger = logging.getLogger('app_logger')


# Check user users in the LDAP and return his information
def get_ldap_user(username, password):
    ldap_url = settings.JUMPCLOUD_URL
    bind_dn = 'uid={username},{dn}'.format(
        username=username,
        dn=settings.JUMPCLOUD_DN
    )

    try:
        ldap_server = Server(ldap_url, get_info=ALL, use_ssl=True)
        logger.debug('ldap_server: %s', str(ldap_server))
        ldap_cnx = Connection(ldap_server, bind_dn, password, auto_bind=True)
    except LDAPException as error:
        logger.debug('LDAPException: %s', error)
        raise LDAPException(error)

    # get user email from ldap - we allow for empty email
    search_str = '(&(objectClass=person)(uid={username}))'.format(
        username=username
    )
    ldap_cnx.search(settings.JUMPCLOUD_DN, search_str, attributes=['mail'])
    user_email = None
    if len(ldap_cnx.response) > 0:
        user_email = ldap_cnx.response[0]['attributes']['mail'][0]

    # search all groups the user is in and flatten the list of groups
    search_str = '(&(objectClass=groupOfNames)(member=uid={username},ou=Users,{dn}))'.format(
        username=username,
        dn=settings.JUMPCLOUD_DN
    )

    ldap_cnx.search(settings.JUMPCLOUD_DN, search_str, attributes=['cn'])
    user_groups = list(
        chain.from_iterable(
            [val['attributes']['cn'] for val in ldap_cnx.response]
        ))

    return user_email, user_groups
