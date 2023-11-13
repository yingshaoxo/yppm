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
            page_size: 10,
            page_number: 0,
            post_list: [] as any[],
            comment_list: [] as any[],
        });

        const functions = reactive({
            search: async () => {
                let input = dict?.input_value.trim()
                dict.input_value = input
                window.history.pushState({}, dict.input_value, `./?search_text=${dict.input_value}`)

                let request = new question_and_answer_objects.Search_Request()
                request.search_input = input
                request.page_size = dict.page_size
                request.page_number = dict.page_number

                let response = await global_dict.client.visitor_search(request)
                if (response?.post_list != null) {
                    dict.post_list = response?.post_list
                }
                if (response?.comment_list != null) {
                    dict.comment_list = response?.comment_list
                }
            },
            jump_to_detail_page: async (item: any) => {
                global_functions.go_to_page("detail_page", {id: item?.id})
            },
            jump_to_detail_page_with_comment_object: async (item: any) => {
                global_functions.go_to_page("detail_page", {id: item?.parent_post_id})
            }
        })

        onMounted(async () => {
            if (global_dict?.current_page_data?.search_text != null) {
                dict.input_value = global_dict?.current_page_data?.search_text
            }
            await functions.search()
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
            <textarea class="the_input" @input="()=>{ auto_adjust_input_height(200) }" v-model="dict.input_value" v-on:keyup.enter="functions.search"></textarea>
            <button class="the_search_button" @click="functions.search()">Search</button>
        </div>
        <div class="history_post_list">
            <div class="post_row" v-for="item in dict.post_list"
                @click="functions.jump_to_detail_page(item)"
            >
                <div class="text">
                    <span class="question_indicator">Question</span>: {{ item?.title }}
                </div>
            </div>
            <div class="post_row" v-for="item in dict.comment_list"
                @click="functions.jump_to_detail_page_with_comment_object(item)"
            >
                <div class="text">
                    <span class="comment_indicator">Answer</span>: {{ item?.description??''.substring(0, 25) }}
                </div>
            </div>
        </div>
        <div class="button_group">
            <button class="button" @click="()=>{dict.page_number += 1; functions.search();}">Next Page</button>
            <button class="button" @click="()=>{dict.page_number -= 1; functions.search();}">Previous Page</button>
        </div>

        <div class="right_floating_button"
            @click="()=>{
                global_functions.go_to_page('detail_page', {})
            }"
        >
            <span>+</span>
        </div>

        <div class="left_floating_button"
            @click="()=>{
                global_functions.go_to_page('chat_page', {})
            }"
        >
            <span>?</span>
        </div>
    </div>
</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import "../../assets/css/css_for_human.less";

.full_screen {
    width: 95vw;
    height: 100vh;

    ._rows;
    ._horizontal_center;
}

.input_container {
    margin-top: 35px;

    max-height: 100px;
    width: 96%;
    justify-content: space-between;
    
    .the_input {
        width: 100%;
    }
    .the_search_button {
        max-height: 40px;
    }
}

.history_post_list {
    margin-top: 50px;

    width: 95%;
    height: 100%;
    text-align: left;

    ._rows;

    .post_row {
        width: 100%;
        padding-top: 25px;
        padding-bottom: 25px;
        margin-bottom: 8px;
        background-color: #FAFAFA;

        .text {
            padding-left: 15px;
            padding-right: 15px;
        }
    }

    .question_indicator {
        font-weight: bold;
        color: #D32F2F;
    }

    .comment_indicator {
        font-weight: bold;
        color: #757575;
    }
}

.button_group {
    margin-top: 50px;
    margin-bottom: 50px;

    width: 100%;
    
    .button {
        width: 120px;
        &:first-child {
            margin-right: 64px;
        }
    }
}

pre{ 
    white-space: pre-wrap; 
    word-break: break-word;
}

.right_floating_button {
    position:fixed;
    font-size: 150%;

    ._rows();
    ._center();

    width:40px;
    height:40px;

    bottom:40px;
    right:20px;

    background-color:rgba(239, 83, 80);

    color:#FFF;
    font-weight: bold;

    border-radius:50px;
    text-align:center;
    box-shadow: 2px 2px 3px #999;
}

.left_floating_button {
    .right_floating_button;

    right: auto;
    left: 20px;

    background-color: rgba(245, 127, 23);

    font-size: 150%;
}
</style>
