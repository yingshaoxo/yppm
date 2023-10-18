<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { global_dict } from '../store';
import { global_functions } from '../store';

const dict = reactive({
})

const functions = reactive({
  ok: () => {
    global_dict.show_dialog_window = false
    global_dict.dialog_message = ""
  }
})

onMounted(async () => {

})
</script>

<template>
  <div v-if="global_dict.show_dialog_window" class="screen"
    @click="functions.ok"
  >
    <div class="dialog_window" @click.stop="()=>{
      global_functions.copy_text_to_clipboard(global_dict.dialog_message)
      global_dict.dialog_message = 'Message copied.'
      global_functions.execute_a_function_after_x_milliseconds(()=>{
        global_dict.show_dialog_window = false
      }, 1000)
    }">
      <p v-for="sentence in global_dict.dialog_message.split('\n')">{{ sentence }}</p>
      <button @click="functions.ok">OK</button>
    </div>
  </div>
</template>

<style scoped>
.screen {
  z-index: 555;
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

.dialog_window {
  background-color: white;
  color: black;

  padding: 24px;

  max-width: 100%;
  max-height: 60vh;

  overflow-x: auto;
  overflow-y: auto;

  word-break: break-all;
}

button {
  margin-top: 10px;
}
</style>
