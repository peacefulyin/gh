<template>
  <transition name="slide-fade">
    <div class="rules-container">
      <header class="header">
        <router-link to="/">
          <img class="close-icon" src="../../assets/icon/close.svg" alt="close">
        </router-link>
        <h1 class="heading">游戏规则</h1>
      </header>
      <div class="content">
        <div class="title">
          <img src="../../assets/icon/tips.svg" alt="tips">
<!--          <h2>玩法介绍</h2>-->
        </div>
        <p class="details" style="">
          每个人每天有 <span>3</span> 次游戏机会，使用完后可以通过 <span id="inviteText">邀请好友</span> 的方式来增加游戏机会。<br>
          每局游戏 <span>10</span> 道题，答对 <span>7</span> 道及以上可获得 <span>10</span> 积分。 <br>
          每 <span>10</span> 积分可以抽奖一次，抽奖可以获得积分或者奖品。<br>
          实物奖品通过联系微信客服来领取。
        </p>
<!--        <div class="title">-->
<!--          <img src="../../assets/icon/question.svg" alt="question">-->
<!--          <h2>常见问题</h2>-->
<!--        </div>-->
<!--        <p class="details">-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--          这里是内容<br>-->
<!--        </p>-->
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'RulesPage'
};
</script>

<style lang="scss" scoped src="./style.scss"></style>
