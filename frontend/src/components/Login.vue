<template>
  <div class="login box">
    <!--<img src="../../static/image/background.png" alt="">-->
    <div class="login">

      <!--logo-->
      <div class="login-title">
        <img class="logo" src="../../static/image/logo2.png" alt="">
      </div>

      <div class="login_box">

        <div class="title">
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="密码登录" name="first"></el-tab-pane>
            <el-tab-pane label="短信登陆" name="second"></el-tab-pane>
          </el-tabs>
        </div>

        <!--账号密码登陆-->
        <div class="inp" v-if="is_code">
          <label><input type="text" placeholder="用户名 / 手机号码 / 邮箱" class="user" v-model="username"></label>
          <label><input type="password" name="" class="pwd" placeholder="密码" v-model="password"></label>
          <div id="geetest1"></div>
          <div class="rember">
            <p>
              <label><input type="checkbox" class="no" style="width: 12px" v-model="remember_me"/></label>
              <span>&nbsp;记住密码</span>
            </p>
            <p style="padding-right: 30px; font: normal 12px 'Microsoft YaHei'">忘记密码</p>
          </div>
          <button class="login_btn btn btn-primary" @click="code_login" :disabled="login_disabled">登录</button>
          <p class="go_login">没有账号
            <router-link to="/register">立即注册</router-link>
          </p>
        </div>

        <!--手机号登陆-->
        <div class="inp" v-else>
          <label><input type="text" placeholder="手机号码" class="user" v-model="phone" @blur="check_phone"></label>
          <label><input type="text" class="pwd" placeholder="短信验证码" style="width: 180px" v-model="code"></label>
          <el-button id="get_code" class="btn btn-primary" type="primary" style="height: 45px" :disabled="captcha_disabled" @click="get_code">
            获取验证码
          </el-button>
          <button class="login_btn" @click="message_login">登录</button>
          <div class="go_login">没有账号
            <router-link to="/register">立即注册</router-link>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",

  data() {
    return {
      // 标签页默认显示“密码登录”
      activeName: "first",
      // 默认显示“密码登录”框
      is_code: true,
      // 获取验证码默认不可用
      captcha_disabled: true,
      // 记住密码
      username: localStorage.username ? localStorage.username : "",
      password: localStorage.password ? localStorage.password : "",
      phone: "",
      code: "",
      // 记住密码
      remember_me: false,
      // 认证成功出现验证码框后禁用登陆按钮
      login_disabled: false,
      // 用于存储临时token，如果验证码认证成功后再将其存入session中
      token: ""
    }
  },
  methods: {
    // 标签切换
    handleClick(tab) {
      this.is_code = tab.name === "first";
    },

    // 密码登陆请求
    code_login() {
      this.$axios({
        url: this.$settings.HOST + "users/code_login/",
        method: "post",
        data: {
          username: this.username,
          password: this.password,
        }
      }).then(res => {
        // 用户名密码校验完成后将token存入临时缓存
        this.token = res.data.token
        if (res.data) {
          // 获取滑块验证码
          this.get_captcha()
          // 将登录按钮禁用
          this.login_disabled = true
        }
      }).catch(error => {
        this.$message.error("用户名或密码错误!")
      })
    },

    // 滑块验证码获取方法
    get_captcha() {
      // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
      this.$axios({
        url: this.$settings.HOST + "users/captcha/", // 加随机数防止缓存
        method: "get",
        params: {
          username: this.username,
        },
      }).then(res => {
        let data = JSON.parse(res.data);
        initGeetest({
          gt: data.gt,
          challenge: data.challenge,
          product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
          offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
          new_captcha: data.new_captcha
        }, this.handlerPopup);
      })
    },

    // 请求验证码的回调函数  完成验证码的验证
    handlerPopup(captchaObj) {
      // 回调函数中  this的指向会被改变
      let self = this;
      // 在验证码被用户成功滑动后开始执行
      captchaObj.onSuccess(function () {
        let validate = captchaObj.getValidate();
        self.$axios({
          url: self.$settings.HOST + "users/captcha/",
          method: "post",
          data: {
            geetest_challenge: validate.geetest_challenge,
            geetest_validate: validate.geetest_validate,
            geetest_seccode: validate.geetest_seccode
          },
        }).then(res => {
          self.$message({
            message: "恭喜你，登陆成功",
            type: "success",
            duration: 1000,
          })
          // 登陆时来判断用户是否需要记住密码 remember_me的值为True代表需要记住密码
          if (self.remember_me) {
            // 代表用户要记住密码
            localStorage.username = self.username;
            localStorage.password = self.password;
          } else {
            localStorage.removeItem("username")
            localStorage.removeItem("password")
          }
          // 将token信息保存
          sessionStorage.token = self.token;
          // 登陆成功后返回到首页
          self.$router.push("/")
        }).catch(error => {
          console.log(error);
        });
      });
      // 将验证码加到id为captcha的元素里
      captchaObj.appendTo("#geetest1");
    },

    // 检查短信登陆中手机号是否存在
    check_phone() {
      this.$axios({
        url: this.$settings.HOST + "users/login_mobile_check/",
        method: "get",
        params: {
          phone: this.phone,
        }
      }).then(res => {
        this.captcha_disabled = false
      }).catch(error => {
        this.$message.error(error.response.data)
        this.captcha_disabled = true
      })
    },

    // 根据手机号获取验证码
    get_code() {
      this.$axios({
        url: this.$settings.HOST + "users/send/",
        method: "get",
        params: {
          phone: this.phone
        }
      }).then(res => {
          this.$message.success(res.data)
      }).catch(error => {
        this.$message.error("您在60s内已经发送过一次验证码，请稍后再试～")
      })
    },

    // 短信登陆
    message_login() {
      this.$axios({
        url: this.$settings.HOST + "users/message_login/",
        method: "post",
        data: {
          phone: this.phone,
          code: this.code,
        }
      }).then(res => {
        if (res.data.token) {
          // 保存用户登陆状态
          sessionStorage.token = res.data.token
          this.$message.success("登陆成功，即将跳转到首页")
          // 跳转到首页
          this.$router.push("/");
        }
      }).catch(error => {
        this.$message.error("验证码不正确")
      })
    },
  },
}
</script>

<style scoped>
.box {
  width: 100%;
  height: 1008px;
  position: relative;
  overflow: hidden;
}

.box img {
  width: 100%;
  min-height: 100%;
}

.box .login {
  position: absolute;
  width: 500px;
  height: 500px;
  top: -480px;
  left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
}

.login .login-title {
  width: 100%;
  height: 277px;
  text-align: center;
}

.login-title img {
  width: 190px;
  height: auto;
}

.login-title p {
  font-size: 18px;
  color: #fff;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.login_box {
  width: 370px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.login_box .title {
  font-size: 20px;
  color: #9b9b9b;
  letter-spacing: .32px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 50px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}

.login_box .title span:nth-of-type(1) {
  color: #4a4a4a;
  border-bottom: 2px solid #84cc39;
}

.logo {
  height: 60px;
  width: 100px;
  object-fit: cover;
}

.inp {
  width: 350px;
  margin: 0 auto;
}

.inp input {
  margin-left: 25px;
  outline: 0;
  width: 85%;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}

#geetest1 {
  margin-left: 25px;
  margin-top: 15px;
}

.inp input.user {
  margin-bottom: 16px;
}

.inp .rember {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-top: 10px;
}

.inp .rember p:first-of-type {
  font-size: 12px;
  color: #4a4a4a;
  letter-spacing: .19px;
  margin-left: 22px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  position: relative;
}

.inp .rember p:nth-of-type(2) {
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
  cursor: pointer;
}

.inp .rember input {
  outline: 0;
  width: 30px;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}

.inp .rember p span {
  display: inline-block;
  font-size: 12px;
  width: 100px;

}

.login_btn {
  width: 85%;
  margin-left: 25px;
  height: 45px;
  background: #84cc39;
  border-radius: 5px;
  font-size: 16px;
  color: #fff;
  letter-spacing: .26px;
  margin-top: 10px;
}

.inp .go_login {
  text-align: center;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .26px;
  padding-top: 20px;
}

.inp .go_login span {
  color: #84cc39;
  cursor: pointer;
}
</style>
