import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import JQuery from 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import Vue from 'vue';
import App from './App.vue';
import router from './router';

window.$ = JQuery;

library.add(faBars);

Vue.use(BootstrapVue); // Adding the use of bootstrap to vue
Vue.use(IconsPlugin); // Allows the use of Icons from bootstrap
Vue.config.productionTip = false;
new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
