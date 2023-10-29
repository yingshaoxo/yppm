<script setup lang="ts">
import { onBeforeMount, onMounted, reactive } from "vue";

import { PlusOutlined } from '@ant-design/icons-vue';

import dialog_window_page from "./pages/dialog_window_page.vue"

import { global_dict } from "./store";
import { global_functions } from "./store";

let dict = reactive({
    show_user_agreement: false,
    show_add_app_dialog: false,
    an_app: new global_dict.app_store_objects.An_App(),
    question: "1 + 1 = ?",
    answer: ""
})

let functions = reactive({
    on_add_finish: async () => {
        var add_app_request = new global_dict.app_store_objects.Add_App_Request()
        add_app_request.an_app = dict.an_app
        add_app_request.question = dict.question
        add_app_request.answer = dict.answer
        
        let response = await global_dict.client.add_app(add_app_request)
        if ((response?.app_name != null)) {
            await global_functions.print("Add successfully!")
            await global_functions.go_to_page(global_dict.page_name_dict.app_page, {
              name: response?.app_name
            })
        }
    }
})

onBeforeMount(async () => {
    await global_functions.init()

    let agree_value = global_functions.get_value("agree_key", false);
    if (!agree_value) {
        dict.show_user_agreement = true
    }
})
</script>

<template>
    <div class="global_loading" v-if="global_dict.show_global_loading">
        <a-spin size="large" />
    </div>
    
    <dialog_window_page></dialog_window_page>
    
    <component :is="global_dict.page_name_to_component_dict[global_dict.current_page_name]"></component>
    
    <div class="right_floating_button"
        @click="async ()=>{
            dict.show_add_app_dialog = true
        }"
    >
        <PlusOutlined />
    </div>

    <a-modal 
        v-model:visible="dict.show_user_agreement" 
        title="User Agreement" 
        @ok="async () => {
            dict.show_user_agreement = false
            global_functions.set_value('agree_key', true)
        }"
        :destroyOnClose="true"
        :maskClosable="true"
        width="80%" 
    >
        <p>We know other people's products spent millions of words in their user agreement paper, just to express "we are not responsible for the side effects of our product, and we remain every rights about our product and your content in our platform. We could do whatever we want."</p>
        <p>But we are different. We tell you directly: "We are not responsible for the side effects of this product, and we do not censorship any contents inside of this platform, even if its a spam or false advertising. "</p>

        <p class="_less_obvious_text">(Because you never know if an advertising is false one or not unless you lose money, if "a good product" 5 years later has quality issue or not, a censored sentence become truth 10 years later or not.)</p>
        <p class="_less_obvious_text">(You should take responsibility about your copyright or Intelligence_Property leaking, not us.)</p>

        <p>We do not lie.</p>
        <p class="_red">By agreeing this policy, you agree to give up any rights to lawsuit our platform.</p>
    </a-modal>
    
    <a-modal 
        v-model:visible="dict.show_add_app_dialog" 
        title="Add" 
        @ok="async () => {
            dict.show_add_app_dialog = false
            await functions.on_add_finish()
        }"
        :destroyOnClose="true"
        :maskClosable="false"
        width="80%" 
    >
        <a-form
            :model="dict.an_app"
            name="basic"
            :label-col="{ span: 6 }"
            :wrapper-col="{ span: 16 }"
            autocomplete="off"
            @finishFailed="() => {
                global_functions.print('Something is wrong, please check your input!')
            }"
        >
            <a-form-item
                label="Name"
                name="name"
                :rules="[{ required: false, message: 'Please input the name!' }]"
            >
                <a-input v-model:value="dict.an_app.name" />
            </a-form-item>
            
            <a-form-item
              label="Description"
              name="description"
              :rules="[{ required: false, message: 'Please input the description!' }]"
            >
              <a-textarea
                v-model:value="dict.an_app.description"
                auto-size
              />
            </a-form-item>
            
            <a-form-item
              label="URL"
              name="url"
              :rules="[{ required: false, message: 'Please input the url!' }]"
            >
                <a-input v-model:value="dict.an_app.url" />
            </a-form-item>
            
            <a-form-item
              label="Contact"
              name="author_contact_method"
              :rules="[{ required: false, message: 'Please input the contact method!' }]"
            >
                <a-input v-model:value="dict.an_app.author_contact_method" />
            </a-form-item>
            
            <a-form-item
              label="Verify"
              name="verify"
              :rules="[{ required: false, message: 'Please input answer!' }]"
            >
                <div>{{ dict.question }}</div>
                <a-input v-model:value="dict.answer" />
            </a-form-item>
        </a-form>
    </a-modal>
    
    <div class="global_bottom_blank">
    </div>
    
    <div class="bottom_text">
        Do it yourself, freedom is everything.
    </div>
</template>

<style lang="less" scoped>
.right_floating_button {
    position:fixed;

    ._center;

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

.global_bottom_blank {
    height: 40px;
}

.bottom_text {
    position:fixed;

    ._center;

    align-items: center;
    justify-content: center;
    align-content: center;

    width: 100%;

    bottom: 0px;

    background-color:rgba(239, 83, 80, 0.85);

    color:#FFF;
    font-weight: bold;

    text-align:center;

    span {
        margin-right: 8px;
    }
}

.global_loading {
    z-index: 666;
    position: absolute;
    margin: 0;
    padding: 0;
    left: 0;
    top: 0;

    width: 100vw;
    height: 100%;
    min-height: 100vh;
    background-color: rgba(0, 0, 0, 0.6);

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    align-content: center;
}
</style>
