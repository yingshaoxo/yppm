# docker build --tag yingshaoxo/yppm_question_and_answer_community . --no-cache



FROM node:18 as frontend_building_stage

COPY ./front_end /front_end

WORKDIR /front_end

RUN yarn

RUN GENERATE_SOURCEMAP=false NODE_OPTIONS="--max-old-space-size=8192" yarn build



FROM python:3.10-bullseye as building_stage

COPY ./back_end /code/back_end
RUN git clone https://gitlab.com/yingshaoxo/auto_everything.git /temp/auto_everything
RUN cp -fr /temp/auto_everything/auto_everything /code/back_end/auto_everything

COPY --from=frontend_building_stage /front_end/dist /code/front_end/dist

RUN rm -fr /code/back_end/yingshaoxo_chat_data
RUN git clone https://gitlab.com/yingshaoxo/yingshaoxo_txt_data.git /code/back_end/yingshaoxo_chat_data



FROM python:3.10-alpine as final_stage

COPY --from=building_stage /code /code



EXPOSE 54321
WORKDIR /code/back_end
CMD ["python", "main.py"]
