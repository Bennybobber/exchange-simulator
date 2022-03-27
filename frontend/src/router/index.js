import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Trade from '../views/Trade.vue';
import Learn from '../views/Learn.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'SimEx Home',

    },
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/register',
    component: Register,
  },
  {
    path: '/trade/:coin/:name',
    component: Trade,
  },
  {
    path: '/portfolio',
    name: 'portfolio',
    // lazy-loaded
    component: () => import('../views/Portfolio.vue'),
  },
  {
    path: '/learn',
    component: Learn,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
