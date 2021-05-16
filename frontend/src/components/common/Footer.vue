<template>
  <div class="footer">

    <!--导航栏-->
    <ul>
      <li v-for="(nav_bottom, i) in nav_bottom_list" :key="i">
        <span v-if="nav_bottom.is_site"><a :href="nav_bottom.link">{{ nav_bottom.title }}</a></span>
        <span v-else><router-link :to="nav_bottom.link">{{ nav_bottom.title }}</router-link></span>
      </li>
    </ul>

    <div id="detail">
      <b>©zch zzzch007@126.com 版权所有</b><br>
      <i>本网站正在建设中，给您带来的不变敬请谅解！</i>
    </div>
  </div>
</template>

<script>
export default {
  name: "Footer",

  data() {
    return {
      nav_bottom_list: []
    }
  },

  methods: {
    // 获取所有的底部标签
    get_nav_bottoms() {
      this.$axios.get(this.$settings.HOST + "index/nav_bottom/").then(response => {
        this.nav_bottom_list = response.data
      })
    }
  },

  created() {
    this.get_nav_bottoms()
  }
}
</script>

<style scoped>
.footer {
  width: 100%;
  height: 228px;
  background: #25292e;
  color: #fff;
}

.footer ul {
  margin: 0 auto 16px;
  padding-top: 38px;
  width: 810px;
}

.footer ul li {
  float: left;
  width: 112px;
  margin: 0 10px;
  text-align: center;
  font-size: 14px;
}

.footer ul::after {
  content: "";
  display: block;
  clear: both;
}

.footer p {
  text-align: center;
  font-size: 12px;
}

a {
  font: normal 14px "Arial Black";
  color: #f1e6e6;
}

#detail {
  margin-top: 40px;
  font-size: 11px;
  color: #7B7B7B;
  text-align: center;
  line-height: 20px;
}
</style>
