${include file="doctype.html.tpl" /}
<head>
    <title>${out_none value=title xml_escape=True /}</title>
    ${include file="content_type.html.tpl" /}
    ${include file="openid_references.html.tpl" /}
    ${include file="includes.html.tpl" /}
</head>
<body>
    ${include file="header.html.tpl" /}
    <div id="content-wrapper">
        ${include file_value=page_include /}
    </div>
    ${include file="footer.html.tpl" /}
</body>
${include file="end_doctype.html.tpl" /}
