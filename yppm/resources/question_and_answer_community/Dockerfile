# docker build --tag yingshaoxo/yppm_question_and_answer_community . --no-cache



FROM node:18 as frontend_building_stage

COPY ./front_end /front_end

WORKDIR /front_end

RUN yarn

RUN GENERATE_SOURCEMAP=false NODE_OPTIONS="--max-old-space-size=8192" yarn build




FROM python:3.10-bullseye as building_stage

RUN pip install "git+https://github.com/yingshaoxo/auto_everything.git@dev" --break-system-packages

COPY ./back_end /code/back_end

COPY --from=frontend_building_stage /front_end/dist /code/front_end/dist

RUN rm -fr /code/back_end/yingshaoxo_chat_data
RUN git clone https://gitlab.com/yingshaoxo/yingshaoxo_txt_data.git /code/back_end/yingshaoxo_chat_data



EXPOSE 54321
WORKDIR /code/back_end
CMD ["python", "main.py"]
