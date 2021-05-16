<template>
  <div class="detail">
    <Header/>
    <div class="main">
      <div class="phone-info">

        <!-- 视频播放组件 -->
        <div class="wrap-left">
          <videoPlayer class="video-player vjs-custom-skin" ref="videoPlayer" :playsinline="true"
                       :options="playerOptions">
          </videoPlayer>
        </div>

        <div class="wrap-right">
          <h3 class="phone-name">{{ phone.name }}</h3>
          <p class="data">{{ phone.user_num }}人已购买&nbsp;&nbsp;&nbsp;&nbsp;</p>

          <div class="sale-time">
            <b class="sale-type" v-if="phone.discount_name"><i>{{ phone.discount_name }}</i></b>
            <b class="sale-type" v-else><i>无优惠</i></b>
            <p class="expire">距离结束：仅剩
              {{ parseInt(phone.active_time / (24 * 3600)) }}天
              {{ parseInt(phone.active_time / 3600 % 24) }}小时
              {{ parseInt(phone.active_time / 60 % 60) }}分
              <span class="second">
                {{ parseInt(phone.active_time % 60) }}
              </span> 秒
            </p>
          </div>

          <br>
          <p class="data">{{ phone.brief }}</p>
          <p class="phone-price">
            <span>活动价</span>
            <span class="discount">¥{{ phone.real_price }}</span>
            <span class="original">¥{{ phone.price }}</span>
          </p>
          <div class="buy">
            <div class="buy-btn">
              <button class="buy-now">立即购买</button>
              <button class="installment">分期付款</button>
            </div>
            <div class="add-cart" @click="add_cart"><img src="/static/image/cart.svg" alt="">加入购物车</div>
          </div>
        </div>
      </div>

      <div class="phone-tab">
        <ul class="tab-list">
          <li :class="tabIndex===1 ? 'active' : ''" @click="tabIndex=1">详情介绍</li>
          <li :class="tabIndex===2 ? 'active' : ''" @click="tabIndex=2">详细测评</li>
          <li :class="tabIndex===3 ? 'active' : ''" @click="tabIndex=3">用户评论</li>
          <li :class="tabIndex===4 ? 'active' : ''" @click="tabIndex=4">常见问题</li>
        </ul>
      </div>

      <div class="phone-content">
        <div class="phone-tab-list">

          <div class="tab-item" v-if="tabIndex===1">
            <div class="tab-item-title">
              <p class="chapter">商品详情</p>
            </div>
            <div v-html="phone.content"></div>
          </div>

          <div class="tab-item" v-if="tabIndex===2">
            <div class="tab-item-title">
              <p class="chapter">评测</p>
              <p class="chapter-length">共{{ evaluation_num }}个</p>
            </div>
            <div class="chapter-item" v-if="evaluation" v-for="(evaluation_item,i) in evaluation" :key="i">
              <a :href="evaluation_item.content">
                <p class="chapter-title">
                  <img src="/static/image/avatar1.svg" alt="">
                  {{ i + 1 }}. {{ evaluation_item.title }} ————<b><i>「{{ evaluation_item.author }}」</i></b>
                </p>
              </a>
              <p class="chapter-summary">{{ evaluation_item.summary }}</p>
              <br>
            </div>
            <div class="chapter-item" v-else>
              <p class="chapter-summary">&nbsp;&nbsp;暂无评测</p>
            </div>
          </div>

          <div class="tab-item" v-if="tabIndex===3">
            <div class="tab-item-title">
              <p class="chapter">评论</p>
              <p class="chapter-length">共0个</p>
            </div>
            <div class="chapter-item">
              <p class="chapter-summary">&nbsp;&nbsp;正在建设中～</p>
            </div>
          </div>

          <div class="tab-item" v-if="tabIndex===4">
            <div class="tab-item-title">
              <p class="chapter">常见问题</p>
              <p class="chapter-length">共0个</p>
            </div>
            <div class="chapter-item">
              <p class="chapter-summary">&nbsp;&nbsp;正在建设中～</p>
            </div>
          </div>

        </div>
      </div>

    </div>
    <Footer/>
  </div>
</template>

<script>
import {videoPlayer} from 'vue-video-player'
import Header from "./common/Header";
import Footer from "./common/Footer";

export default {
  name: "phoneDetail",

  data() {
    return {
      tabIndex: 1, // 分类默认展示详情
      phone_id: 0, // 商品id
      evaluation_num: 0,
      phone: {},
      evaluation: [],
      // 视频播放的配置
      playerOptions: {
        playbackRates: [0.5, 1.0, 1.5, 2.0], // 播放速度
        autoplay: false, //如果true,则自动播放
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 循环播放
        preload: 'auto',  // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: 'zh-CN',
        aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        // 播放资源和资源格式
        sources: [{
          type: "video/mp4",
          //你的视频地址（必填）
          src: "https://cdn.theguardian.tv/webM/2015/07/20/150716YesMen_synd_768k_vp8.webm"
        }],
        poster: "", //视频封面图
        width: document.documentElement.clientWidth, // 默认视频全屏时的最大宽度
        notSupportedMessage: '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
      },
    }
  },

  methods: {
    // 检查用户是否登录
    check_user_login() {
      let token = sessionStorage.token;
      if (!token) {
        let self = this;
        this.$confirm("对不起,请登录后再添加购物车", {
          callback() {
            self.$router.push("/login");
          }
        });
        return false
      }
      return token;
    },

    // 获取上一页传递的课程id
    get_phone_id() {
      let phone_id = this.$route.params.id;
      if (phone_id > 0) {
        this.phone_id = phone_id;
      }
    },

    // 获取当前课程的详细信息
    get_phone_detail() {
      this.$axios({
        url: this.$settings.HOST + "shop/detail/" + this.phone_id + "/",
        method: "get",
      }).then(res => {
        this.phone = res.data;
        // 播放视频
        // this.playerOptions.sources[0].src = res.data.video;
        this.playerOptions.poster = res.data.cover;
        this.evaluation = res.data.evaluation;
        this.evaluation_num = res.data.evaluation.length;
        // 活动倒计时
        if (this.phone.active_time > 0) {
          let timer = setInterval(() => {
            if (this.phone.active_time > 1) {
              this.phone.active_time -= 1
            } else {
              clearInterval(timer)
            }
          }, 1000)
        }
      })
    },

    // 添加商品至购物车
    add_cart() {
      // 添加购物车之前必须确保用户已登录
      let token = this.check_user_login();
      this.$axios({
        url: this.$settings.HOST + "cart/option/",
        method: "post",
        data: {
          phone_id: this.phone_id,
        },
        headers: {
          // 提交token时必须在请求头中声明token  jwt token
          "Authorization": "jwt " + token
        },
      }).then(res => {
        this.$message.success(res.data.message)
        // 每次添加成功后向状态机提交修改购物车数量的行为
        this.$store.commit("add_cart", res.data.cart_length);
      }).catch(error => {
        this.$message.error(error.response)
      })
    },
  },

  created() {
    this.get_phone_id()
    this.get_phone_detail()
  },

  components: {
    Header,
    Footer,
    videoPlayer,
  }
}
</script>

<style scoped>
.main {
  background: #fff;
  padding-top: 30px;
}

.phone-info {
  width: 1200px;
  margin: 0 auto;
  overflow: hidden;
}

.wrap-left {
  float: left;
  width: 690px;
  height: 388px;
  background-color: #000;
}

.wrap-right {
  float: left;
  position: relative;
  height: 388px;
}

.phone-name {
  font-size: 18px;
  color: #333;
  padding: 10px 23px;
  width: 464px;
  /*letter-spacing: .45px;*/
}

.data {
  width: 450px;
  padding-left: 23px;
  padding-right: 23px;
  padding-bottom: 16px;
  font-size: 14px;
  color: #9b9b9b;
}

.sale-time {
  width: 464px;
  background: #84cc39;
  font-size: 14px;
  color: #4a4a4a;
  padding: 10px 23px;
  overflow: hidden;
}

.sale-type {
  font-size: 16px;
  color: #fff;
  letter-spacing: .36px;
  float: left;
  line-height: 30px;
}

.sale-time .expire {
  font-size: 14px;
  color: #fff;
  float: right;
}

.sale-time .expire .second {
  width: 24px;
  display: inline-block;
  background: #fafafa;
  color: #5e5e5e;
  padding: 6px 0;
  text-align: center;
}

.phone-price {
  background: #fff;
  font-size: 14px;
  color: #4a4a4a;
  padding: 5px 23px;
}

.discount {
  font-size: 26px;
  color: #fa6240;
  margin-left: 10px;
  display: inline-block;
  margin-bottom: -5px;
}

.original {
  font-size: 14px;
  color: #9b9b9b;
  margin-left: 10px;
  text-decoration: line-through;
}

.buy {
  width: 464px;
  padding: 0 23px;
  position: absolute;
  left: 0;
  bottom: 20px;
  overflow: hidden;
}

.buy .buy-btn {
  float: left;
}

.buy .buy-now {
  width: 125px;
  height: 40px;
  border: 0;
  background: #ffc210;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  margin-right: 15px;
  outline: none;
}

.buy .installment {
  width: 125px;
  height: 40px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 15px;
  background: #fff;
  color: #ffc210;
  border: 1px solid #ffc210;
}

.add-cart {
  width: 125px;
  height: 38px;
  border-radius: 4px;
  float: right;
  font-size: 13px;
  border: 1px solid #969595;
  color: #969595;
  text-align: center;
  cursor: pointer;
  line-height: 38px;
}

.add-cart img {
  width: 20px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.phone-tab {
  width: 100%;
  background: #fff;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px 0 #f0f0f0;

}

.phone-tab .tab-list {
  width: 1200px;
  margin: auto;
  color: #4a4a4a;
  overflow: hidden;
}

.tab-list li {
  float: left;
  margin-right: 15px;
  padding: 26px 20px 16px;
  font-size: 17px;
  cursor: pointer;
}

.tab-list .active {
  color: #ffc210;
  border-bottom: 2px solid #ffc210;
}

.tab-list .installment {
  color: #fb7c55;
}

.phone-content {
  width: 1240px;
  margin: 0 auto;
  overflow: hidden;
  padding-bottom: 40px;
}

.phone-tab-list {
  width: 1240px;
  height: auto;
  padding: 20px;
  background: #fff;
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
}

.tab-item {
  width: 1200px;
  background: #fff;
  padding-bottom: 20px;
  box-shadow: 1px 2px 3px 4px #f0f0f0;
}

.tab-item-title {
  justify-content: space-between;
  padding: 25px 20px 11px;
  border-radius: 4px;
  margin-bottom: 20px;
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, .05);
  overflow: hidden;
}

.chapter {
  font-size: 17px;
  color: #4a4a4a;
  float: left;
}

.chapter-length {
  float: right;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
}

.chapter-title {
  font-size: 16px;
  color: #cb5252;
  letter-spacing: .26px;
  padding: 12px 25px;
  border-radius: 2px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}

.chapter-summary {
  font-size: 13px;
  color: #838181;
  letter-spacing: .26px;
  padding: 5px 30px;
  border-radius: 2px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}

.chapter-title img {
  width: 18px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.lesson-item .time img {
  width: 18px;
  height: 18px;
  margin-left: 15px;
  vertical-align: text-bottom;
}

.side-title span {
  display: inline-block;
  border-left: 2px solid #ffc210;
  padding-left: 12px;
}

.category-content .cont1 img {
  width: 54px;
  height: 54px;
  margin-right: 12px;
  float: left;
}
</style>
