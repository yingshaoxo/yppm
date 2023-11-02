import { reactive } from 'vue';

export const global_dict = reactive({
    hi: "yingshaoxo",
});

export const global_functions = reactive({
    hi: ()=>{
        console.log("hi, yingshaoxo")
    }
});
