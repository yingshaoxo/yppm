<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { reactive, onMounted } from 'vue';

import { global_dict, global_functions } from '../../store';

import type * as question_and_answer_object_types from '../../generated_yrpc/question_and_answer_objects'
import * as question_and_answer_objects from '../../generated_yrpc/question_and_answer_objects'

import PopUpPage from '../pop_up_page.vue';

import snarkdown from 'snarkdown'

@Component({
    components: {
        PopUpPage,
    },
    setup() {
        const dict = reactive({
            create_new_post_mode: false,
            a_new_post: new question_and_answer_objects.A_Post(),
            a_new_comment: new question_and_answer_objects.A_Comment(),
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
            special_comment: new question_and_answer_objects.A_Comment(),
            show_special_comment: false,
        });

        const functions = reactive({
            get_a_post: async () => {
                let request = new question_and_answer_objects.Get_A_Post_Request()
                request.id = dict?.a_post?.id
                let response = await global_dict.client.visitor_get_a_post(request)
                if (response?.post != null) {
                    dict.a_post = response?.post
                    dict.a_post.description = snarkdown(dict?.a_post?.description??'')??''
                    if (dict?.a_post?.comment_id_list != null) {
                        let request2 = new question_and_answer_objects.Get_Comment_List_By_Id_List_Request()
                        request2.comment_id_list = dict?.a_post?.comment_id_list
                        let response2 = await global_dict.client.visitor_get_comment_list_by_id_list(request2)
                        if (response2?.comment_list != null) {
                            dict.comment_list = response2?.comment_list
                            for (let i = 0; i < dict.comment_list.length; i++) {
                                if (dict.comment_list[i].owner_id == "") {
                                    dict.comment_list[i].owner_id = "anonymous"
                                }
                                if (dict.comment_list[i].description != null) {
                                    dict.comment_list[i].description = snarkdown(dict?.comment_list[i]?.description??'')
                                } 
                            }
                            let length = dict?.comment_list?.length
                            let half_length = Math.round(length / 2)
                            dict.left_old_list = dict?.comment_list.slice(0, half_length)
                            dict.right_new_list = dict?.comment_list.slice(half_length, length)
                            dict.right_new_list.reverse();
                        }
                    }
                }
            },
            create_a_post: async () => {
                let request = new question_and_answer_objects.Add_Post_Request()
                request.username = global_functions.get_username()
                request.a_post = dict?.a_new_post
                let response = await global_dict.client.user_add_post(request)
                if (response?.post_id != null) {
                    // do a reloading with that post id
                    global_functions.go_to_page("detail_page", {id: response?.post_id})
                }
            },
            create_a_comment: async () => {
                let request = new question_and_answer_objects.Comment_Post_Request()

                dict.a_new_comment.parent_post_id = dict.a_post.id;
                dict.a_new_comment.parent_post_owner_id = dict.a_post.owner_id;
                request.a_comment = dict?.a_new_comment
                request.username = global_functions.get_username()

                let response = await global_dict.client.user_comment_post(request)
                if (response?.comment_id != null) {
                    // do a reloading with that post id
                    global_functions.refresh()
                }
            },
            set_and_show_a_special_comment: (item: any) => {
                dict.special_comment = item
                dict.show_special_comment = true
            }
        })

        onMounted(async () => {
            if (global_dict?.current_page_data?.id != null) {
                dict.a_post.id = global_dict?.current_page_data?.id
                await functions.get_a_post()
            } else {
                dict.create_new_post_mode = true
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
    auto_adjust_input_height(class_name: any, height_limit: any) {
        const input = document.querySelector(`.${class_name}`) as HTMLInputElement;

        input.style.height = 'auto';
        let new_height = input.scrollHeight;
        if (new_height <= height_limit) {
            input.style.height = new_height + 'px';
        } else {
            input.style.height = height_limit + 'px';
        }
    }
}
</script>

<template>
    <div class="full_screen">
        <div class="detail_view_container">
            <h1 class="title">
                {{dict.a_post.title}}
            </h1>

            <div class="post_seperator" v-if="dict.a_post.description.trim().startsWith('<h')">
            </div>

            <div class="description">
                <div v-html="dict.a_post.description"></div>
            </div>
            <div class="author">
                <span v-if="dict?.a_post?.owner_id == ''">@anonymous</span>
                <span v-if="dict?.a_post?.owner_id != ''">@{{dict.a_post.owner_id}}</span>
            </div>

            <div class="post_seperator">
            </div>

            <div class="new_comment_container">
                <textarea class="the_textarea_2" v-model="dict.a_new_comment.description" placeholder="Say Something Here..." @input="()=>{ auto_adjust_input_height('the_textarea_2', 200) }"></textarea>
                <button @click="functions.create_a_comment">Answer</button>
            </div>

            <div class="post_seperator">
            </div>

            <div class="comment_list">
                <div class="left_old_list">
                    <div v-for="item in dict.left_old_list" class="one_comment" @click="functions.set_and_show_a_special_comment(item)">
                        <div class="owner_id">{{ item?.owner_id }}: </div>
                        <div class="description" v-html="item?.description"></div>
                    </div>
                </div>
                <div class="right_new_list">
                    <div v-for="item in dict.right_new_list" class="one_comment" @click="functions.set_and_show_a_special_comment(item)">
                        <div class="owner_id">{{ item?.owner_id }}: </div>
                        <div class="description" v-html="item?.description"></div>
                    </div>
                </div>
            </div>
        </div>

        <PopUpPage :display="dict.create_new_post_mode">
            <div class="create_new_post_mode">
                <div class="new_post_container">
                    <p>What is your question title?</p>
                    <input v-model="dict.a_new_post.title" placeholder="Please Input Your Question Title Here...">
                    <p>What is your question description?</p>
                    <textarea class="the_textarea" v-model="dict.a_new_post.description" placeholder="Please Input Your Question Description Here..." @input="()=>{ auto_adjust_input_height('the_textarea', 400) }"></textarea>
                    <button @click="functions.create_a_post">Confirm</button>
                </div>
            </div>
        </PopUpPage>

        <PopUpPage :display="dict.show_special_comment">
            <div class="create_new_post_mode">
                <div class="new_post_container">
                    <div class="special_owner_id">{{ dict?.special_comment?.owner_id }}: </div>
                    <div v-html="dict?.special_comment?.description"></div>
                    <button @click="()=>{
                        dict.show_special_comment = false
                    }">Return</button>
                </div>
            </div>
        </PopUpPage>
    </div>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import "../../assets/css/css_for_human.less";

.full_screen {
    width: 100vw;
    min-height: 100vh;

    ._rows;
    ._horizontal_center;
}

.detail_view_container {
    margin-top: 20px;

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

    .new_comment_container {
        margin-top: 35px;
        margin-bottom: 35px;
        width: 100%;

        ._columns();
        ._horizontal_center();

        .the_textarea_2 {
            margin-left: 8px;
            width: 100%;
            min-height: 25px;
        }

        button {
            margin-right: 8px;
            height: 35px;
            padding: 4px;
        }
    }
}

.comment_list {
    margin-top: 50px;

    width: 100%;

    overflow: auto;

    ._columns;
    ._center;

    .left_old_list {
        padding: 4px;

        background-color: rgba(241, 248, 233, 0.2);
        width: 50%;
        height: 100vh;
    }

    .right_new_list {
        padding: 4px;

        background-color: rgba(187, 222, 251, 0.2);
        width: 50%;
        height: 100vh;
    }

    .one_comment {
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .owner_id {
        font-weight: bold;
        margin-bottom: 8px;
    }

    .description {
        margin-bottom: 32px;
    }
}

pre{ 
    white-space: pre-wrap; 
    word-break: break-word;
}

.create_new_post_mode {
    background-color: rgba(255,255,255);

    ._rows();
    ._horizontal_center();

    width: 100vw;
    height: 100vh;
    text-align: left;

    .new_post_container {
        margin-top: 35px;
        width: 88%;

        ._rows();
        padding-left: 8px;
        padding-right: 8px;
        >* {
            margin-bottom: 20px;
        }

        .the_textarea {
            min-height: 100px;
        }

        button {
            margin-top: 15px;
            padding: 4px;
        }
    }
}

.special_owner_id {
    font-weight: bold;
    margin-bottom: 48px;
}

</style>

<style lang="less">
    .description {
        /* Reset default margin and padding */
            body, h1, h2, h3, h4, h5, h6, p {
            margin: 0;
            padding: 0;
        }

        /* Set the font and color */
        body {
            font-family: Arial, sans-serif;
            color: #333;
        }

        /* Styling for heading tags */
        h1, h2, h3, h4 {
            margin: 16px 0;
        }

        h1 {
            font-size: 2em;
        }

        h2 {
            font-size: 1.5em;
        }

        h3 {
            font-size: 1.17em;
        }

        h4 {
            font-size: 1em;
        }

        /* Styling for paragraphs */
        p {
            margin: 12px 0;
            line-height: 1.6;
        }

        /* Styling for code blocks */
        pre {
            background-color: #f4f4f4;
            padding: 8px;
            border-radius: 3px;
            overflow-x: auto;
        }

        code {
            font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
        }

        /* Styling for blockquotes */
        blockquote {
            margin: 12px 0;
            padding: 8px 16px;
            background-color: #f7f7f7;
            border-left: 4px solid #ddd;
        }
    }
</style>
