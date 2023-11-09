<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { reactive, onMounted, onBeforeMount } from 'vue';

import Visitor_HomeSearchPage from './pages/visitor/search_page.vue';
import Visitor_HomeChatPage from './pages/visitor/chat_page.vue';
import Visitor_DetailPage from './pages/visitor/detail_page.vue';

import { global_dict, global_functions } from './store';

@Component({
    components: {
        Visitor_HomeSearchPage,
        Visitor_HomeChatPage,
        Visitor_DetailPage
    },

    setup() {
        const dict = reactive({
        })

        onBeforeMount(()=>{
            global_functions.go_to_page_based_on_current_url()
        })

        onMounted(async () => {
            //console.log("hi");
        });

        return {
            global_dict,
            global_functions,
            dict,
            increment() {
            },
        };
    },
})

export default class App extends Vue {}
</script>

<template>
    <div id="app">
        <div v-if="global_dict.current_page_name == 'search_page'">
            <Visitor_HomeSearchPage />
        </div>

        <div v-if="global_dict.current_page_name == 'chat_page'">
            <Visitor_HomeChatPage />
        </div>

        <div v-if="global_dict.current_page_name == 'detail_page'">
            <Visitor_DetailPage />
        </div>

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
    height: 100%;
    width: 100%;

    background-color: rgba(224, 224, 224, 1);

    ._columns;
    ._center;
}
</style>
