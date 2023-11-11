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
            a_post: {
                owner_id: "",
                id: "",
                title: "Hi",
                description: "You are died.",
                comment_id_list: ["1", "2"],
                create_time_in_10_numbers_timestamp_format: null,
                tag: null, // for example, [ad, spam, adult]
            } as question_and_answer_object_types.A_Post,
            comment_list: [] as any,
            left_old_list: [] as any,
            right_new_list: [] as any,
        });

        const functions = reactive({
            get_a_post: async () => {
                let request = new question_and_answer_objects.Get_A_Post_Request()
                request.id = dict?.a_post?.id
                let response = await global_dict.client.visitor_get_a_post(request)
                if (response?.post != null) {
                    dict.a_post = response?.post
                    if (dict?.a_post?.comment_id_list != null) {
                        let request2 = new question_and_answer_objects.Get_Comment_List_By_Id_List_Request()
                        request2.comment_id_list = dict?.a_post?.comment_id_list
                        let response2 = await global_dict.client.visitor_get_comment_list_by_id_list(request2)
                        if (response2?.comment_list != null) {
                            dict.comment_list = response2?.comment_list
                            let length = dict?.comment_list?.length
                            let half_length = Math.round(length / 2)
                            dict.left_old_list = dict?.comment_list.slice(0, half_length)
                            dict.right_new_list = dict?.comment_list.slice(half_length, length)
                            dict.right_new_list.reverse();
                        }
                    }
                }
            }
        })

        onMounted(() => {
            if (global_dict?.current_page_data?.id != null) {
                dict.a_post.id = global_dict?.current_page_data?.id
            }
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
        <div class="detail_view_container">
            <h2 class="title">
                {{dict.a_post.title}}
            </h2>
            <div class="description">
                {{dict.a_post.description}}
            </div>
            <div class="author">
                @{{dict.a_post.owner_id}}
            </div>

            <div class="post_seperator">
            </div>

            <div class="comment_list">
                <div class="left_old_list">
                    <div v-for="item in dict.left_old_list">
                        <span>{{ item?.owner_id }}:</span>
                        <span>{{item?.description}}</span>
                    </div>
                </div>
                <div class="right_new_list">
                    <div v-for="item in dict.right_new_list">
                        <span>{{ item?.owner_id }}:</span>
                        <span>{{item?.description}}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import "../../assets/css/css_for_human.less";

.full_screen {
    width: 98vw;
    min-height: 100vh;

    ._rows;
    ._horizontal_center;
}

.detail_view_container {
    margin-top: 25px;

    width: 100%;
    text-align: left;

    .title {
        padding-left: 16px;
        padding-right: 16px;
    }

    .description {
        padding-left: 16px;
        padding-right: 16px;
    }

    .author {
        ._less_obvious_text;
        margin-top: 10px;
        text-align: right;

        padding-left: 16px;
        padding-right: 16px;
    }

    .post_seperator {
        width: 100%;
        height: 1px;
        background-color: rgba(0,0,0);

        margin-top: 16px;
        margin-bottom: 16px;
    }
}

.comment_list {
    margin-top: 50px;

    width: 100%;

    overflow: auto;

    ._columns;

    .left_old_list {
        padding: 4px;

        background-color: #FF8A80;
        width: 50%;
    }

    .right_new_list {
        padding: 4px;

        background-color: #BBDEFB;
        width: 50%;
    }

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
