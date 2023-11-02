import Vue from 'vue'
import App from './App.vue'

import './assets/css/css_for_human.less';

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
