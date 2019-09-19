<template>
    <div>

        <PreloadImage
                :imgArr="imgArr"
        />
        <PromptBox v-show="showPrompt" :promptMessage="promptMessage"/>
        <main class="main" :class="{ blur: whetherBlur}">
            <div class="mask"></div>
            <img
                    @click="switchBackgroundMusic"
                    class="music"
                    :src="musicIconSrc"
                    alt="music"
            />
            <router-link to="/invitation">
                <button class="invite-code head-btn">填写邀请码</button>
            </router-link>
            <router-link to="/rank">
                <button class="rank-list head-btn">排行榜&nbsp;<Icon class="icon" name="angle-right"/>
                </button>
            </router-link>


            <!--中间的信息栏-->
            <section class="info-panel">
                <img class="avatar" v-lazy="headImgUrl" alt="头像">
                <div class="text-info">
                    <div>
                        <p class="title">剩余游戏次数</p>
                        <router-link to="/share">
                            <p class="content">
                                {{ gameNumber[0] }}/{{ gameNumber[1] }}&nbsp;
                                <Icon class="icon" name="angle-right"/>
                            </p>
                        </router-link>
                    </div>
                    <div></div>
                    <div>
                        <p class="title">我的积分/总得分</p>
                        <router-link to="prize">
                            <p class="content">
                                {{ points }} / {{score}}&nbsp;
                                <Icon class="icon" name="angle-right"/>
                            </p>
                        </router-link>
                    </div>
                </div>
                <!--三个按钮-->
                <!--                <BeginButton-->
                <!--                        class="practice-btn"-->
                <!--                        @click.native="play('practice')"-->
                <!--                >-->
                <!--                    <span class="text">练习模式 (每天三次机会)</span>-->
                <!--                </BeginButton>-->
                <BeginButton
                        class="normal-btn"
                        @click.native="play('normal')"
                >
                    <img class="begin" src="../../assets/icon/begin.svg" alt="begin">
                    <span class="text">开始答题</span>
                </BeginButton>
                <router-link to="/lottery" >
                    <BeginButton
                            class="activity-btn"
                            :propsStyle="{ backgroundColor: '#198cf9' }"
                    >
                    <span class="activity-intro"><span class="text">前往抽奖</span></span>
                    </BeginButton>
                </router-link>
                <!--活动预告-->
                <!--                <div class="trailer">-->
                <!--                    <div class="title">限时答题活动预告</div>-->
                <!--                    <div class="content">-->
                <!--                        <p>{{ trailerTime }}</p>-->
                <!--                        <div></div>-->
                <!--                        <p>&yen;&nbsp;{{ trailerPrize }}&nbsp;奖金</p>-->
                <!--                    </div>-->
                <!--                </div>-->
                <!--分割线-->
                <div class="divider"></div>
                <!--滚动消息-->
                <ScrollMessage class="message" :messages="messages"/>
            </section>
            <div class="help">
                <Icon name="question-circle" class="help-icon"/>
                <router-link to="/rules">游戏规则</router-link>
            </div>

        </main>
        <router-view @showPromptBox="showPromptBox"/>
    </div>
</template>

<script>
    import {mapState, mapMutations} from 'vuex';
    import Icon from 'vue-awesome/components/Icon';
    import ScrollMessage from '../../components/ScrollMessage';
    import PromptBox from '../../components/PromptBox';
    import BeginButton from '../../components/BeginButton';
    import PreloadImage from '../../components/PreloadImage';
    import {
        GET_CACHE,
        SET_USER_INFO,
        SWITCH_MUSIC,
        PLAY_GAME,
        END_GAME,
        SET_TOKEN,
        SET_DATA_FETCH
    } from '../../store/mutation-types';
    import {getAccessToken, getUserInfo, playGame, wxShare} from '../../api';
    import {getUrlParam} from '../../utils/common_tools'
    import musicIcon from '../../assets/icon/background-music.svg';
    import muteMusicIcon from '../../assets/icon/background-music-mute.svg';
    import imageList from './image-list';
    import wxapi from "../../common/wxapi";


    // 临时 ResultPage
    export default {
        name: 'HomePage',
        data() {
            return {
                imgArr: imageList,
                dataFetched: false,
                showPrompt: false,
                whetherBlur: false,
                promptMessage: '',
                trailerTime: '',
                trailerPrize: 0,
                messages: []
            };
        },
        methods: {
            jsSdkInit() {
                wxapi.wxRegister(this.wxRegCallback)
            },
            wxShareTimeline () {
                // 微信自定义分享到朋友圈
                const shareLink = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa0c3aa5fdd1d1a78&redirect_uri=http%3a%2f%2f172.10.3.98&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
                const shareImg = "http://172.10.3.98:8001/static/20.png"
                let option = {
                    title: '跟我来航天凯天垃圾英雄，一起玩游戏、赢大奖！！！。', // 分享标题, 请自行替换
                    link: shareLink, // 分享链接，根据自身项目决定是否需要split
                    imgUrl: shareImg, // 分享图标, 请自行替换，需要绝对路径
                    success: () => {
                        const type = 'timeline'
                        this.wxShareCallback(type)
                    },
                    error: () => {
                        this.showPromptBox("未知错误")
                    }
                }
                console.log('option',option);
                // 将配置注入通用方法
                wxapi.ShareTimeline(option)
            },
            wxShareCallback(type) {
                console.log("?????")

                const {openid, token} = this.$store.state;
                wxShare({openid, token,type}).then(res =>{
                    if (res.data.code === 200) {
                        this.$store.commit('SHARE');
                    }
                    this.showPromptBox(res.data.msg)
                })
            },

            wxShareAppMessage () {
                const shareLink = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa0c3aa5fdd1d1a78&redirect_uri=http%3a%2f%2f172.10.3.98&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
                const shareImg = "http://172.10.3.98:8001/static/20.png"
                // 微信自定义分享给朋友
                let option = {
                    title: '跟我来航天凯天垃圾英雄，一起玩游戏、赢大奖！！！', // 分享标题, 请自行替换
                    desc: '一起来嗨吧！！！', // 分享描述, 请自行替换
                    link: shareLink, // 分享链接，根据自身项目决定是否需要split
                    imgUrl: shareImg, // 分享图标, 请自行替换，需要绝对路径
                    success: () => {
                        const type = 'friend'
                        console.log("success")

                        this.wxShareCallback(type)
                    },
                    error: () => {
                        this.showPromptBox("未知错误")
                    }
                }
                // 将配置注入通用方法
                wxapi.ShareAppMessage(option)
            },
            wxRegCallback () {
            // 用于微信JS-SDK回调
            this.wxShareTimeline()
            this.wxShareAppMessage()
        },

            set_user_info() {
                let code = getUrlParam('code');
                if (!code) {
                    return
                }
                getAccessToken(code).then(ret => {
                    if (ret.data.code !== 200) {
                        return
                    }

                    let ret_data = ret.data

                    let user_data = JSON.parse(ret_data.data);


                    const userinfo = {
                        openid: user_data.openid,
                        nickname: user_data.nickname,
                        headImgUrl: user_data.headimgurl,
                        score: user_data.score,
                        prize: 0,
                        rank: 0,
                        points: user_data.points,
                        gameNumber: user_data.remain_game.normal,
                        practiceNumber: user_data.remain_practive,
                        userPrizes: user_data.prizes,
                        invitationCode: user_data.invitation_code,
                        isInvited: user_data.is_invited
                    };



                    let trailer = {
                        time: new Date(2018, 2, 5, 21, 30),
                        prize: 200
                    }
                    let messages = [
                        '提示：邀请一名好友双方各获得一次游戏机会',
                        '小技巧：所有答案都在XXX里哦~',
                        '提示：分享到朋友或朋友圈均可获得游戏机会哦~',
                        '小提示：页面右上角有音效开关哦~',
                    ]

                    this.setToken(ret_data.token)
                    this.setUserInfo(userinfo)
                    this.setDataFetch(true)

                    this.messages = messages;
                    this.trailerPrize = trailer.prize || 0;
                    const trailerTime = new Date(trailer.time);
                    const restDay = trailerTime.getDate() - new Date().getDate();
                    switch (restDay) {
                        case 0:
                            this.trailerTime = `今天 ${trailerTime.getHours()}:${trailerTime.getMinutes()}`;
                            break;
                        case 1:
                            this.trailerTime = `明天 ${trailerTime.getHours()}:${trailerTime.getMinutes()}`;
                            break;
                        case 2:
                            this.trailerTime = `后天 ${trailerTime.getHours()}:${trailerTime.getMinutes()}`;
                            break;
                        default:
                            this.trailerTime = `${trailerTime.getMonth() + 1 || 0}月${trailerTime.getDate() || 0}日 ${trailerTime.getHours() || 0}:${trailerTime.getMinutes() || 0}`;
                    }
                })
            },
            play(type) {

                if (this.gameMode) return;
                switch (type) {
                    case 'normal':
                        if (this.gameNumber[0] <= 0) {
                            this.showPromptBox('游戏次数不够，尝试填写邀请码吧！');
                            return;
                        }
                        break;
                    case 'practice':
                        if (this.practiceNumber <= 0) {
                            this.showPromptBox('今日练习次数已用完，试试游戏模式吧！');
                            return;
                        }
                        break;
                    case 'activity':
                        break;
                    default:
                }
                playGame({openid: this.openid, token: this.token, type}).then(res => {
                    if (res.data.code !== 200) {
                        return
                    }
                    this.commitPlayGame(type);
                    this.$router.push('/countdown');
                }).catch(_ => {
                    this.showPromptBox('抱歉，暂时无法答题');
                });
            },
            showPromptBox(msg) {
                if (msg === '') return;
                this.promptMessage = msg;
                this.showPrompt = true;
                clearTimeout(this.timeout);
                this.timeout = setTimeout(() => {
                    this.showPrompt = false;
                }, 2500);
            },
            judgeBlur() {
                this.whetherBlur = ['/invitation', '/share', '/prize'].indexOf(this.$route.path) > -1;
            },
            switchBackgroundMusic() {
                this.switchMusic();
                // 如果静音
                if (this.mute) {
                    this.showPromptBox('音效已关闭');
                } else {
                    this.showPromptBox('音效已开启');
                }
            },
            loadUserInfo() {
                // getUserInfo().then(({ data }) => {
                //   this.setUserInfo(data);
                //   this.messages = data.messages;
                //   this.trailerPrize = data.trailer.prize || 0;
                //   const trailerTime = new Date(data.trailer.time);
                //   const restDay = trailerTime.getDate() - new Date().getDate();
                //   switch (restDay) {
                //     case 0:
                //       this.trailerTime = `今天 ${trailerTime.getHours()}:${trailerTime.getMinutes()}`;
                //       break;
                //     case 1:
                //       this.trailerTime = `明天 ${trailerTime.getHours()}:${trailerTime.getMinutes()}`;
                //       break;
                //     case 2:
                //       this.trailerTime = `后天 ${trailerTime.getHours()}:${trailerTime.getMinutes()}`;
                //       break;
                //     default:
                //       this.trailerTime = `${trailerTime.getMonth() + 1 || 0}月${trailerTime.getDate() || 0}日 ${trailerTime.getHours() || 0}:${trailerTime.getMinutes() || 0}`;
                //   }
                // });
            },


            ...mapMutations({
                getCache: GET_CACHE,
                setUserInfo: SET_USER_INFO,
                switchMusic: SWITCH_MUSIC,
                commitPlayGame: PLAY_GAME,
                endGame: END_GAME,
                setToken: SET_TOKEN,
                setDataFetch: SET_DATA_FETCH,

            })
        },
        computed: {
            musicIconSrc() {
                return this.mute ? muteMusicIcon : musicIcon;
            },
            ...mapState([
                'openid',
                'headImgUrl',
                'gameNumber',
                'practiceNumber',
                'prize',
                'mute',
                'token',
                'score',
                'points',
                'gameMode'
            ])
        },
        watch: {
            $route() {
                this.judgeBlur();
            }
        },
        components: {
            Icon,
            ScrollMessage,
            PromptBox,
            BeginButton,
            PreloadImage
        },
        mounted() {
            this.jsSdkInit()
            this.set_user_info()


        },
        created() {
            // 获取缓存
            this.getCache();
            // 避免刷新后失去背景模糊
            this.judgeBlur();
            this.loadUserInfo();
            // 防止后退回主页再次通过url进入答题页
            this.endGame();
            if (this.$route.params.message) {
                this.$nextTick(() => {
                    this.showPromptBox(this.$route.params.message);
                });
            }
        }
    };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss" src="./style.scss"></style>
