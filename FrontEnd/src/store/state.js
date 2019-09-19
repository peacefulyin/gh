const state = {
  openid: '',
  nickname: '',
  headImgUrl: '',
  invitationCode: '',
  gameNumber: [3, 3],
  practiceNumber: 3,
  prize: 0,
  score: 0,
  points: 0,
  token: null,
  rank: 0,
  mute: false,
  gameMode: '', // 三种模式，normal:普通模式，practice:练习模式，activity:活动模式，为空：未开始游戏
  previousGameMode: '',
  rankingList:{
    "week": [],
    "allTime": []
  },
  userPrizes: [],
  dataFetched: false,
  isInvited:false,
  notShowIntro: false
};

export default state;
