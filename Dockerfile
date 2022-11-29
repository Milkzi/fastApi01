FROM nginx
MAINTAINER hucheng<12064936@qq.com>

COPY dist/ /usr/share/nginx/html/
COPY nginx/conf/nginx.conf /etc/nginx/nginx.conf



RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' > /etc/timezone

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]