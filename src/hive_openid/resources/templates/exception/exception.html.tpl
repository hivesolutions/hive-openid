<div id="main-wrapper">
    <div class="error">
        <img class="image image-logo" src="${out value=base_path /}resources/images/hive_openid_service.png" />
        <p class="title">Something went terribly wrong</p>
        <p class="message">${out value=exception_message xml_escape=True /}</p>
    </div>
</div>
