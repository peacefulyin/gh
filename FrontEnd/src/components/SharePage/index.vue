<template>
  <PopupModal>
    <router-link to="/">
      <img class="close-btn" src="../../assets/icon/close.svg" alt="close">
    </router-link>
    <p class="invitation-code">{{ invitationCode }}</p>
    <h1 class="title">邀请好友填写邀请码，获得游戏机会</h1>
    <ul class="rules">
      <li>填写好友邀请码或者向好友分享你的邀请码</li>
      <li>好友填写你的邀请码参与答题后，双方均获得一次游戏机会</li>
      <li>每人每天邀请的人数没有限制</li>
      <li>分享给朋友可获得一次游戏机会，每天最多分享 5 次</li>
      <li>分享到朋友圈可获得一次游戏机会，每天最多分享 1 次</li>


    </ul>
    <div class="share-btns" @click="showShareTip">
      <div class="icon">
        <img src="../../assets/icon/wechat.svg" alt="wechat">
      </div>
      <div class="icon" @click="showShareTip">
        <img src="../../assets/icon/friendster.svg" alt="friendster">
      </div>
    </div>
  </PopupModal>
</template>

<script>
import { mapState } from 'vuex';
import PopupModal from '../PopupModal';
import wxapi from "../../common/wxapi";
import shareImg from '../../assets/garbage/harmful_garbage_04.png'

export default {
  name: 'SharePage',
  components: {
    PopupModal
  },
  methods: {
    wxRegCallback () {
      // 用于微信JS-SDK回调
      this.wxShareTimeline()
      this.wxShareAppMessage()
    },
    wxShareTimeline () {
      // 微信自定义分享到朋友圈
      let option = {
        title: '限时团购周 挑战最低价', // 分享标题, 请自行替换
        link: window.location.href.split('#')[0], // 分享链接，根据自身项目决定是否需要split
        imgUrl: shareImg, // 分享图标, 请自行替换，需要绝对路径
        success: () => {
          alert('分享成功')
        },
        error: () => {
          alert('已取消分享')
        }
      }
      console.log('option',option);
      // 将配置注入通用方法
      wxapi.ShareTimeline(option)
    },
    wxShareAppMessage () {
      console.log("clicked");
      // 微信自定义分享给朋友
      let option = {
        title: '限时团购周 挑战最低价', // 分享标题, 请自行替换
        desc: '限时团购周 挑战最低价', // 分享描述, 请自行替换
        link: window.location.href.split('#')[0], // 分享链接，根据自身项目决定是否需要split
        imgUrl: shareImg, // 分享图标, 请自行替换，需要绝对路径
        success: () => {
          console.log("???")
          alert('分享成功')
        },
        error: () => {
          alert('已取消分享')
        }
      }
      // 将配置注入通用方法
      wxapi.ShareAppMessage(option)
    },
    showShareTip() {
      this.$emit('showPromptBox', '请点击页面右上角按钮进行分享。');
    }
  },
  mounted() {
    // wxapi.wxRegister(()=>{
    //   this.wxShareAppMessage();
    //   this.wxShareTimeline();
    // })
  },
  computed: mapState([
    'invitationCode'
  ])
};
</script>

<style lang="scss" scoped src="./style.scss"></style>
