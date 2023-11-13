<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { reactive, onMounted } from 'vue';

@Component({
    setup() {
        const dict = reactive({
        });

        const functions = reactive({
        })

        onMounted(() => {
        });

        return {
            dict,
            functions,
        };
    },
})

export default class Pop_Up_Page extends Vue {
    @Prop({ default: false })
    display!: boolean;

    @Prop({ default: '999' })
    z_index!: string;
}
</script>

<template>
    <div class="full_screen" v-if="display" :style="{ zIndex: z_index }">
        <slot></slot>
    </div>
</template>

<style scoped lang="less">
.full_screen {
    /*
    z-index: 999;
    */
    position: fixed;
    /*
    background-color: rgba(0,0,0,0.6);
    */

    width: 100vw;
    min-height: 100vh;

    display: flex;
    flex-direction: row;

    justify-content: center;
    align-items: center;
    text-align: center;
}
</style>
