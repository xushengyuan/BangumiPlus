import xmlrpc.client
s = xmlrpc.client.ServerProxy('http://localhost:6800/rpc')
s.aria2.addUri(['http://example.org/file'])
