<div id="header">
    <div id="header-wrapper">
        <a href="${out_none value=base_path /}index">
            <div id="logo"></div>
        </a>
        ${if item=session_pt_hive_hive_openid_plugins_main_login value=None operator=eq}
            <div class="button button-login button-dark-green-small" target="${out_none value=base_path /}signin">
                <span class="button-dark-green-small-text">Login</span>
            </div>
            <div class="header-tools">
                <p class="user-signed-status light-black">
                    <span>You are not signed in</span>
                </p>
                <p class="header-links dark-blue">
                    <a class="underline-link" href="${out_none value=base_path /}index">home</a> |
                    <a class="underline-link" href="${out_none value=base_path /}user">recover password</a>
                </p>
            </div>
        ${elif item=session_pt_hive_hive_openid_plugins_main_login value=False operator=eq /}
            <div class="button button-login button-dark-green-small" target="${out_none value=base_path /}signin">
                <span class="button-dark-green-small-text">Login</span>
            </div>
            <div class="header-tools">
                <p class="user-signed-status light-black">
                    <span>You are not signed in</span>
                </p>
                <p class="header-links dark-blue">
                    <a class="underline-link" href="${out_none value=base_path /}index">home</a> |
                    <a class="underline-link" href="${out_none value=base_path /}user">recover password</a>
                </p>
            </div>
        ${else /}
            <div class="button button-logout button-dark-blue-small" target="${out_none value=base_path /}logout">
                <span class="button-dark-blue-small-text">Logout</span>
            </div>
            <div class="header-tools">
                <p class="user-signed-status light-black">
                    <span class="link">openid.hive.pt/<span class="user-signed-status-name">${out_none value=session_pt_hive_hive_openid_plugins_main_user_information.username /}</span></span>
                </p>
                <p class="header-links dark-blue">
                    <a class="underline-link" href="${out_none value=base_path /}index">home</a> |
                    <a class="underline-link" href="${out_none value=base_path /}users/${out_none value=session_pt_hive_hive_openid_plugins_main_user_information.username /}">your account</a> |
                    <a class="underline-link" href="${out_none value=base_path /}domains">your domains</a>
                </p>
            </div>
        ${/if}
    </div>
</div>
<div id="header-shadow"></div>
