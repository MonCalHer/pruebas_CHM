import unittest
import ldap3


class LdapLoginTest(unittest.TestCase):

    def test_login(self):
      
        ## connect to server
        #auto ldap = LDAP("http://localhost/ControlModelos/Login.aspx");
        #server = 'xy.sat.gob.mx'
        admin_username = 'CAHM878R'
        admin_password = 'bebegato.2019'
        domain = 'dssat.sat.gob.mx' + '\\' + admin_username
        connection = ldap.initialize('LDAP://dssat.sat.gob.mx')
        connection.protocol_version = 3
        connection.set_option(ldap.OPT_REFERRALS, 0)
        connection.simple_bind_s('{0}\{1}'.format(domain, admin_username), admin_password)
        search_username = 'CAHM878R'
        ## search for uid
        #auto r = ldap.search_s("dc=example,dc=com", LDAP_SCOPE_SUBTREE, "(uid=%s)".format("test"));
        base_dn = 'DC=EXAMPLE,DC=COM'
        ldap_filter = '(sAMAccountName={0})'.format(search_username)
        attribs = ['*']
        results = connection.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attribs)
        self.assertIsNotNone(results)
        self.assertGreaterEqual(len(results), 2)
        # grab the first user
        match = results[0]
        self.assertTrue('John' in match[0])
        properties = ['mobile', 'mail', 'lastlogontimestamp', 'userprincipalname', 'lockouttime', 'samaccountname',
                      'logoncount', 'accountexpires', 'lastlogon', 'name', 'company', 'department', 'memberof',
                      'displayname', 'whencreated', 'whenchanged', 'distinguishedname', 'givenname', 'telephonenumber',
                      'description', 'title', 'physicaldeliveryofficename', 'primarygroupid', 'sn', 'cn', 'dn']
        user = dict()
        for key in match[1].keys():
            if key.lower() not in properties:
                continue
            user[key] = match[1][key]
        self.assertEquals(user['sAMAccountName'], search_username)
        connection.unbind()

if __name__ == '__main__':
    unittest.main()