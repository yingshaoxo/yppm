<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { reactive, onMounted } from 'vue';

import HelloWorld from './components/HelloWorld.vue';

import { global_dict, global_functions } from './store';

@Component({
  components: {
    HelloWorld,
  },
  setup() {
    const dict = reactive({
        count: 0
    })

    onMounted(() => {
      console.log(`The count is: ${dict.count}`);
    });

    return {
      global_dict,
      global_functions,
      dict,
      increment() {
        dict.count++;
        global_functions.hi();
      },
    };
  },
})

export default class App extends Vue {}
</script>

<template>
  <div id="app">
      <div>
        <h1>{{ global_dict.hi }}</h1>
        <h1>The count is: {{ dict.count }}</h1>
        <button @click="increment()">Increment</button>
      </div>
      <!--img alt="Vue logo" src="./assets/logo.png"-->
      <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>
  </div>
</template>

<style lang="less">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
