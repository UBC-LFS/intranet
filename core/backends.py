from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

from ldap3 import ALL_ATTRIBUTES, SUBTREE, Server, Connection
from ldap3.core.exceptions import LDAPBindError
import json


class CustomLDAPBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        server = Server(settings.INTRANET_LDAP_URI)

        try:
            auth_conn = Connection(
                server,
                user = "uid={},{}".format(username, settings.INTRANET_LDAP_MEMBER_DN),
                password = password,
                authentication = 'SIMPLE',
                check_names = True,
                client_strategy = 'SYNC',
                auto_bind = True,
                raise_exceptions = False
            )

            is_valid = auth_conn.bind()
            if not is_valid:
                return False

            conn = Connection(
                server,
                user = settings.INTRANET_LDAP_AUTH_DN,
                password = settings.INTRANET_LDAP_AUTH_PASSWORD,
                authentication = 'SIMPLE',
                check_names = True,
                client_strategy = 'SYNC',
                auto_bind = True,
                raise_exceptions = False
            )

            conn.bind()

            conn.search(
                search_base = "uid={0},{1}".format(username, settings.INTRANET_LDAP_MEMBER_DN),
                search_filter = settings.INTRANET_LDAP_SEARCH_FILTER,
                search_scope = SUBTREE,
                attributes = ALL_ATTRIBUTES
            )

            entries = json.loads(conn.response_to_json())['entries']

            if len(entries) == 0:
                return None

            attr = entries[0]['attributes']
            username = attr[ settings.LDAP_ATTR_MAP['username'] ][0]
            email = attr[ settings.LDAP_ATTR_MAP['email'] ][0]
            full_name = attr[ settings.LDAP_ATTR_MAP['full_name'] ][0]
            last_name = attr[ settings.LDAP_ATTR_MAP['last_name'] ][0]
            first_name = full_name.split(last_name)[0].strip()

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.first_name = first_name,
                user.last_name = last_name,
                user.email = email
                user.set_unusable_password()
                user.save()

            return user

        except LDAPBindError as e:
            print('LDAPBindError', e)
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None