<template>
  <div class="cart_item">

    <div class="cart_column column_1">
      <el-checkbox class="my_el_checkbox" v-model="phone.selected"></el-checkbox>
    </div>

    <div class="cart_column column_2">
      <p>
        <img :src="phone.cover" alt="">
        <span><router-link :to="'/detail/' + phone.id">{{ phone.name }}</router-link></span>
      </p>
    </div>

    <div class="cart_column column_3">¥{{ phone.price }}</div>

    <div class="cart_column column_4"><a href="javascript:void(0);" @click="del_phone">删除</a></div>

  </div>
</template>


<script>
export default {
  name: "CartItem",

  props: ['phone'],

  methods: {
    // 选中状态的切换
    change_selected() {
      this.$axios({
        url: this.$settings.HOST + "cart/option/",
        method: "put",
        data: {
          phone_id: this.$props.phone.id,
        },
        headers: {
          // 提交token时必须在请求头中声明token  jwt token
          "Authorization": "jwt " + sessionStorage.token
        },
      }).then(res => {
        // 更新父组件中的各种信息
        this.dad_show()
      })
    },

    // 删除商品
    del_phone() {
      this.$axios({
        url: this.$settings.HOST + "cart/option/",
        method: "delete",
        data: {
          phone_id: this.$props.phone.id,
        },
        headers: {
          // 提交token时必须在请求头中声明token  jwt token
          "Authorization": "jwt " + sessionStorage.token
        },
      }).then(res => {
        this.$message.success("删除成功")
        // 每次添加成功后向状态机提交修改购物车数量的行为
        this.$store.state.cart_length--;
        // 更新父组件中的各种信息
        this.dad_show()
      })
    },

    // 父组件实时显示
    dad_show() {
      this.$emit("ds_show")
    },
  },

  watch: {
    // 监测select的选中
    "phone.selected":
      function () {
        this.change_selected();
      },
  }
}
</script>

<style scoped>
.cart_item::after {
  content: "";
  display: block;
  clear: both;
}

.cart_column {
  float: left;
  height: 250px;
}

.cart_item .column_1 {
  width: 88px;
  position: relative;
}

.my_el_checkbox {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  margin: auto;
  width: 16px;
  height: 16px;
}

.cart_item .column_2 {
  padding: 67px 10px;
  width: 700px;
  height: 116px;
}

.cart_item .column_2 img {
  float: left;
  width: 175px;
  height: 115px;
  vertical-align: middle;
}

.cart_item .column_2 span {
  width: 450px;
  display: inline-block;
  float: left;
  margin-top: -75px;
  margin-left: 175px;
}

.cart_item .column_3 {
  padding: 67px 10px;
  height: 116px;
  width: 142px;
  line-height: 116px;
}

.my_el_select {
  width: 117px;
  height: 28px;
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
}

.cart_item .column_4 {
  padding: 67px 28px;
  height: 116px;
  width: 142px;
  line-height: 116px;
}

</style>

