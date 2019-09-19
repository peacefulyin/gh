import request from './request';

// export function getUserInfo() {
//   return request('get', '/userinfo');
// }



// export function invite({ openid, code }) {
//   return request('post', '/invite', { openid, code });
// }
//
// export function getQuestion({ openid, type, order }) {
//   return request('post', '/question', { openid, type, order });
// }

// const apiRoot = 'http://225n26h324.51mypc.cn/'
// const apiLocalRoot = 'http://172.10.3.98:8001'
export const apiLocalRoot = 'http://172.10.3.98:8001'



export function playGame({ openid, type,token }) {
  return request('post', `${apiLocalRoot}/main/play`, { openid,type,token});
}

export function sendGameResult({ openid, token,score }) {
  return request('post', `${apiLocalRoot}/main/finish_game`, { openid,token,score});
}


export function getAccessToken(code) {
  return request('get', `${apiLocalRoot}/main/get_user_info?code=`+code);
}

export function getPrizes() {
  return request('post', `${apiLocalRoot}/main/get_prizes`);

}

export function startLottery({openid,token}) {
  return request('post', `${apiLocalRoot}/main/start_lottery`, { openid,token});
}

export function getUserPrizes({openid, token}) {
  return request('post', `${apiLocalRoot}/main/get_user_prizes`, { openid,token});

}
// export function getRankingList({ type }) {
//   return request('get', 'http://225n26h324.51mypc.cn/main/get_ranking?type='+type);
// }

export function getRankingList({openid,token,type }) {
  return request('post', `${apiLocalRoot}/main/get_ranking`,{ openid,token,type});
}

export function setInvitation({ openid,token,invitationCode}) {
  return request('post', `${apiLocalRoot}/main/invitation`,{ openid,token,invitationCode});
}

export function heartBeat({openid, token}) {
  return request('post', `${apiLocalRoot}/main/heart_beat`,{ openid,token});
}

export function wxShare({openid, token,type}) {
  return request('post', `${apiLocalRoot}/wechat/wx_share`,{ openid,token,type});
}




// export function getAccessToken() {
//   return request('get', 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxa0c3aa5fdd1d1a78&secret=a2210e72cefba5bc34b18850ab8024f3&code=011TtcQI0aymKe2zxkMI0ONfQI0TtcQ2&grant_type=authorization_code');
// }

