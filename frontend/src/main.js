import BootstrapVue from 'bootstrap-vue'; // Import Bootstrap here
import Vue from 'vue';
import App from './App.vue';
import router from './router';

Vue.use(BootstrapVue); // Use Bootstrap here
Vue.config.productionTip = false;
new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
