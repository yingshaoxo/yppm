<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { reactive, onMounted } from 'vue';

import HomeChatPage from './pages/visitor/home_chat_page.vue';

import { global_dict, global_functions } from './store';

@Component({
    components: {
        HomeChatPage,
    },

    setup() {
        const dict = reactive({
        })

        onMounted(() => {
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
        <div>
            <HomeChatPage />
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
