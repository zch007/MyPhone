import Vue from 'vue'
import Router from 'vue-router'
import Index from "../components/Index";
import Login from "../components/Login";
import Register from "../components/Register";
import Shop from "../components/Shop";
import Detail from "../components/Detail";
import Cart from "../components/Cart";
import Order from "../components/Order";

Vue.use(Router)

export default new Router({
  routes: [
    {path: '/index', component: Index},
    {path: '/login', component: Login},
    {path: '/register', component: Register},
    {path: '/shop', component: Shop},
    {path: '/detail/:id', component: Detail},
    {path: '/cart', component: Cart},
    {path: '/order', component: Order},
    {path: '/*', redirect: '/index'},
  ]
})
