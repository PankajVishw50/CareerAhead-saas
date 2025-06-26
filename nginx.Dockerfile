FROM nginx:alpine

RUN mkdir -p ./frontend/dist/

COPY ./frontend/dist/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx.entrypoint.sh nginx.entrypoint.sh

RUN chmod u+x /nginx.entrypoint.sh

EXPOSE 80

ENTRYPOINT [ "./nginx.entrypoint.sh" ]
