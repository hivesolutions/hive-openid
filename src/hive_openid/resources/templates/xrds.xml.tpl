<?xml version="1.0" encoding="UTF-8"?>
<xrds:XRDS
    xmlns:xrds="xri://$xrds"
    xmlns:openid="http://openid.net/xmlns/1.0"
    xmlns="xri://$xrd*($v*2.0)">
  <XRD version="2.0">
    <Service priority="0">
      <Type>http://specs.openid.net/auth/2.0/signon</Type>
        <Type>http://openid.net/sreg/1.0</Type>
        <Type>http://openid.net/extensions/sreg/1.1</Type>
        <Type>http://schemas.openid.net/pape/policies/2007/06/phishing-resistant</Type>
        <Type>http://openid.net/srv/ax/1.0</Type>
      <URI>${out value=openid_server xml_escape=True /}</URI>
      <LocalID>${out value=openid_user_base xml_escape=True /}</LocalID>
    </Service>
    <Service priority="1">
      <Type>http://openid.net/signon/1.1</Type>
        <Type>http://openid.net/sreg/1.0</Type>
        <Type>http://openid.net/extensions/sreg/1.1</Type>
        <Type>http://schemas.openid.net/pape/policies/2007/06/phishing-resistant</Type>
        <Type>http://openid.net/srv/ax/1.0</Type>
      <URI>${out value=openid_server xml_escape=True /}</URI>
      <openid:Delegate>${out value=openid_user_base xml_escape=True /}</openid:Delegate>
    </Service>
    <Service priority="2">
      <Type>http://openid.net/signon/1.0</Type>
        <Type>http://openid.net/sreg/1.0</Type>
        <Type>http://openid.net/extensions/sreg/1.1</Type>
        <Type>http://schemas.openid.net/pape/policies/2007/06/phishing-resistant</Type>
        <Type>http://openid.net/srv/ax/1.0</Type>
      <URI>${out value=openid_server xml_escape=True /}</URI>
      <openid:Delegate>${out value=openid_user_base xml_escape=True /}</openid:Delegate>
    </Service>
  </XRD>
</xrds:XRDS>
