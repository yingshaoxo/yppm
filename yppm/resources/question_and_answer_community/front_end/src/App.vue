<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { reactive, onMounted, onBeforeMount } from 'vue';

import Visitor_HomeSearchPage from './pages/visitor/search_page.vue';
import Visitor_HomeChatPage from './pages/visitor/chat_page.vue';
import Visitor_DetailPage from './pages/visitor/detail_page.vue';

import PopUpPage from './pages/pop_up_page.vue';

import { global_dict, global_functions } from './store';

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
        })

        const functions = reactive({
            save_username: () => {
                global_functions.set_value('username', dict.username.trim())
                dict.need_to_input_username=false
                global_functions.refresh()
            }
        })

        onBeforeMount(()=>{
            if (global_functions.get_value('username') == null) {
                dict.need_to_input_username = true;
            } else {
                global_functions.go_to_page_based_on_current_url()
            }
        })

        onMounted(async () => {
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

        <template v-if="!dict.need_to_input_username">
            <div v-if="global_dict.current_page_name == 'search_page'">
                <Visitor_HomeSearchPage />
            </div>

            <div v-if="global_dict.current_page_name == 'chat_page'">
                <Visitor_HomeChatPage />
            </div>

            <div v-if="global_dict.current_page_name == 'detail_page'">
                <Visitor_DetailPage />
            </div>
        </template>
        <!--img alt="Vue logo" src="./assets/logo.png"-->
        <!--
        <h1>{{ global_dict.hi }}</h1>
        <h1>The count is: {{ dict.count }}</h1>
        <button @click="increment()">Increment</button>
        -->
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

    ._columns;
    ._center;
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
</style>
