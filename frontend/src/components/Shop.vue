<template>
  <div class="shop">
    <Header></Header>
    <div class="main">

      <!--分类条件-->
      <div class="condition">

        <!--分类展示-->
        <ul class="cate-list">
          <li class="title">商品分类:</li>
          <li @click="category_id=0" :class="category_id===0 ? 'this' : ''">全部</li>
          <li v-for="category in category_list" @click="category_id=category.id"
              :class="category_id===category.id ? 'this' : ''">{{ category.name }}
          </li>
        </ul>

        <!--排序过滤-->
        <div class="ordering">
          <ul>
            <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选:</li>
            <li class="default " @click="change_order_type('id')" :class="change_order_class('id')">默认</li>
            <li class="hot " @click="change_order_type('user_num')" :class="change_order_class('user_num')">人气</li>
            <li class="price" @click="change_order_type('price')" :class="change_order_class('price')">价格</li>
          </ul>
          <p class="condition-result">共{{ phone_num }}个商品</p>
        </div>
      </div>

      <!-- 商品列表 -->
      <div class="shop-list">
        <div class="shop-item" v-for="phone in phone_list">
          <router-link :to="'/detail/'+ phone.id">

            <div class="shop-image">
              <img :src="phone.cover" alt="">
            </div>

            <div class="shop-info">

              <h3><b class="phone-name">{{ phone.name }}</b>
                <span><img src="/static/image/avatar1.svg" alt="">{{ phone.user_num }}人已购买</span>
              </h3>

              <i class="phone-brief">{{ phone.brief }}</i>

              <div class="evaluation-list"></div>

              <div class="pay-box">
                <span class="discount-type" v-if="phone.discount_name">{{ phone.discount_name }}</span>
                <span class="no-discount" v-else>无优惠</span>
                <span class="discount-price">￥{{ phone.real_price }}元</span>
                <span class="original-price">原价：{{ phone.price }}元</span>
                <span class="buy-now">立即购买</span>
              </div>

            </div>
          </router-link>
        </div>
      </div>

      <el-pagination backgrounds :page-size="filters.size" layout="prev, pager, next, sizes" :page-sizes="[5, 10]"
                     @size-change="size_change" @current-change="change_page" :total="phone_num" class="el-pagination">
      </el-pagination>

    </div>
    <Footer></Footer>
  </div>
</template>


<script>
import Header from "./common/Header";
import Footer from "./common/Footer";

export default {
  name: "Shop",

  data() {
    return {
      category_list: [],  // 分类列表
      category_id: 0,  // 分类id(默认0，表示显示全部)
      phone_list: [],  // 所有商品
      phone_num: 0,  // 商品数
      // 过滤器，对数据进行过滤
      filters: {
        type: "id", // 筛选的类型
        orders: "asc", // 排序类型 desc降序 asc升序
        size: 5,
        page: 1,
      }
    }
  },

  // 检测页面中分类id的值的变化  一旦变化  则根据当前点击的id获取对应的课程
  watch: {
    category_id() {
      // 重新按照当前点击的id发起请求（每次点击标签后都会发一个新的请求）
      this.get_all_phone()
    },
  },

  methods: {
    // 获取所有分类的方法
    get_all_category() {
      this.$axios.get(this.$settings.HOST + "shop/category/").then(response => {
        this.category_list = response.data;
      })
    },

    // 改变排序样式
    change_order_class(type) {
      // 更改选中的高亮效果
      if (this.filters.type === type && this.filters.orders === "asc") {
        return "this asc"
      } else if (this.filters.type === type && this.filters.orders === "desc") {
        return "this desc"
      } else {
        return ""
      }
    },

    // 改变排序类型
    change_order_type(type) {
      // 通过click事件改变点击的类型
      if (this.filters.type === type && this.filters.orders === "asc") {
        this.filters.orders = "desc"
      } else if (this.filters.type === type && this.filters.orders === "desc") {
        this.filters.orders = "asc"
      }
      // 更改排序方式
      this.filters.type = type;
      // 重新获取排序后结果
      this.get_all_phone();
    },

    // 获取手机列表
    get_all_phone() {
      let filters = {
        // 将每次切换后的页面传递过去
        page: this.filters.page,
        size: this.filters.size,
      }
      // 完成排序相关
      if (this.filters.orders === "desc") {
        filters.ordering = "-" + this.filters.type;
      } else {
        filters.ordering = this.filters.type;
      }
      // 判断是否要根据分类id查询课程
      if (this.category_id > 0) {
        filters.category = this.category_id;
      }
      this.$axios.get(this.$settings.HOST + "shop/list/", {
        params: filters
      }).then(res => {
        this.phone_list = res.data.results;
        this.phone_num = res.data.count;
      })
    },

    // 分页
    change_page(page) {
      this.filters.page = page;
      this.get_all_phone();
    },

    // 改变每页展示的手机数量
    size_change(size) {
      this.filters.size = size;
      // 改变每次分页展示的数量后，都展示更新后的第一页
      this.filters.page = 1;
      this.get_all_phone();
    },
  },

  created() {
    this.get_all_category()  // 自动获取分类
    this.get_all_phone()  // 自动获取商品
  },

  components: {
    Header: Header,
    Footer: Footer,
  }
}
</script>

<style scoped>
.shop {
  background: #f6f6f6;
}

.shop .main {
  width: 1100px;
  margin: 35px auto 0;
  min-height: calc(635px);
}

.shop .condition {
  margin-bottom: 35px;
  padding: 25px 30px 25px 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.shop .cate-list {
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, .05);
  padding-bottom: 18px;
  margin-bottom: 17px;
}

.shop .cate-list::after {
  content: "";
  display: block;
  clear: both;
}

.shop .cate-list li {
  float: left;
  font-size: 16px;
  padding: 6px 15px;
  line-height: 16px;
  margin-left: 14px;
  position: relative;
  transition: all .3s ease;
  cursor: pointer;
  color: #4a4a4a;
  border: 1px solid transparent; /* transparent 透明 */
}

.shop .cate-list .title {
  color: #888;
  margin-left: 0;
  letter-spacing: .36px;
  padding: 0;
  line-height: 28px;
}

.shop .cate-list .this {
  color: #ffc210;
  border: 1px solid #ffc210 !important;
  border-radius: 30px;
}

.shop .ordering::after {
  content: "";
  display: block;
  clear: both;
}

.shop .ordering ul {
  float: left;
}

.shop .ordering ul::after {
  content: "";
  display: block;
  clear: both;
}

.shop .ordering .condition-result {
  float: right;
  font-size: 14px;
  color: #9b9b9b;
  line-height: 28px;
}

.shop .ordering ul li {
  float: left;
  padding: 6px 15px;
  line-height: 16px;
  margin-left: 14px;
  position: relative;
  transition: all .3s ease;
  cursor: pointer;
  color: #4a4a4a;
}

.shop .ordering .title {
  font-size: 16px;
  color: #888;
  letter-spacing: .36px;
  margin-left: 0;
  padding: 0;
  line-height: 28px;
}

.shop .ordering .this {
  color: #ffc210;
}

.shop .ordering .price {
  position: relative;
}

.shop .ordering .price::before,
.shop .ordering .price::after {
  cursor: pointer;
  content: "";
  display: block;
  width: 0;
  height: 0;
  border: 5px solid transparent;
  position: absolute;
  right: 0;
}

.shop .ordering .price::before {
  border-bottom: 5px solid #aaa;
  margin-bottom: 2px;
  top: 2px;
}

.shop .ordering .price::after {
  border-top: 5px solid #aaa;
  bottom: 2px;
}

.shop .shop-item:hover {
  box-shadow: 4px 6px 16px rgba(0, 0, 0, .5);
}

.shop .shop-item {
  width: 1050px;
  background: #fff;
  padding: 20px 30px 20px 20px;
  margin-bottom: 35px;
  border-radius: 2px;
  cursor: pointer;
  box-shadow: 2px 3px 16px rgba(0, 0, 0, .1);
  /* css3.0 过渡动画 hover 事件操作 */
  transition: all .2s ease;
}

.shop .shop-item::after {
  content: "";
  display: block;
  clear: both;
}

.shop .shop-item .shop-image {
  float: left;
  width: 360px;
  height: 210px;
  margin-right: 30px;
}

.shop .shop-item .shop-image img {
  width: 100%;
}

.shop .shop-item .shop-info {
  float: left;
  width: 660px;
}

.shop-item .shop-info h3 {
  font-size: 26px;
  color: #333;
  font-weight: normal;
  margin-bottom: 8px;
}

.shop-item .shop-info h3 span {
  font-size: 13px;
  color: #9b9b9b;
  float: right;
  margin-top: 18px;
}

.shop-item .shop-info h3 span img {
  width: 10px;
  height: auto;
  margin-right: 3px;
  margin-top: 3px;
}

.shop-item .shop-info .author-info span {
  float: right;
}

.shop-item .phone-name {
  font-size: 18px;
}

.shop-item .phone-brief {
  color: #ffb300;
  font-size: 14px;
}

.shop-item .phone-user {
  font-size: 11px;
}

.shop-item .evaluation-list::after {
  content: "";
  display: block;
  clear: both;
  min-height: calc(80px);
}

.shop-item .evaluation-list li {
  float: left;
  width: 44%;
  font-size: 14px;
  color: #666;
  padding-left: 22px;
  /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
  background: url("/static/image/play-icon-gray.svg") no-repeat left 4px;
  margin-bottom: 15px;
}

.shop-item .evaluation-list li .evaluation-title {
  /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  display: inline-block;
  max-width: 200px;
}

.shop-item .evaluation-list li:hover {
  background-image: url("/static/image/play-icon-yellow.svg");
  color: #ffc210;
}

.shop-item .pay-box::after {
  content: "";
  display: block;
  clear: both;
}

.shop-item .pay-box .discount-type {
  padding: 6px 10px;
  font-size: 16px;
  color: #fff;
  text-align: center;
  margin-right: 8px;
  background: #fa6240;
  border: 1px solid #fa6240;
  border-radius: 10px 0 10px 0;
  float: left;
}

.shop-item .pay-box .no-discount {
  padding: 6px 10px;
  font-size: 16px;
  color: #fff;
  text-align: center;
  margin-right: 8px;
  background: #5a5858;
  border: 1px solid #5a5858;
  border-radius: 10px 0 10px 0;
  float: left;
}

.shop-item .pay-box .discount-price {
  font-size: 24px;
  color: #fa6240;
  float: left;
}

.shop-item .pay-box .original-price {
  text-decoration: line-through;
  font-size: 14px;
  color: #9b9b9b;
  margin-left: 10px;
  float: left;
  margin-top: 10px;
}

.shop-item .pay-box .buy-now {
  width: 120px;
  height: 38px;
  background: transparent;
  color: #fa6240;
  font-size: 16px;
  border: 1px solid #fd7b4d;
  border-radius: 3px;
  transition: all .2s ease-in-out;
  float: right;
  text-align: center;
  line-height: 38px;
}

.shop-item .pay-box .buy-now:hover {
  color: #fff;
  background: #ffc210;
  border: 1px solid #ffc210;
}

.el-pagination {
  background: #f6f6f6;
  text-align: center;
  padding-top: 20px;
  padding-bottom: 50px;
}
</style>
