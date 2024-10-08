<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { reactive, onMounted, onBeforeMount } from 'vue';

import Visitor_HomeSearchPage from './pages/visitor/search_page.vue';
import Visitor_HomeChatPage from './pages/visitor/chat_page.vue';
import Visitor_DetailPage from './pages/visitor/detail_page.vue';

import PopUpPage from './pages/pop_up_page.vue';

import { global_dict, global_functions } from './store';

import { start_the_translation } from './auto_translation';

@Component({
    components: {
        Visitor_HomeSearchPage,
        Visitor_HomeChatPage,
        Visitor_DetailPage,
        PopUpPage
    },

    setup() {
        const dict = reactive({
            need_to_input_username: false,
            username: "",
            admin_token: ""
        })

        const functions = reactive({
            save_username: () => {
                global_functions.set_value('username', dict.username.trim())
                dict.need_to_input_username=false
                global_functions.refresh()
            },
            onFileChange(e: any) {
                var files = e.target.files || e.dataTransfer.files;
                if (!files.length) {
                    return;
                }
                let file = files[0];

                let do_it = async () => {
                    let base64_file = await global_functions.file_to_base64(file)
                    await global_functions.upload_whole_site_data(dict.admin_token, base64_file)
                }
                do_it();
            },
        })

        onBeforeMount(async ()=>{
            await global_functions.set_reachable_client()

            global_functions.go_to_page_based_on_current_url()

            if (global_dict.current_page_name == global_dict.page_name_dict.search_page) {
                if (global_functions.get_value('username') == null) {
                    dict.need_to_input_username = true;
                }
            }
        })

        onMounted(async () => {
            start_the_translation();
        });

        return {
            global_dict,
            global_functions,
            dict,
            functions,
        };
    },
})

export default class App extends Vue {}
</script>

<template>
    <div id="app">
        <PopUpPage :display="dict.need_to_input_username">
            <div class="input_username_window">
                <p>What is your name?</p>
                <input v-model="dict.username" placeholder="Please Input Your Name Here...">
                <button @click="()=>{
                    functions.save_username()
                }">Confirm</button>
            </div>
        </PopUpPage>

        <PopUpPage :display="global_dict.show_global_loading" :z_index="9999">
            <div class="loading_window">
                Loading...
            </div>
        </PopUpPage>

        <PopUpPage :display="global_dict.show_global_message" :z_index="8888">
            <div class="global_message_window">
                {{global_dict.global_message}}
            </div>
        </PopUpPage>

        <PopUpPage :display="global_dict.show_admin_page" :z_index="7777">
            <div class="admin_window">
                <input v-model="dict.admin_token" placeholder="Input Admin Token Here...">
                <br/>
                <br/>
                <br/>
                <button @click="global_functions.download_whole_site_data(dict.admin_token)">Download</button>
                <br/>
                <br/>
                <p>Upload:</p>
                <input type="file" id="myFile" name="filename" @change="functions.onFileChange">
            </div>
        </PopUpPage>

        <div v-if="!dict.need_to_input_username">
            <div v-if="global_dict.current_page_name == 'search_page'">
                <Visitor_HomeSearchPage />
            </div>

            <div v-if="global_dict.current_page_name == 'chat_page'">
                <Visitor_HomeChatPage />
            </div>

            <div v-if="global_dict.current_page_name == 'detail_page'">
                <Visitor_DetailPage />
            </div>
        </div>
    </div>
</template>

<style lang="less">
@import "./assets/css/css_for_human.less";

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;

    margin: 0px;
    min-height: 100vh;
    width: 100%;

    background-color: rgba(224, 224, 224, 1);
}

.input_username_window {
    ._rows;

    padding-top: 80px;
    padding-left: 40px;
    padding-right: 40px;
    background-color: rgba(255,255,255);

    >* {
        margin-bottom: 24px;
    }

    width: 100vw;
    height: 100vh;
    text-align: left;

    input {
        border: 1px solid #000;
        height: 25px;
    }

    button {
        padding: 4px;
    }
}

.loading_window {
    background-color: rgba(0,0,0,0.5);
    color: rgba(255,255,255);

    width: 100vw;
    height: 100vh;

    ._rows;
    ._center;

    font-size: 120%;
}

.global_message_window {
    background-color: rgba(255,255,255,1);

    ._rows();
    ._center();

    width: 100vw;
    height: 100vh;

    padding: 32px;
    font-size: 120%;
}

.admin_window {
    background-color: rgba(255,255,255,1);

    ._rows();
    ._center();

    width: 100vw;
    height: 100vh;

    padding: 32px;
}
</style>
