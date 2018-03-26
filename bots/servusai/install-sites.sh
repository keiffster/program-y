#! /bin/sh

cp ./rest/rest.site /etc/nginx/sites-enabled/rest.site

cp ./web/web.site /etc/nginx/sites-enabled/web.site

cp ./facebook/facebook.site /etc/nginx/sites-enabled/facebook.site

cp ./kik/kik.site /etc/nginx/sites-enabled/kik.site

cp ./line/line.site /etc/nginx/sites-enabled/line.site

cp ./twilio/twilio.site /etc/nginx/sites-enabled/twilio.site

cp ./viber/viber.site /etc/nginx/sites-enabled/viber.site

nginx -t

service nginx restart