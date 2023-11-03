<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component

export default class Visitor_Home_Chat_Page extends Vue {
}
</script>

<template>
    <div class="full_screen">
        <div class="history_message_list">
            <div class="message_other">Hi, yingshaoxo</div>
            <div class="message_me">Hi, stranger.</div>
        </div>
        <div class="input_container _columns">
            <input class="the_input"></input>
            <button>Send</button>
        </div>
    </div>
</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.full_screen {
    width: 100vw;
    height: 100vh;
}

.history_message_list {
    width: 100%;

    .message_other {
        text-align: left;
    }

    .message_me {
        text-align: right;
    }
}

.input_container {
    height: 30px;
    width: 100%;
    justify-content: space-between;

    .the_input {
        width: 100%;
    }
}
</style>
