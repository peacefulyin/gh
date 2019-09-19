<template>
    <main class="main">
        <div class="game-intro-wrapper" v-if="introState<7&&!notShowIntro">
            <div class="game-intro-bg">

            </div>
            <div class="intro-state-btn-wrapper">
                <button id="befIntroStateBtn" v-show="this.introState>1" @click="jumpIntroState('before')"><span><</span></button>
                <button id="afIntroStateBtn"  v-show="this.introState<6" @click="jumpIntroState('next')"><span>></span></button>
            </div>
            <div class="game-intro-content" >
                <h3>{{gameIntro.barrels[introState].title}}</h3>
                <p>
                    {{gameIntro.barrels[introState].text}}
                </p>
            </div>
            <div class="options-wrapper">
                <BeginButton
                        class="normal-btn"
                        @click.native="introFinish"
                >
                    <span class="text">我知道了</span>
                </BeginButton>
                <div class="stop-remind-wrapper">
                    <input name="stopRemind" type="checkbox" v-model="notShowIntroCheck"  style="margin-right: 2vw"/>
                    <span style="color: white;">不再提示</span>
                </div>
            </div>

        </div>

        <header class="header"></header>
        <svg
                class="animation clock"
                v-if="isAnswered && isRight"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 130.2 130.2">
            <circle
                    class="path circle"
                    fill="none"
                    stroke="#73AF55"
                    stroke-width="6"
                    stroke-miterlimit="10"
                    cx="65.1" cy="65.1"
                    r="62.1"
            >
            </circle>
            <polyline
                    class="path check"
                    fill="none"
                    stroke="#73AF55"
                    stroke-width="10"
                    stroke-linecap="round"
                    stroke-miterlimit="10"
                    points="100.2,40.2 51.5,88.8 29.8,67.5 "
            >
            </polyline>
        </svg>
        <svg
                class="animation clock"
                v-else-if="isAnswered"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 130.2 130.2">
            <circle
                    class="path circle"
                    fill="none"
                    stroke="#D06079"
                    stroke-width="6"
                    stroke-miterlimit="10"
                    cx="65.1"
                    cy="65.1"
                    r="62.1"
            >
            </circle>
            <line
                    class="path line"
                    fill="none"
                    stroke="#D06079"
                    stroke-width="10"
                    stroke-linecap="round"
                    stroke-miterlimit="10"
                    x1="34.4"
                    y1="37.9"
                    x2="95.8"
                    y2="92.3">
            </line>
            <line
                    class="path line"
                    fill="none"
                    stroke="#D06079"
                    stroke-width="10"
                    stroke-linecap="round"
                    stroke-miterlimit="10"
                    x1="95.8"
                    y1="38"
                    x2="34.4"
                    y2="92.2">
            </line>
        </svg>
        <CountdownTimer
                ref="clock"
                v-else
                class="clock"
                :rotateDeg="(totalTime - restTime) / totalTime * 360"
                :text="restTime"
        />
        <div class="background"></div>
        <div class="game-zone" id="gameZone">
            <div class="barrel-list">
                <div class="barrel" ref="wetBarrelWrapper" @click="">
                    <img class="barrel-img crashTarget" ref="wetBarrel" id="wetBarrel"
                         :src="barrelsOpen.wetBarrel?barrels.wet[0]: barrels.wet[1]" alt="">
                </div>
                <div class="barrel" ref="dryBarrelWrapper">
                    <img class="barrel-img crashTarget" ref="dryBarrel" id="dryBarrel"
                         :src="barrelsOpen.dryBarrel?barrels.dry[0]: barrels.dry[1]" alt="">
                    <span></span>
                </div>
                <div class="barrel" ref="recyclableBarrelWrapper">
                    <img class="barrel-img crashTarget" ref="recyclableBarrel" id="recyclableBarrel"
                         :src="barrelsOpen.recyclableBarrel?barrels.recyclable[0]: barrels.recyclable[1]" alt="">
                    <span></span>
                </div>
                <div class="barrel" ref="harmfulBarrelWrapper">
                    <img class="barrel-img crashTarget" ref="harmfulBarrel" id="harmfulBarrel"
                         :src="barrelsOpen.harmfulBarrel?barrels.harmful[0]: barrels.harmful[1]" alt="">
                    <span></span>
                </div>
            </div>
            <div v-show="!isAnswered && restTime!==0" ref="garbage" class="garbage draggable" id="draggedGarbage"><img
                    id="garbageImage" src="" alt=""></div>
        </div>
        <StatusBar
                class="bottom-bar"
                :count="questionCount"
                :current="currentQuestion"
        />
        <ResultPage
                v-if="isEnd"
                :result="isRight"
                :title="showMessage.title"
                :text="showMessage.text"
                :score="totalScore"
        />
        <audio ref="timeout" src="../../assets/audio/timeout.wav">浏览器版本过低，请尽快升级</audio>
        <audio ref="wrong" src="../../assets/audio/wrong.mp3">浏览器版本过低，请尽快升级</audio>
    </main>
</template>

<script>

    import {mapState, mapMutations} from 'vuex';
    import {END_GAME, SET_NOT_SHOW_INTRO, SET_POINTS_AND_SCORE, SET_STATE} from '../../store/mutation-types';
    import CountdownTimer from '../../components/CountdownTimer';
    import Option from '../../components/Option';
    import ResultPage from '../../components/ResultPage';
    import StatusBar from '../../components/StatusBar';
    import PreloadImage from '../../components/PreloadImage';
    import BeginButton from '../../components/BeginButton'
    import {getScore, sendGameResult} from '../../api';
    import wetGarbageImage from '../../assets/garbage/wet_garbage.png'
    import wetGarbageCloseImage from '../../assets/garbage/wet_garbage_close.png'
    import dryGarbageImage from '../../assets/garbage/dry_garbage.png'
    import dryGarbageCloseImage from '../../assets/garbage/dry_garbage_close.png'
    import harmfulGarbageImage from '../../assets/garbage/harmful_garbage.png'
    import harmfulGarbageCloseImage from '../../assets/garbage/harmful_garbage_close.png'
    import recyclableGarbageImage from '../../assets/garbage/recyclable_garbage.png'
    import recyclableGarbageCloseImage from '../../assets/garbage/recyclable_garbage_close.png'

    import wet_garbage_01 from "../../assets/garbage/wet_garbage_01.png"
    import wet_garbage_02 from "../../assets/garbage/wet_garbage_02.png"
    import wet_garbage_03 from "../../assets/garbage/wet_garbage_03.png"
    import wet_garbage_04 from "../../assets/garbage/wet_garbage_04.png"
    import wet_garbage_05 from "../../assets/garbage/wet_garbage_05.png"
    import wet_garbage_06 from "../../assets/garbage/wet_garbage_06.png"
    import dry_garbage_02 from "../../assets/garbage/dry_garbage_02.png"
    import dry_garbage_03 from "../../assets/garbage/dry_garbage_03.png"
    import recyclable_garbage_01 from "../../assets/garbage/recyclable_garbage_01.png"
    import recyclable_garbage_02 from "../../assets/garbage/recyclable_garbage_02.png"
    import recyclable_garbage_03 from "../../assets/garbage/recyclable_garbage_03.png"
    import recyclable_garbage_04 from "../../assets/garbage/recyclable_garbage_04.png"
    import recyclable_garbage_05 from "../../assets/garbage/recyclable_garbage_05.png"
    import recyclable_garbage_06 from "../../assets/garbage/recyclable_garbage_06.png"
    import recyclable_garbage_07 from "../../assets/garbage/recyclable_garbage_07.png"
    import recyclable_garbage_08 from "../../assets/garbage/recyclable_garbage_08.png"
    import recyclable_garbage_09 from "../../assets/garbage/recyclable_garbage_09.png"
    import recyclable_garbage_10 from "../../assets/garbage/recyclable_garbage_10.png"
    import recyclable_garbage_11 from "../../assets/garbage/recyclable_garbage_11.png"
    import recyclable_garbage_12 from "../../assets/garbage/recyclable_garbage_12.png"
    import recyclable_garbage_13 from "../../assets/garbage/recyclable_garbage_13.png"
    import recyclable_garbage_14 from "../../assets/garbage/recyclable_garbage_14.png"
    import recyclable_garbage_15 from "../../assets/garbage/recyclable_garbage_15.png"
    import recyclable_garbage_16 from "../../assets/garbage/recyclable_garbage_16.png"
    import recyclable_garbage_17 from "../../assets/garbage/recyclable_garbage_17.png"
    import recyclable_garbage_18 from "../../assets/garbage/recyclable_garbage_18.png"
    import recyclable_garbage_21 from "../../assets/garbage/recyclable_garbage_21.png"
    import harmful_garbage_01 from "../../assets/garbage/harmful_garbage_01.png"
    import harmful_garbage_02 from "../../assets/garbage/harmful_garbage_02.png"
    import harmful_garbage_03 from "../../assets/garbage/harmful_garbage_03.png"
    import harmful_garbage_04 from "../../assets/garbage/harmful_garbage_04.png"
    import harmful_garbage_05 from "../../assets/garbage/harmful_garbage_05.png"
    import harmful_garbage_06 from "../../assets/garbage/harmful_garbage_06.png"
    import harmful_garbage_07 from "../../assets/garbage/harmful_garbage_07.png"


    export default {
        name: 'Quiz',
        data() {
            return {
                garbageImageElem: null,
                garbageImageContainer: null,
                show: false,
                nowCrash: null,
                beforeCrash: null,
                question: {
                    questionName: '将所有垃圾分类',
                    questionTitle: '',
                    questionOptions: [],
                    questionId: ''
                },
                introState: 0,
                gameIntro: {
                    barrels: [
                        {
                            title: "垃圾英雄",
                            text: "一共10道题，每答对一题可获得1分，总共答对7道以上时可获得10积分，每10积分可参与一次抽奖。"
                        },
                        {
                            title: "湿垃圾",
                            text: "湿垃圾又称为厨余垃圾、有机垃圾,即易腐垃圾,指食材废料、剩菜剩饭、过期食品、瓜皮果核、花卉绿植、中药药渣等易腐的生物质生活废弃物。"
                        },
                        {
                            title: "干垃圾",
                            text: "干垃圾是对垃圾按照可回收垃圾、厨余垃圾、有害垃圾分类后剩余下来的一种垃圾。"
                        },
                        {
                            title: "可回收垃圾",
                            text: "可回收物就是可以再生循环的垃圾。本身或材质可再利用的纸类、硬纸板、玻璃、塑料、金属、塑料包装等废弃物"
                        },
                        {
                            title: "有害垃圾",
                            text: "有害垃圾指废电池、废灯管、废药品、废油漆及其容器等对人体健康或者自然环境造成直接或者潜在危害的生活废弃物。"
                        },
                        {
                            title: "垃圾",
                            text: "按住垃圾后拖动到对应的垃圾桶。"
                        },
                        {
                            title: "计时器",
                            text: "在规定的时间内完成。"
                        },
                    ]
                }
                ,
                barrelsRect: {
                    wetBarrel: null,
                    dryBarrel: null,
                    recyclableBarrel: null,
                    harmfulBarrel: null
                },
                barrelsOpen: {
                    wetBarrel: false,
                    dryBarrel: false,
                    recyclableBarrel: false,
                    harmfulBarrel: false,
                },
                barrels: {
                    wet: [wetGarbageImage, wetGarbageCloseImage],
                    dry: [dryGarbageImage, dryGarbageCloseImage],
                    recyclable: [recyclableGarbageImage, recyclableGarbageCloseImage],
                    harmful: [harmfulGarbageImage, harmfulGarbageCloseImage]
                },
                garbages: [
                    {src: wet_garbage_01, type: "wet"},
                    {src: wet_garbage_02, type: "wet"},
                    {src: wet_garbage_02, type: "wet"},
                    {src: wet_garbage_04, type: "dry"},
                    {src: wet_garbage_05, type: "wet"},
                    {src: wet_garbage_06, type: "wet"},
                    {src: dry_garbage_02, type: "dry"},
                    {src: dry_garbage_03, type: "dry"},
                    {src: recyclable_garbage_01, type: "recyclable"},
                    {src: recyclable_garbage_02, type: "recyclable"},
                    {src: recyclable_garbage_03, type: "recyclable"},
                    {src: recyclable_garbage_04, type: "recyclable"},
                    {src: recyclable_garbage_05, type: "recyclable"},
                    {src: recyclable_garbage_06, type: "recyclable"},
                    {src: recyclable_garbage_07, type: "recyclable"},
                    {src: recyclable_garbage_08, type: "recyclable"},
                    {src: recyclable_garbage_09, type: "recyclable"},
                    {src: recyclable_garbage_10, type: "recyclable"},
                    {src: recyclable_garbage_11, type: "recyclable"},
                    {src: recyclable_garbage_12, type: "recyclable"},
                    {src: recyclable_garbage_13, type: "recyclable"},
                    {src: recyclable_garbage_14, type: "recyclable"},
                    {src: recyclable_garbage_15, type: "recyclable"},
                    {src: recyclable_garbage_16, type: "recyclable"},
                    {src: recyclable_garbage_17, type: "recyclable"},
                    {src: recyclable_garbage_21, type: "recyclable"},
                    {src: harmful_garbage_01, type: "harmful"},
                    {src: harmful_garbage_02, type: "harmful"},
                    {src: harmful_garbage_03, type: "harmful"},
                    {src: harmful_garbage_04, type: "harmful"},
                    {src: harmful_garbage_05, type: "harmful"},
                    {src: harmful_garbage_06, type: "harmful"},
                    {src: harmful_garbage_07, type: "harmful"},
                ],
                questionCount: 10, // 总题数
                currentQuestion: 0, // 当前第几题
                totalTime: 10, // 总共答题时间
                restTime: 10, // 剩余答题时间
                isAnswered: false,
                isRight: false, // 本题是否答对
                isEnd: false, // 是否结束（全部答对或答错一题）
                optionsNum: 4,
                optionsInfo: [],
                costTime: [], // 花费的时间，第一位开始时间，第二位结束时间
                totalScore: 0, // 总分
                showMessage: {}, // 要展示的消息
                successMessage: [
                    {
                        title: 'YOU WIN！！！',
                        text: 'CHEERS, YOU GOT IT! '
                    }, {
                        title: '恭喜你，闯关成功！',
                        text: '分享给好友，刷新奖金上限！'
                    }, {
                        title: '大吉大利，今晚吃鸡！',
                        text: '什么时候我才能像你一样优秀！'
                    }, {
                        title: '恭喜你，闯关成功！',
                        text: '一看你就是自带学神buff的人。'
                    }
                ],
                failMessage: [
                    {
                        title: '很遗憾，闯关失败',
                        text: '快去邀请好友，获得更多答题机会。'
                    }, {
                        title: '智者千虑，必有一失',
                        text: '你已经很不错了，再加把劲！'
                    }, {
                        title: '很遗憾，闯关失败',
                        text: '人不丑也要多读书！'
                    }, {
                        title: '很遗憾，闯关失败',
                        text: '快去资助手册小程序里复习一波吧！'
                    }, {
                        title: '很遗憾，闯关失败',
                        text: '每天都来练习模式练一练吧！'
                    }
                ],
                barrels_open: {  // 垃圾桶状态 false关闭，true 打开
                    wet: true,
                    dry: true,
                    harmful: true,
                    recyclable: true,

                },
                idBarrelElemMap: {},
                notShowIntro: false,
                notShowIntroCheck: false
            };
        },
        methods: {
            introFinish() {
                if(this.notShowIntroCheck){
                    this.setNotShowIntro(true)
                }
                this.introState = 7
                this.countdown();
            },
            resetData() {
                this.show = false;
                this.optionsInfo = new Array(this.optionsNum).fill({selected: false});
                this.isRight = false;
                this.restTime = 10;
            },

            jumpIntroState(type) {
                if (type === 'next') {
                    if(this.introState>=6) return;
                    this.introState += 1
                }else if (type === 'before') {
                    if(this.introState<=1) return;
                    this.introState-=1
                }

            },
            rand(arr) {
                for (var i = arr.length - 1; i >= 0; i--) {
                    var randomIndex = Math.floor(Math.random() * (i + 1));
                    var itemIndex = arr[randomIndex];
                    arr[randomIndex] = arr[i];
                    arr[i] = itemIndex;
                }
                console.log('arr.slice(0, 10)',arr.slice(0, 10).length,arr.slice(0, 10));
                return arr.slice(0,10);
            }
            ,
            // 倒计时
            countdown() {
                clearInterval(this.countdownInterval);
                this.countdownInterval = setInterval(() => {
                    if (this.restTime === 1) {
                        this.playAudio('timeout');
                    }
                    if (this.restTime === 0) {
                        this.optionsInfo = new Array(this.optionsNum).fill({selected: true});
                        clearInterval(this.countdownInterval);
                        if (this.currentQuestion < this.questionCount) {
                            setTimeout(_ => {
                                this.nextQuestion();
                            }, 2000)
                        } else {
                            this.finishGame("b")
                        }
                        return;
                    }
                    this.restTime -= 1;
                }, 1000);
            }

            ,
            // 判断选择是否正确
            showResult() {
                // 结束游戏
                this.endGame();
                // 播放动画后展示结果
                setTimeout(() => {
                    // 随机获取提示文本
                    this.getRandomMessage(this.totalScore >= 2 ? this.successMessage : this.failMessage);
                    this.isEnd = true;
                }, 1200);
            }
            ,
            getRandomMessage(array) {
                this.showMessage = array[Math.floor(Math.random() * array.length)];
            }
            ,
            playAudio(type) {
                if (this.mute) return;
                switch (type) {
                    case 'wrong':
                        this.$refs.wrong.play();
                        break;
                    case 'timeout':
                        this.$refs.timeout.play();
                        break;
                    default:
                }
            }
            ,

            finishGame() {
                clearInterval(this.countdownInterval);
                sendGameResult({
                    openid: this.openid,
                    token: this.token,
                    score: this.totalScore
                }).then(res => {
                    if (res.data.code !== 200) return;
                    const {points, score} = res.data.data
                    this.setPointAndScore({points, score})

                    this.showResult();
                })
            }
            ,

            initGame() {
                let draggableElem = document.querySelectorAll('.draggable')[0];
                let draggie = new Draggabilly(draggableElem, {
                    containment: true
                });
                let dragElem = document.getElementById('draggedGarbage');

                // 获取DOM，应改用refs
                this.garbageImageContainer = document.getElementById("draggedGarbage");
                this.garbageImageElem = document.getElementById("garbageImage");

                //让外部函数可获取this
                let that = this

                //打乱垃圾顺序
                this.garbages = this.rand(this.garbages);

                let count = 0


                draggie.on('dragMove', function (event, pointer, moveVector) {
                    count += 1
                    if (count % 4 === 0) {
                        // let any_crash = false;
                        let anyCrash = false
                        Object.entries(that.barrelsRect).forEach(([key, rect], index) => {
                            const garbageRect = that.$refs.garbage.getBoundingClientRect()
                            const barrelRect = that.$refs[key].getBoundingClientRect();

                            if (that.crash(garbageRect, barrelRect)) {

                                // if(that.beforeCrash !== that.nowCrash){
                                //     that.beforeCrash = that.nowCrash;
                                // }

                                that.nowCrash = key
                                anyCrash = true
                            }
                        })

                        if (!anyCrash) {
                            that.nowCrash = null

                        }

                        // if(!anyCrash){
                        //     that.nowCrash = null
                        //     Object.keys(that.barrelsOpen).forEach(key=>{
                        //         that.barrelsOpen[key] = false
                        //     })
                        // }else {
                        //     that.barrelsOpen[that.nowCrash] = true;
                        // }


                        // if(that.beforeCrash=== that.nowCrash){
                        //     that.barrelsOpen[that.beforeCrash] = false;
                        // }
                        // console.log('barrelsOpen',that.barrelsOpen)
                        // if (!any_crash) {
                        //     that.nowCrash = null;
                        // }
                        // if (that.nowCrash === null) {
                        //     Object.entries(that.barrelsOpen).forEach(([key,value]) =>{
                        //         if (value) {
                        //             that.barrelsOpen[key] = false
                        //         }
                        //
                        //     })
                        // }
                    }

                });


                draggie.on('dragEnd', function (event, pointer, moveVector) {
                    if (that.nowCrash === null) {
                        dragElem.style.left = "50%";
                        dragElem.style.top = "50%";
                    } else {
                        that.isAnswered = true
                        if (that.nowCrash.includes(that.garbages[that.currentQuestion - 1].type)) {
                            that.isRight = true
                            that.totalScore += 1
                        }

                        switch (that.nowCrash) {
                            case "wetBarrel":
                                document.getElementById("wetBarrel").src = wetGarbageCloseImage
                                break;
                            case "dryBarrel":
                                document.getElementById("dryBarrel").src = dryGarbageCloseImage
                                break;
                            case "harmfulBarrel":
                                document.getElementById("harmfulBarrel").src = harmfulGarbageCloseImage
                                break;
                            case "recyclableBarrel":
                                document.getElementById("recyclableBarrel").src = recyclableGarbageCloseImage
                                break;
                            default:

                        }

                        // 隐藏垃圾
                        that.garbageImageContainer.style.opacity = 0;


                        if (that.currentQuestion < that.questionCount) {
                            setTimeout(() => {
                                that.nextQuestion();
                            }, 2000)
                        } else {
                            that.finishGame()
                        }
                    }
                })

                this.garbageImageElem.src = this.garbages[0].src
                this.currentQuestion = 1;
                // this.countdown();
            }
            ,
            crash(garbageRect, barrelRect) {
                return !(garbageRect.left > barrelRect.right || garbageRect.right < barrelRect.left || garbageRect.top > barrelRect.bottom || garbageRect.bottom < barrelRect.top);
            }
            ,

            initBarrelRect() {
                Object.keys(this.barrelsRect).forEach(key => {
                    this.barrelsRect[key] = this.$refs[key].getBoundingClientRect()
                })
            }
            ,
            nextQuestion() {
                const currentQuestionIndex = this.currentQuestion + 1 - 1 //展示逻辑
                this.garbageImageElem.src = this.garbages[currentQuestionIndex].src
                this.currentQuestion += 1
                this.garbageImageContainer.style.left = "50%";
                this.garbageImageContainer.style.top = "46%";
                this.garbageImageContainer.style.opacity = 1
                this.resetData();
                this.countdown();
            }
            ,
            ...
                mapMutations({
                    endGame: END_GAME,
                    setState: SET_STATE,
                    setPointAndScore: SET_POINTS_AND_SCORE,
                    setNotShowIntro: SET_NOT_SHOW_INTRO,

                })

        }
        ,
        created() {
            // 避免直接通过url访问这个页面
            if (!this.gameMode) {
                this.$router.push('/');
            }
            this.resetData();
        }
        ,
        mounted() {
            this.initGame();
            this.initBarrelRect()
        }
        ,
        beforeDestroy() {
            clearInterval(this.countdownInterval);
        }
        ,
        watch: {
            optionsInfo() {
                this.isAnswered = this.optionsInfo.some(element => element.selected);
            }
            ,
            nowCrash(val, oldVal) {
                if (val === null) {
                    Object.entries(this.barrelsOpen).forEach(([key, value]) => {
                        if (value) {
                            this.barrelsOpen[key] = false
                        }
                    })
                } else {
                    this.barrelsOpen[val] = true
                    if (oldVal) {
                        this.barrelsOpen[oldVal] = false;
                    }
                }

            }
            ,
            introState(val,oldVal) {
                // 可在dom中绑定操作，在一个方法中可使逻辑集中。
                switch (val) {
                    case 1:
                        this.$refs.wetBarrelWrapper.style.zIndex = 3;
                        if (val< oldVal) {
                            this.$refs.dryBarrelWrapper.style.zIndex = 'auto';
                        }
                        break;
                    case 2:
                        this.$refs.wetBarrelWrapper.style.zIndex = 'auto';
                        this.$refs.dryBarrelWrapper.style.zIndex = 3;

                        if (val< oldVal) {
                            this.$refs.recyclableBarrelWrapper.style.zIndex = 'auto';
                        }

                        break;
                    case 3:
                        this.$refs.dryBarrelWrapper.style.zIndex = 'auto';
                        this.$refs.recyclableBarrelWrapper.style.zIndex = 3;
                        if (val< oldVal) {
                            this.$refs.harmfulBarrelWrapper.style.zIndex = 'auto';
                        }
                        break;
                    case 4:
                        this.$refs.recyclableBarrelWrapper.style.zIndex = 'auto';
                        this.$refs.harmfulBarrelWrapper.style.zIndex = 3;
                        if (val< oldVal) {
                            this.$refs.garbage.style.zIndex = 'auto';
                        }
                        break;
                    case 5:
                        this.$refs.harmfulBarrelWrapper.style.zIndex = 'auto';
                        this.$refs.garbage.style.zIndex = '3';
                        if (val< oldVal) {
                            document.getElementById('timerContainer').style.zIndex = 2;
                        }
                        break;
                    case 6:
                        this.$refs.garbage.style.zIndex = 'auto';
                        document.getElementById('timerContainer').style.zIndex= 3;
                        break;
                    case 7:
                        document.getElementById('timerContainer').style.zIndex= 2;
                        break;
                    default:
                }

            }
        }
        ,
        computed: {
            ...
                mapState([
                    'openid',
                    'mute',
                    'gameMode',
                    'token',
                    'points',
                    'score',
                ])
        }
        ,
        components: {
            CountdownTimer,
            Option,
            ResultPage,
            StatusBar,
            PreloadImage,
            BeginButton
        }
        ,

    };
</script>

<style lang="scss" scoped src="./style.scss"></style>
