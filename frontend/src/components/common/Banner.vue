<template>
  <div class="banner">

    <el-carousel height="670px" :interval="3000" arrow="always">
      <el-carousel-item v-for="(banner, i) in banner_list" :key="i">
        <a :href="banner.link"><img :src="banner.img" :alt="banner.title"></a>
      </el-carousel-item>
    </el-carousel>

  </div>
</template>

<script>
export default {
  name: "Banner",

  data() {
    return {
      banner_list: []
    }
  },

  methods: {
    // 获取轮播图数据
    get_banners() {
      this.$axios.get(this.$settings.HOST + "index/banner/").then(response => {
        this.banner_list = response.data
      })
    }
  },

  created() {
    this.get_banners()
  }
}
</script>

<style scoped>
.banner {
  width: 100%;
  min-height: calc(635px);
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}

img {
  width: 101%;
}
</style>
