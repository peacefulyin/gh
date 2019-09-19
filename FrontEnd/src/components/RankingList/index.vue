<template>
  <transition name="slide-fade">
    <div class="list-container">
      <header class="header">
        <router-link to="/">
          <img class="close-icon" src="../../assets/icon/close-white.svg" alt="close">
        </router-link>
        <h1 class="heading">排行榜</h1>
      </header>
      <div class="content">
        <nav>
<!--          <button-->
<!--            :class="{ active: rankingType === 1 }"-->
<!--            @click="rankingType = 1"-->
<!--          >-->
<!--            本周</button>-->
<!--          <button-->
<!--            :class="{ active: rankingType === 2 }"-->
<!--            @click="rankingType = 2"-->
<!--          >-->
<!--            总榜-->
<!--          </button>-->
        </nav>
        <div class="top-list">
          <div
            class="top-list-box"
            v-for="(item, index) in rankingList"
            v-if="index <= 2"
            :key="item.userId"
          >
            <img class="avatar" v-lazy="item.headimgurl" alt="avatar">
            <p class="user-name">{{ item.nickname }}</p>
            <p class="score">{{ item.score }}分</p>
          </div>


        </div>
        <div class="list">
          <div
            class="list-box"
            v-for="(item, index) in rankingList"
            v-if="index > 2"
            :key="item.userId"
            :class="{ active: index +1 === self_rank }"
          >
            <span class="rank">{{ index + 1 }}</span>
            <img class="avatar" v-lazy="item.headimgurl" alt="avatar">
            <div class="user-name">{{ item.nickname }}</div>
            <div class="score">{{ item.score }}分</div>
          </div>
        </div>
        <div class="self list">
          <div class="list-box">
            <span class="rank">{{ self_rank }}</span>
            <img class="avatar" v-lazy="headImgUrl" alt="avatar">
            <div class="user-name">{{ nickname }}</div>
            <div class="score">{{ score }}分</div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { mapState } from 'vuex';
import { getRankingList } from '../../api';

export default {
  name: 'RankingList',
  data() {
    return {
      rankingType: 2, // 排行榜类别，2为总榜，1为周榜
      rankingList: [],
      self_rank: 0
    };
  },
  computed: mapState([
    'nickname',
    'headImgUrl',
    'score',
    'openid',
    'token',
  ]),
  // watch: {
  //   rankingType(newType) {
  //     getRankingList({ type: newType })
  //       .then(({ data }) => {
  //         this.rankingList = data.rankingList;
  //       });
  //   }
  // },
  created() {
    getRankingList({type: this.rankingType,openid:this.openid,token:this.token})
      .then(({ data }) => {
        this.rankingList = JSON.parse(data.data.ranking_list);
        const index = this.rankingList.findIndex(item => item.openid === this.openid)
        this.self_rank = index+1
      });
  }
};
</script>

<style lang="scss" scoped src="./style.scss"></style>
