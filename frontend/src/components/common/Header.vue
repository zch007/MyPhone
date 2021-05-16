<template>
  <div class="header-box">
    <div class="header">
      <div class="content">

        <!--logo-->
        <div class="logo full-left">
          <router-link to="/"><img src="/static/image/logo1.png" alt="MyPhone" id="logo"></router-link>
        </div>

        <!--导航栏-->
        <ul class="nav full-left" v-for="(nav_top, i) in nav_top_list" :key="i">
          <li>
            <span v-if="nav_top.is_site"><a :href="nav_top.link">{{ nav_top.title }}</a></span>
            <span v-else><router-link :to="nav_top.link">{{ nav_top.title }}</router-link></span>
          </li>
        </ul>

        <!--购物车和个人信息-->
        <div class="login-bar full-right">
          <div class="shop-cart full-left">
            <router-link to="/cart">
              <img src="/static/image/cart.svg" alt="">
              <span v-if="token">购物车 {{ this.$store.state.cart_length }}</span>
              <span v-else><router-link to="/cart">购物车</router-link></span>
            </router-link>
          </div>

          <div class="login-box full-left" v-if="token">
            <span><router-link to="/index">您好，{{ user.username }}</router-link></span>
            &nbsp;|&nbsp;
            <span @click="exit">退出登陆</span>
          </div>
          <div class="login-box full-left" v-else>
            <span><router-link to="/login">登陆</router-link></span>
            &nbsp;|&nbsp;
            <span><router-link to="/register">注册</router-link></span>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",

  data() {
    return {
      nav_top_list: [],
      user: {"username": ""},
      token: sessionStorage["token"],
      // 购物车角标
    }
  },

  methods: {
    // 获取所有的顶部标签
    get_nav_tops() {
      this.$axios.get(this.$settings.HOST + "index/nav_top/").then(response => {
        this.nav_top_list = response.data
      }).catch(error => {
        console.log(error)
      })
    },

    // 退出登陆
    exit() {
      sessionStorage.removeItem("token")
      this.token = false
      // 跳转首页
      this.$router.push("/")
      this.get_cart()
    },

    // 获取购物车数字
    get_cart() {
      this.$axios({
        url: this.$settings.HOST + 'index/cart_show/',
        method: 'get',
        headers: {
          // 提交token时必须在请求头中声明token  jwt token
          "Authorization": "jwt " + this.token
        },
      }).then(res => {
        this.$store.commit("add_cart", res.data.cart_length)
      }).catch(error => {
        console.log(error)
      })
    },

    // 获取登陆用户信息
    get_user() {
      this.$axios({
        url: this.$settings.HOST + 'index/user/',
        method: 'get',
        headers: {
          "Authorization": "jwt " + this.token
        },
      }).then(res => {
        this.user = res.data
      }).catch(error => {
        console.log(error)
      })
    }
  },

  created() {
    this.get_nav_tops();
    this.get_cart();
    this.get_user();
  }
}
</script>

<style scoped>
.header-box {
  height: 110px;
}

.header {
  width: 100%;
  height: 110px;
  box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
  position: fixed;
  left: 0;
  right: 0;
  margin: auto;
  z-index: 99;
  background: #fff;
}

.header .content {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.header .content .logo {
  height: 110px;
  margin-right: 60px;
  cursor: pointer;
}

.header .content .logo img {
  width: 80px;
  height: 120px;
  object-fit: cover;
  vertical-align: middle;
}

.header .nav li {
  float: left;
  height: 80px;
  line-height: 100px;
  margin-right: 30px;
  font-size: 16px;
  color: #4a4a4a;
  cursor: pointer;
}

.header .nav li span {
  padding-bottom: 16px;
  padding-left: 5px;
  padding-right: 5px;
}

.header .nav li span a {
  display: inline-block;
}

.header .nav li .this {
  color: #4a4a4a;
  border-bottom: 4px solid #ffc210;
}

.header .nav li:hover span {
  color: #000;
}

.header .login-bar {
  height: 100px;
}

.header .login-bar .shop-cart {
  margin-right: 20px;
  border-radius: 17px;
  background: #f3efef;
  cursor: pointer;
  font-size: 14px;
  height: 38px;
  width: 100px;
  margin-top: 30px;
  line-height: 42px;
  text-align: center;
}

.header .login-bar .shop-cart:hover {
  background: #f0f0f0;
}

.header .login-bar .shop-cart img {
  width: 15px;
  margin-right: 4px;
  margin-left: 6px;
}

.header .login-bar .shop-cart span {
  margin-right: 6px;
}

.header .login-bar .login-box {
  margin-top: 33px;
}

.header .login-bar .login-box span {
  color: #4a4a4a;
  cursor: pointer;
}

.header .login-bar .login-box span:hover {
  color: #000000;
}

.login-box {
  line-height: 36px;
}

a {
  text-decoration: none;
  color: #333;
}

.member {
  display: inline-block;
  height: 34px;
  margin-left: 20px;
}

.member img {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-block;
}

.member img:hover {
  border: 1px solid yellow;
}

.header .login-bar .login-box1 {
  margin-top: 16px;
}

a:hover {
  display: inline-block;
}

#logo {
  width: 120px;
}
</style>
