# docker build --tag yingshaoxo/yppm_python3_point_2_in_alpine . --no-cache

# docker run --name test yingshaoxo/yppm_python3_point_2_in_alpine
# docker rm test

#FROM python:3.10-alpine as start_stage
FROM alpine:3.14 as start_stage
#COPY --from=frontend_building_stage /front_end/dist /code/front_end/dist
#COPY ./back_end /code/back_end
#RUN git clone https://gitlab.com/yingshaoxo/auto_everything.git /temp/auto_everything

COPY ./python3.2_static_amd64.run /bin/
COPY ./hello.py /code/example/

WORKDIR /code/example

ENV PYTHONUNBUFFERED=1

#EXPOSE 80
CMD ["python3.2_static_amd64.run", "-c", "print('ying'+'shaoxo'+'666')"]
