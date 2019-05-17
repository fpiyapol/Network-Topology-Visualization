import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue';
import Topology from './views/Topology.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/topology',
      component: Topology
    }
  ]
})
