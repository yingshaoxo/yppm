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
            search: async (input: string) => {
                input = input.trim()

                let request = new question_and_answer_objects.Search_Request()
                request.search_input = input
                request.page_size = dict.page_size
                request.page_number = dict.page_number

                let response = await global_dict.client.visitor_search(request)
                console.log(response)
                if (response?.post_list != null) {
                    dict.post_list = response?.post_list
                }
                if (response?.comment_list != null) {
                    dict.comment_list = response?.comment_list
                }
            }
        })

        onMounted(() => {
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
            <textarea class="the_input" @input="()=>{ auto_adjust_input_height(200) }" v-model="dict.input_value"></textarea>
            <button class="the_search_button" @click="functions.search(dict.input_value)">Search</button>
        </div>
        <div class="history_post_list">
            <div class="post_row" v-for="item in dict.post_list">
                <div class="text">
                    {{ item?.title }}
                </div>
            </div>
            <div class="post_row" v-for="item in dict.comment_list">
                <div class="text">
                    {{ item?.description??''.substring(0, 25) }}
                </div>
            </div>
        </div>
        <div class="button_group">
            <button class="button">Next Page</button>
            <button class="button">Previous Page</button>
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
    .the_search_button {
        max-height: 40px;
    }
}

.history_post_list {
    margin-top: 50px;

    width: 95%;
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
}

.button_group {
    margin-top: 50px;

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
</style>
