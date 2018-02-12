"""
    Simple Python script to delete standard acl 

    Installing python dependencies:
    > pip install lxml ncclient

    Running script: (save as delete-standard-acl.py)
    > python delete-standard-acl.py -a <device-ip> -u <username> -p <password> --port 830
    > For example:
    > python delete-standard-acl.py -a 172.26.249.167 -u cisco -p cisco --port 830
"""

import lxml.etree as ET
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError

payload = """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" xmlns:ios-acl="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
    <ip>
      <access-list>
        <ios-acl:standard xc:operation="delete">
          <ios-acl:name>MANAGEMENT</ios-acl:name>
        </ios-acl:standard>
      </access-list>
    </ip>
  </native>
</config>
"""

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'csr'}) as m:

        # execute netconf operation
        try:
            response = m.edit_config(target='running', config=payload).xml
            data = ET.fromstring(response)
        except RPCError as e:
            data = e._raw

        # beautify output
        print(ET.tostring(data, pretty_print=True))

