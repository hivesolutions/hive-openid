<div id="main-wrapper">
    <div id="user-sidebar">
        <div id="user-pictures">
            <img id="user-avatar" src="${out_none value=openid_user_information.images.gravatar xml_escape=True /}?s=200" />
        </div>
        <div id="user-operations">
            <ul>
                <li>
                    <a class="underline-link" href="${out_none value=base_path /}users/${out_none value=openid_user /}.vcf">
                        Download a vCard
                    </a>
                </li>
            </ul>
        </div>
        <div id="user-description">" ${out_none value=openid_user_information.description xml_escape=True /} "</div>
    </div>
    <div id="content">
        <div class="user-title">
            <h1 class="user-name">${out_none value=openid_user_information.name xml_escape=True /} (${out_none value=openid_user_information.username xml_escape=True /})</h1>
            <h2 class="user-position">${out_none value=openid_user_information.work.position xml_escape=True /}</h2>
        </div>
        <div class="user-info-bar-left">
            <h3 class="user-info-title dark-blue">E-Mail</h3>
            <p class="user-info-text light-black">${out_none value=openid_user_information.email xml_escape=True /}</p>
            <h3 class="user-info-title dark-blue">Work</h3>
            <p class="user-info-text light-black">${out_none value=openid_user_information.work.email xml_escape=True /}</p>
            <h3 class="user-info-title dark-blue">Address</h3>
            <p class="user-info-text light-black">
                ${out_none value=openid_user_information.work.address.street xml_escape=True /} <br />
                ${out_none value=openid_user_information.work.address.zip_code xml_escape=True /}
                ${out_none value=openid_user_information.work.address.city xml_escape=True /} <br />
                ${out_none value=openid_user_information.work.address.country xml_escape=True /}
            </p>
        </div>
        <div class="user-info-bar-right">
            <h3 class="user-info-title dark-blue">Website</h3>
            <p class="user-info-text">
                <a class="underline-link" href="${out_none value=openid_user_information.website xml_escape=True /}">
                    ${out_none value=openid_user_information.website xml_escape=True /}
                </a>
            </p>
            <h3 class="user-info-title dark-blue">Facebook</h3>
            <p class="user-info-text">
                <a class="underline-link" href="${out_none value=openid_user_information.social.facebook xml_escape=True /}">
                    ${out_none value=openid_user_information.social.facebook xml_escape=True /}
                </a>
            </p>
            <h3 class="user-info-title dark-blue">Twitter</h3>
            <p class="user-info-text">
                <a class="underline-link" href="${out_none value=openid_user_information.social.twitter xml_escape=True /}">
                    ${out_none value=openid_user_information.social.twitter xml_escape=True /}
                </a>
            </p>
        </div>
    </div>
</div>
