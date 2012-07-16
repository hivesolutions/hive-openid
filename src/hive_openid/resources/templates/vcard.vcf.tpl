BEGIN:VCARD
VERSION:3.0
ADR:;;${out_none value=openid_user_information.work.address.street /};${out_none value=openid_user_information.work.address.city /};${out_none value=openid_user_information.work.address.city /};${out_none value=openid_user_information.work.address.zip_code /};${out_none value=openid_user_information.work.address.country /}
EMAIL:${out_none value=openid_user_information.email /}
FN:${out_none value=openid_user_information.name /}
N:${out_none value=openid_user_information.last_name /};${out_none value=openid_user_information.first_name /};;;
ORG:${out_none value=openid_user_information.work.company /}
PHOTO:${out_none value=openid_user_information.images.gravatar /}
TEL;TYPE=WORK:${out_none value=openid_user_information.work.email /}
TITLE:${out_none value=openid_user_information.work.position /}
END:VCARD
