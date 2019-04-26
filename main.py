# THIS WILL NOT WORK FROM REPL.IT
# (Or shouldn't; your DC isn't public, right?)
# By the way, are you sure you don't just want
# to use Powershell?
# Well, then. You go, Pythonista.
# http://ldap3.readthedocs.io/
from ldap3 import Server, Connection, ALL, Tls
import ssl

# Domain user with which to access AD
user_dn = 'CN=Recipients,DC=sat,DC=org'
password = 'secret-password'

tls_configuration = Tls(validate=ssl.CERT_OPTIONAL,
      version=ssl.PROTOCOL_TLSv1)
server = Server('localhost/',
     use_ssl=True, get_info=ALL, tls=tls_configuration)
conn = Connection(server, user_dn, password)
conn.start_tls()
conn.bind()
 
# Base DN for searches
base_dn = 'ou=Humans,dc=ourschool,dc=org'
  
# Only search for active users
query_addition = '(!(userAccountControl:1.2.840.113556.1.4.803:=2))'

query = '(&(objectCategory=person)(objectClass=user)' + query_addition + ')'

conn.search(base_dn,
            query,
            attributes=['cn',
              'givenName',
              'displayName',
              'distinguishedName',
              'employeeID',
              'mail',
              'name',
              'sAMAccountName',
              'sn',
              'userPrincipalName',
              ])
for entry in conn.entries:
  # pick your attributes; using name for now
  print(entry.name)
