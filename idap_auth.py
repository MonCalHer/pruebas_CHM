from ldap3 import 
def get_ldap_connection(dn=None, password=None):
    tls_configuration = None
    use_ssl = False
    try:
        cacert = configuration.get("ldap", "cacert")
        tls_configuration = Tls(validate=ssl.CERT_REQUIRED, ca_certs_file=cacert)
        use_ssl = True
    except:
        pass

    server = Server(configuration.get("ldap", "uri"), use_ssl, tls_configuration)
    conn = Connection(server, native(dn), native(password))

    if not conn.bind():
        log.error("Cannot bind to ldap server: %s ", conn.last_error)
        raise AuthenticationError("Cannot bind to ldap server")

    return conn 