FROM nginx:alpine

RUN mkdir -p ./frontend/dist/

COPY ./frontend/dist/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
