import unittest.mock
import xml.etree.ElementTree as ET
import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.requestobjects.UserGetListInGroupRequest import UserGetListInGroupRequest


def return_users_list(**kwargs):
    return '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;ISO-8859-1&quot;?&gt;&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;Chriss-MacBook-Pro-4.local,2017-06-12 20:31:26.721149,2059102188&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;UserGetListInGroupResponse&quot; xmlns=&quot;&quot;&gt;&lt;userTable&gt;&lt;colHeading&gt;User Id&lt;/colHeading&gt;&lt;colHeading&gt;Last Name&lt;/colHeading&gt;&lt;colHeading&gt;First Name&lt;/colHeading&gt;&lt;colHeading&gt;Department&lt;/colHeading&gt;&lt;colHeading&gt;Phone Number&lt;/colHeading&gt;&lt;colHeading&gt;Phone Number Activated&lt;/colHeading&gt;&lt;colHeading&gt;Email Address&lt;/colHeading&gt;&lt;colHeading&gt;Hiragana Last Name&lt;/colHeading&gt;&lt;colHeading&gt;Hiragana First Name&lt;/colHeading&gt;&lt;colHeading&gt;In Trunk Group&lt;/colHeading&gt;&lt;colHeading&gt;Extension&lt;/colHeading&gt;&lt;colHeading&gt;Country Code&lt;/colHeading&gt;&lt;colHeading&gt;National Prefix&lt;/colHeading&gt;&lt;row&gt;&lt;col&gt;2212221101@broadsoft-dev.mit.edu&lt;/col&gt;&lt;col&gt;Beaver&lt;/col&gt;&lt;col&gt;Tim&lt;/col&gt;&lt;col/&gt;&lt;col&gt;+1-2212221101&lt;/col&gt;&lt;col&gt;true&lt;/col&gt;&lt;col&gt;beaver@mit.edu&lt;/col&gt;&lt;col&gt;Beaver&lt;/col&gt;&lt;col&gt;Tim&lt;/col&gt;&lt;col&gt;false&lt;/col&gt;&lt;col&gt;1101&lt;/col&gt;&lt;col&gt;1&lt;/col&gt;&lt;col/&gt;&lt;/row&gt;&lt;/userTable&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'


class TestBroadsoftUserGetListInGroupRequest(unittest.TestCase):
    def test_to_xml(self):
        b = broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance()

        # group id/case insensitive True
        g = UserGetListInGroupRequest(broadsoftinstance=b)

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + g.broadsoftinstance.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="UserGetListInGroupRequest">' +
                    '<serviceProviderId>' + b.service_provider + '</serviceProviderId>' +
                    '<GroupId>' + g.group_id + '</GroupId>' +
                    '<responseSizeLimit>' + str(g.response_size_limit) + '</responseSizeLimit>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )
