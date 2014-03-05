BEGIN:VCARD
VERSION:3.0
ADR:;;${out value=openid_user_information.work.address.street /};${out value=openid_user_information.work.address.city /};${out value=openid_user_information.work.address.city /};${out value=openid_user_information.work.address.zip_code /};${out value=openid_user_information.work.address.country /}
EMAIL:${out value=openid_user_information.email /}
FN:${out value=openid_user_information.name /}
N:${out value=openid_user_information.last_name /};${out value=openid_user_information.first_name /};;;
ORG:${out value=openid_user_information.work.company /}
PHOTO:${out value=openid_user_information.images.gravatar /}
TEL;TYPE=WORK:${out value=openid_user_information.work.email /}
TITLE:${out value=openid_user_information.work.position /}
END:VCARD
