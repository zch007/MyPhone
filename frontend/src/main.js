// 导包
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import "element-ui/lib/theme-chalk/index.css"
import axios from 'axios'
import settings from "./settings"
import "../static/css/global.css"
import "../static/js/gt"
import VideoPlayer from 'vue-video-player'
import store from "./store/index"

Vue.config.productionTip = false

// 注册
Vue.use(ElementUI)
Vue.use(VideoPlayer)

// vue-video的配置
require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');

// 注入实例
Vue.prototype.$axios = axios
Vue.prototype.$settings = settings

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>',
  store,
})
