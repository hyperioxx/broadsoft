import xml.etree.ElementTree as ET
import html


class XmlDocument:
    def to_string(self, html_encode=False):
        xml = self.to_xml()
        s = '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(xml).decode('utf-8')

        if html_encode:
            s = html.escape(s, quote=True)

        return s