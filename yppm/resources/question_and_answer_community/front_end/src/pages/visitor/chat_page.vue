<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { reactive, onMounted } from 'vue';

import { global_dict, global_functions } from '../../store';

import type * as question_and_answer_object_types from '../../generated_yrpc/question_and_answer_objects'
import * as question_and_answer_objects from '../../generated_yrpc/question_and_answer_objects'

@Component({
    /*
    components: {
        HomeChatPage,
    },
    */
    setup() {
        const dict = reactive({
            history_context: "",
            input_value: "",
            message_list: [
                {
                    sender: "others",
                    text: "Hi, there!",
                }
            ]
        });

        const functions = reactive({
            send_question: async (input: string) => {
                input = input.trim()

                dict.message_list.unshift({
                    sender: "me",
                    text: input
                })

                dict.history_context += input + "\n"
                let real_input = dict.history_context.substring(dict.history_context.length-800, dict.history_context.length).trim()

                let request = new question_and_answer_objects.Ask_Yingshaoxo_Ai_Request()
                request.input = real_input
                let response = await global_dict.client.ask_yingshaoxo_ai(request)
                if (response?.answers != null) {
                    // add answers to list view
                    dict.message_list.unshift({
                        sender: "others",
                        text: response?.answers
                    })
                    
                }
            }
        })

        onMounted(() => {
            //console.log("hi");
        });

        return {
            global_dict,
            global_functions,
            dict,
            functions,
        };
    },
})

export default class Visitor_Home_Chat_Page extends Vue {
    auto_adjust_input_height(height_limit: any) {
        const input = document.querySelector('.the_input') as HTMLInputElement;
        const input_container = document.querySelector('.input_container') as HTMLInputElement;

        input.style.height = 'auto';
        let new_height = input.scrollHeight;
        if (new_height <= height_limit) {
            input.style.height = new_height + 'px';
            input_container.style.marginBottom = Math.min(new_height, 80) + 'px';
        } else {
            input.style.height = height_limit + 'px';
        }
    }
}
</script>

<template>
    <div class="full_screen">
        <div class="input_container _columns">
            <textarea class="the_input" @input="()=>{ auto_adjust_input_height(200) }" v-model="dict.input_value"
                placeholder="What you want to know?"
            ></textarea>
            <button class="the_send_button" @click="functions.send_question(dict.input_value)">Send</button>
        </div>
        <div class="history_message_list">
            <div v-for="message in dict.message_list">
                <div class="message_row" :class="{'message_me': message.sender=='me', 'message_other': message.sender=='others'}">
                    <div class="message message_other_color" :class="{'message_me_color': message.sender=='me', 'message_other_color': message.sender=='others'}">
                        <pre>{{ message?.text }}</pre>
                    </div>
                </div>
            </div>
            <!--div class="message_row message_other">
                <div class="message message_other_color">
                    Hi, yingshaoxo
                </div>
            </div>
            <div class="message_row message_me">
                <div class="message message_me_color">
                    Hi, stranger.
                </div>
            </div-->
        </div>
    </div>
</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import "../../assets/css/css_for_human.less";

.full_screen {
    width: 98vw;
    height: 100vh;

    ._rows;
    ._horizontal_center;
}

.input_container {
    margin-top: 25px;

    max-height: 100px;
    width: 100%;
    justify-content: space-between;
    
    .the_input {
        width: 100%;
    }
    .the_send_button {
        max-height: 40px;
    }
}

.history_message_list {
    margin-top: 50px;

    width: 95%;
    height: 80vh;

    overflow: auto;

    ._rows;

    .message_row {
        width: 100%;
        margin-bottom: 25px;
        ._columns;
    }

    .message_other {
        justify-content: flex-start;
        text-align: left;
    }

    .message_me {
        justify-content: flex-end;
        text-align: right;
    }

    .message_other_color {
        background-color: rgba(255, 255, 255, 1);
    }

    .message_me_color {
        background-color: rgba(203, 242, 207, 1);
    }

    .message {
        width: 80%;
        min-height: 30px;
        padding: 16px;
        border-radius: 8px;
    }
}

pre{ 
    white-space: pre-wrap; 
    word-break: break-word;
}
</style>
