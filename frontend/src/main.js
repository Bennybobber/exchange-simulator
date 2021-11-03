/* eslint-disable import/prefer-default-export */
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import JQuery from 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

import VeeValidate from 'vee-validate';
import Vue from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
  faHome,
  faUser,
  faUserPlus,
  faSignInAlt,
  faSignOutAlt,
  faBars,
} from '@fortawesome/free-solid-svg-icons';
import App from './App.vue';
import store from './store';
import setupInterceptors from './services/api-interceptors';
import router from './router';

window.$ = JQuery;
library.add(faHome, faUser, faUserPlus, faSignInAlt, faSignOutAlt);

Vue.config.productionTip = false;
Vue.use(VeeValidate);
Vue.component('font-awesome-icon', FontAwesomeIcon);
library.add(faBars);

setupInterceptors(store);

Vue.use(BootstrapVue); // Adding the use of bootstrap to vue
Vue.use(IconsPlugin); // Allows the use of Icons from bootstrap
Vue.config.productionTip = false;
new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
