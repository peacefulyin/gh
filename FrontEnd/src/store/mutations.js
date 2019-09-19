import * as types from './mutation-types';
import { setLocal, getLocal } from '../utils/cache';

const mutations = {
  [types.GET_CACHE](state) {
    state.mute = getLocal('mute') || false;
  },
  [types.SET_USER_INFO](state, userInfo) {
    state.openid = userInfo.openid;
    state.nickname = userInfo.nickname;
    state.headImgUrl = userInfo.headImgUrl;
    state.gameNumber = userInfo.gameNumber;
    state.practiceNumber = userInfo.practiceNumber;
    state.prize = userInfo.prize.toFixed(2);
    state.score = userInfo.score;
    state.points = userInfo.points;
    state.rank = userInfo.rank;
    state.invitationCode = userInfo.invitationCode;
    state.userPrizes = userInfo.userPrizes;
    state.isInvited = userInfo.isInvited;
  },
  [types.PLAY_GAME](state, type) {
    switch (type) {
      case 'normal':
        state.gameNumber[0] -= 1;
        state.gameMode = 'normal';
        break;
      case 'practice':
        state.practiceNumber -= 1;
        state.gameMode = 'practice';
        break;
      case 'activity':
        state.gameMode = 'activity';
        break;
      default:
    }
  },
  [types.END_GAME](state) {
    state.previousGameMode = state.gameMode;
    state.gameMode = '';
  },
  [types.INVITE](state) {
    state.gameNumber[0] += 1;
  },
  [types.SHARE](state) {
    state.gameNumber[0] += 1;
  },
  [types.SWITCH_MUSIC](state) {
    state.mute = !state.mute;
    setLocal('mute', state.mute);
  },
  [types.SET_TOKEN](state,token) {
    state.token = token;
  },
  [types.SET_POINTS](state,points) {
    state.points = points;
  },
  [types.SET_DATA_FETCH](state,dataFetched) {
    state.dataFetched = dataFetched;
  },
  [types.SET_INVITED](state,isInvited) {
    state.isInvited = isInvited;
  },
  [types.SET_POINTS_AND_SCORE](state,{points,score}) {
    state.points = points
    state.score = score

  },
  [types.SET_NOT_SHOW_INTRO](state,notShowIntro) {
    state.notShowIntro = notShowIntro

  },
  [types.SET_STATE](state,state_value) {
    state = Object.assign(state,...state_value);
  }
};

export default mutations;
