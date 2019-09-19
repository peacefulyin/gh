<template>
  <PopupModal>
    <router-link to="/">
      <img class="close-btn" src="../../assets/icon/close.svg" alt="close">
    </router-link>
    <div class="prize-container">
      <img class="avatar" v-lazy="headImgUrl" alt="avatar">
      <p class="user-name">{{ nickname }}</p>
      <p class="text">剩余积分</p>
      <p class="money">{{ points }}</p>
      <h1 class="title">积分</h1>
      <ul class="rules">
        <li>在 <strong>抽奖页面</strong> 可使用积分进行抽奖</li>
        <li>每 <strong>10</strong> 积分可抽奖一次</li>
        <li>可通过 <strong>答题</strong> 获取更多积分</li>
      </ul>
    </div>
  </PopupModal>
</template>

<script>
import { mapState } from 'vuex';
import PopupModal from '../PopupModal';

export default {
  name: 'PrizePage',
  components: {
    PopupModal
  },
  computed: mapState([
    'nickname',
    'headImgUrl',
    'prize',
          'points'
  ])
};
</script>

<style lang="scss" scoped src="./style.scss"></style>
