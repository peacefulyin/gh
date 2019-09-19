<!--<template>-->
<!--    <main class="main">-->
<!--        <header class="header"></header>-->
<!--        <svg-->
<!--                class="animation clock"-->
<!--                v-if="isAnswered && isRight"-->
<!--                version="1.1"-->
<!--                xmlns="http://www.w3.org/2000/svg"-->
<!--                viewBox="0 0 130.2 130.2">-->
<!--            <circle-->
<!--                    class="path circle"-->
<!--                    fill="none"-->
<!--                    stroke="#73AF55"-->
<!--                    stroke-width="6"-->
<!--                    stroke-miterlimit="10"-->
<!--                    cx="65.1" cy="65.1"-->
<!--                    r="62.1"-->
<!--            >-->
<!--            </circle>-->
<!--            <polyline-->
<!--                    class="path check"-->
<!--                    fill="none"-->
<!--                    stroke="#73AF55"-->
<!--                    stroke-width="10"-->
<!--                    stroke-linecap="round"-->
<!--                    stroke-miterlimit="10"-->
<!--                    points="100.2,40.2 51.5,88.8 29.8,67.5 "-->
<!--            >-->
<!--            </polyline>-->
<!--        </svg>-->
<!--        <svg-->
<!--                class="animation clock"-->
<!--                v-else-if="isAnswered"-->
<!--                version="1.1"-->
<!--                xmlns="http://www.w3.org/2000/svg"-->
<!--                viewBox="0 0 130.2 130.2">-->
<!--            <circle-->
<!--                    class="path circle"-->
<!--                    fill="none"-->
<!--                    stroke="#D06079"-->
<!--                    stroke-width="6"-->
<!--                    stroke-miterlimit="10"-->
<!--                    cx="65.1"-->
<!--                    cy="65.1"-->
<!--                    r="62.1"-->
<!--            >-->
<!--            </circle>-->
<!--            <line-->
<!--                    class="path line"-->
<!--                    fill="none"-->
<!--                    stroke="#D06079"-->
<!--                    stroke-width="10"-->
<!--                    stroke-linecap="round"-->
<!--                    stroke-miterlimit="10"-->
<!--                    x1="34.4"-->
<!--                    y1="37.9"-->
<!--                    x2="95.8"-->
<!--                    y2="92.3">-->
<!--            </line>-->
<!--            <line-->
<!--                    class="path line"-->
<!--                    fill="none"-->
<!--                    stroke="#D06079"-->
<!--                    stroke-width="10"-->
<!--                    stroke-linecap="round"-->
<!--                    stroke-miterlimit="10"-->
<!--                    x1="95.8"-->
<!--                    y1="38"-->
<!--                    x2="34.4"-->
<!--                    y2="92.2">-->
<!--            </line>-->
<!--        </svg>-->
<!--        <CountdownTimer-->
<!--                v-else-->
<!--                class="clock"-->
<!--                :rotateDeg="(totalTime - restTime) / totalTime * 360"-->
<!--                :text="restTime"-->
<!--        />-->
<!--        <div class="background"></div>-->
<!--        <div class="game-zone">-->
<!--            <div class="barrel-list">-->
<!--                <div class="barrel">-->
<!--                    <img class="barrel-img crashTarget" id="wetBarrel" :src="wet_barrel" alt="">-->
<!--                </div>-->
<!--                <div class="barrel">-->
<!--                    <img class="barrel-img crashTarget" id="dryBarrel" :src="barrels.dry[0]" alt="">-->
<!--                </div>-->
<!--                <div class="barrel">-->
<!--                    <img class="barrel-img crashTarget" id="recyclableBarrel" :src="barrels.recyclable[0]" alt="">-->
<!--                </div>-->
<!--                <div class="barrel">-->
<!--                    <img class="barrel-img crashTarget" id="harmfulBarrel" :src="barrels.harmful[0]" alt="">-->
<!--                </div>-->
<!--            </div>-->
<!--            <div class="garbage draggable" id="draggedGarbage"><img id="garbageImage" src="" alt=""></div>-->
<!--        </div>-->
<!--        <StatusBar-->
<!--                class="bottom-bar"-->
<!--                :count="questionCount"-->
<!--                :current="currentQuestion"-->
<!--        />-->
<!--        <ResultPage-->
<!--                v-if="isEnd"-->
<!--                :result="isRight"-->
<!--                :title="showMessage.title"-->
<!--                :text="showMessage.text"-->
<!--                :score="totalScore"-->
<!--        />-->
<!--        <audio ref="timeout" src="../../assets/audio/timeout.wav">浏览器版本过低，请尽快升级</audio>-->
<!--        <audio ref="wrong" src="../../assets/audio/wrong.mp3">浏览器版本过低，请尽快升级</audio>-->
<!--    </main>-->
<!--</template>-->

<!--<script>-->

<!--    import {mapState, mapMutations} from 'vuex';-->
<!--    import {END_GAME, SET_POINTS_AND_SCORE, SET_STATE} from '../../store/mutation-types';-->
<!--    import CountdownTimer from '../../components/CountdownTimer';-->
<!--    import Option from '../../components/Option';-->
<!--    import ResultPage from '../../components/ResultPage';-->
<!--    import StatusBar from '../../components/StatusBar';-->
<!--    import {getQuestion, getScore, sendGameResult} from '../../api';-->
<!--    import wetGarbageImage from '../../assets/garbage/wet_garbage.png'-->
<!--    import wetGarbageCloseImage from '../../assets/garbage/wet_garbage_close.png'-->
<!--    import dryGarbageImage from '../../assets/garbage/dry_garbage.png'-->
<!--    import dryGarbageCloseImage from '../../assets/garbage/dry_garbage_close.png'-->
<!--    import harmfulGarbageImage from '../../assets/garbage/harmful_garbage.png'-->
<!--    import harmfulGarbageCloseImage from '../../assets/garbage/harmful_garbage_close.png'-->
<!--    import recyclableGarbageImage from '../../assets/garbage/recyclable_garbage.png'-->
<!--    import recyclableGarbageCloseImage from '../../assets/garbage/recyclable_garbage_close.png'-->

<!--    import wet_garbage_01 from "../../assets/garbage/wet_garbage_01.png"-->
<!--    import wet_garbage_02 from "../../assets/garbage/wet_garbage_02.png"-->
<!--    import wet_garbage_03 from "../../assets/garbage/wet_garbage_03.png"-->
<!--    import wet_garbage_04 from "../../assets/garbage/wet_garbage_04.png"-->
<!--    import wet_garbage_05 from "../../assets/garbage/wet_garbage_05.png"-->
<!--    import dry_gabage_01 from "../../assets/garbage/wet_garbage_06.png"-->
<!--    import recyclable_garbage_01 from "../../assets/garbage/recyclable_garbage_01.png"-->
<!--    import recyclable_garbage_02 from "../../assets/garbage/recyclable_garbage_02.png"-->
<!--    import recyclable_garbage_03 from "../../assets/garbage/recyclable_garbage_03.png"-->
<!--    import harmful_garbage_01 from "../../assets/garbage/harmful_garbage_01.png"-->


<!--    export default {-->
<!--        name: 'Quiz',-->
<!--        data() {-->
<!--            return {-->
<!--                garbageImageElem: null,-->
<!--                garbageImageContainer: null,-->
<!--                show: false,-->
<!--                nowCrash: null,-->
<!--                wet_barrel: wetGarbageImage,-->
<!--                question: {-->
<!--                    questionName: '将所有垃圾分类',-->
<!--                    questionTitle: '',-->
<!--                    questionOptions: [],-->
<!--                    questionId: ''-->
<!--                },-->
<!--                barrels:{-->
<!--                    wet:[wetGarbageCloseImage,wetGarbageImage,wetGarbageCloseImage],-->
<!--                    dry:[dryGarbageCloseImage,dryGarbageImage,dryGarbageCloseImage],-->
<!--                    recyclable:[recyclableGarbageCloseImage,recyclableGarbageImage,recyclableGarbageCloseImage],-->
<!--                    harmful:[harmfulGarbageCloseImage,harmfulGarbageImage,harmfulGarbageCloseImage],-->

<!--                },-->
<!--                garbages: [-->
<!--                    {src: wet_garbage_01, type: "wet"},-->
<!--                    {src: wet_garbage_02, type: "wet"},-->
<!--                    {src: wet_garbage_03, type: "wet"},-->
<!--                    {src: wet_garbage_04, type: "wet"},-->
<!--                    {src: wet_garbage_05, type: "wet"},-->
<!--                    {src: dry_gabage_01, type: "dry"},-->
<!--                    {src: recyclable_garbage_01, type: "recyclable"},-->
<!--                    {src: recyclable_garbage_02, type: "recyclable"},-->
<!--                    {src: recyclable_garbage_03, type: "recyclable"},-->
<!--                    {src: harmful_garbage_01, type: "harmful"},-->
<!--                ],-->
<!--                questionCount: 10, // 总题数-->
<!--                currentQuestion: 0, // 当前第几题-->
<!--                totalTime: 10, // 总共答题时间-->
<!--                restTime: 10, // 剩余答题时间-->
<!--                isAnswered: false,-->
<!--                isRight: false, // 本题是否答对-->
<!--                isEnd: false, // 是否结束（全部答对或答错一题）-->
<!--                optionsNum: 4,-->
<!--                optionsInfo: [],-->
<!--                costTime: [], // 花费的时间，第一位开始时间，第二位结束时间-->
<!--                totalScore: 0, // 总分-->
<!--                showMessage: {}, // 要展示的消息-->
<!--                successMessage: [-->
<!--                    {-->
<!--                        title: 'YOU WIN！！！',-->
<!--                        text: 'CHEERS, YOU GOT IT! '-->
<!--                    }, {-->
<!--                        title: '恭喜你，闯关成功！',-->
<!--                        text: '分享给好友，刷新奖金上限！'-->
<!--                    }, {-->
<!--                        title: '大吉大利，今晚吃鸡！',-->
<!--                        text: '什么时候我才能像你一样优秀！'-->
<!--                    }, {-->
<!--                        title: '恭喜你，闯关成功！',-->
<!--                        text: '一看你就是自带学神buff的人。'-->
<!--                    }-->
<!--                ],-->
<!--                failMessage: [-->
<!--                    {-->
<!--                        title: '很遗憾，闯关失败',-->
<!--                        text: '快去邀请好友，获得更多答题机会。'-->
<!--                    }, {-->
<!--                        title: '智者千虑，必有一失',-->
<!--                        text: '你已经很不错了，再加把劲！'-->
<!--                    }, {-->
<!--                        title: '很遗憾，闯关失败',-->
<!--                        text: '人不丑也要多读书！'-->
<!--                    }, {-->
<!--                        title: '很遗憾，闯关失败',-->
<!--                        text: '快去资助手册小程序里复习一波吧！'-->
<!--                    }, {-->
<!--                        title: '很遗憾，闯关失败',-->
<!--                        text: '每天都来练习模式练一练吧！'-->
<!--                    }-->
<!--                ],-->
<!--                barrels_open: {  // 垃圾桶状态 false关闭，true 打开-->
<!--                    wet: true,-->
<!--                    dry: true,-->
<!--                    harmful: true,-->
<!--                    recyclable: true,-->

<!--                }-->
<!--            };-->
<!--        },-->
<!--        methods: {-->
<!--            resetData() {-->
<!--                this.show = false;-->
<!--                this.optionsInfo = new Array(this.optionsNum).fill({selected: false});-->
<!--                this.isRight = false;-->
<!--                this.restTime = 10;-->
<!--            },-->
<!--            rand(arr) {-->
<!--                var len = arr.length-->
<!--                for (var i = arr.length - 1; i >= 0; i&#45;&#45;) {-->
<!--                    var randomIndex = Math.floor(Math.random() * (i + 1));-->
<!--                    var itemIndex = arr[randomIndex];-->
<!--                    arr[randomIndex] = arr[i];-->
<!--                    arr[i] = itemIndex;-->
<!--                }-->
<!--                return arr;-->
<!--            },-->
<!--            // 倒计时-->
<!--            countdown() {-->
<!--                clearInterval(this.countdownInterval);-->
<!--                this.countdownInterval = setInterval(() => {-->
<!--                    if (this.restTime === 1) {-->
<!--                        this.playAudio('timeout');-->
<!--                    }-->
<!--                    if (this.restTime === 0) {-->
<!--                        this.optionsInfo = new Array(this.optionsNum).fill({selected: true});-->
<!--                        clearInterval(this.countdownInterval);-->
<!--                        if (this.currentQuestion < this.questionCount) {-->
<!--                            setTimeout(_ => {-->
<!--                                this.nextQuestion();-->
<!--                            }, 2000)-->
<!--                        } else {-->
<!--                            this.finishGame("b")-->
<!--                        }-->
<!--                        return;-->
<!--                    }-->
<!--                    this.restTime -= 1;-->
<!--                }, 1000);-->
<!--            },-->
<!--            showQuestion() {-->
<!--                // 获取题目-->
<!--                getQuestion({-->
<!--                    openid: this.openid,-->
<!--                    type: this.gameMode,-->
<!--                    order: this.currentQuestion + 1-->
<!--                })-->
<!--                    .then(({data}) => {-->
<!--                        this.currentQuestion += 1;-->
<!--                        this.question = data;-->
<!--                        this.show = true;-->
<!--                        this.countdown();-->
<!--                        // 开始计时-->
<!--                        this.costTime[0] = new Date().getTime();-->
<!--                    });-->
<!--            },-->
<!--            // 判断选择是否正确-->
<!--            showResult() {-->
<!--                // 结束游戏-->
<!--                this.endGame();-->
<!--                // 播放动画后展示结果-->
<!--                setTimeout(() => {-->
<!--                    // 随机获取提示文本-->
<!--                    this.getRandomMessage(this.totalScore >= 2 ? this.successMessage : this.failMessage);-->
<!--                    this.isEnd = true;-->
<!--                }, 1200);-->
<!--            },-->
<!--            getRandomMessage(array) {-->
<!--                this.showMessage = array[Math.floor(Math.random() * array.length)];-->
<!--            },-->
<!--            playAudio(type) {-->
<!--                if (this.mute) return;-->
<!--                switch (type) {-->
<!--                    case 'wrong':-->
<!--                        this.$refs.wrong.play();-->
<!--                        break;-->
<!--                    case 'timeout':-->
<!--                        this.$refs.timeout.play();-->
<!--                        break;-->
<!--                    default:-->
<!--                }-->
<!--            },-->

<!--            finishGame() {-->
<!--                clearInterval(this.countdownInterval);-->
<!--                sendGameResult({-->
<!--                    openid: this.openid,-->
<!--                    token: this.token,-->
<!--                    score: this.totalScore-->
<!--                }).then(res => {-->
<!--                    if (res.data.code !== 200) return;-->
<!--                    const {points, score} = res.data.data-->
<!--                    console.log("points, score",points, score);-->
<!--                    this.setPointAndScore({points,score})-->
<!--                    console.log('points,score',this.points,this.score)-->

<!--                    this.showResult();-->
<!--                })-->
<!--            },-->

<!--            setBarrelImage(type, state) {-->
<!--                console.log("haha")-->
<!--                this.barrels.wet_barrel = wetGarbageImage-->
<!--                console.log('this.barrels.wet_barrel',this.barrels.wet_barrel);-->
<!--            },-->

<!--            initGame() {-->
<!--                let draggableElem = document.querySelectorAll('.draggable')[0];-->
<!--                let draggie = new Draggabilly(draggableElem, {-->
<!--                    containment: true-->
<!--                });-->
<!--                let dragElem = document.getElementById('draggedGarbage');-->

<!--                // 获取DOM，应改用refs-->
<!--                this.garbageImageContainer = document.getElementById("draggedGarbage");-->
<!--                this.garbageImageElem = document.getElementById("garbageImage");-->

<!--                //让外部函数可获取this-->
<!--                let that = this-->

<!--                //打乱垃圾顺序-->
<!--                this.garbages = this.rand(this.garbages);-->


<!--                draggie.on('dragMove', function (event, pointer, moveVector) {-->
<!--                    let targetElems = document.getElementsByClassName("crashTarget");-->
<!--                    let any_crash = false;-->
<!--                    for (let i = 0; i < targetElems.length; i++) {-->
<!--                        let target = targetElems[i];-->
<!--                        if (crash(dragElem, target)) {-->
<!--                            switch (target.id) {-->
<!--                                case "wetBarrel":-->
<!--                                    console.log("ha");-->
<!--                                    that.setBarrelImage("a","b")-->

<!--                                    that.nowCrash = target.id;-->
<!--                                    any_crash = true;-->
<!--                                    break;-->
<!--                                case "dryBarrel":-->
<!--                                    document.getElementById("dryBarrel").src = dryGarbageImage;-->
<!--                                    that.nowCrash = target.id;-->
<!--                                    any_crash = true;-->
<!--                                    break;-->
<!--                                case "harmfulBarrel":-->
<!--                                    document.getElementById("harmfulBarrel").src = harmfulGarbageImage;-->
<!--                                    that.nowCrash = target.id;-->
<!--                                    any_crash = true;-->
<!--                                    break;-->
<!--                                case "recyclableBarrel":-->
<!--                                    document.getElementById("recyclableBarrel").src = recyclableGarbageImage;-->
<!--                                    that.nowCrash = target.id;-->
<!--                                    any_crash = true;-->
<!--                                    break;-->
<!--                                default:-->

<!--                            }-->
<!--                        }-->
<!--                    }-->
<!--                    if (!any_crash) {-->
<!--                        that.nowCrash = null;-->
<!--                    }-->
<!--                    if (that.nowCrash === null) {-->
<!--                        document.getElementById("wetBarrel").src = wetGarbageCloseImage;-->
<!--                        document.getElementById("dryBarrel").src = dryGarbageCloseImage;-->
<!--                        document.getElementById("harmfulBarrel").src = harmfulGarbageCloseImage;-->
<!--                        document.getElementById("recyclableBarrel").src = recyclableGarbageCloseImage;-->
<!--                    }-->
<!--                });-->


<!--                draggie.on('dragEnd', function (event, pointer, moveVector) {-->
<!--                    console.log("this.nowCrash", that.nowCrash);-->
<!--                    if (that.nowCrash === null) {-->
<!--                        dragElem.style.left = "50%";-->
<!--                        dragElem.style.top = "50%";-->
<!--                    } else {-->
<!--                        console.log("crashed");-->
<!--                        console.log('this.isAnswered', that.isAnswered);-->

<!--                        console.log(that.nowCrash, that.garbages[that.currentQuestion - 1].type)-->
<!--                        that.isAnswered = true-->
<!--                        if (that.nowCrash.includes(that.garbages[that.currentQuestion - 1].type)) {-->
<!--                            that.isRight = true-->
<!--                            that.totalScore += 1-->
<!--                        }-->


<!--                        // 隐藏垃圾-->
<!--                        console.log("that.garbageImageContainer", that.garbageImageContainer);-->
<!--                        that.garbageImageContainer.style.opacity = 0;-->

<!--                        if(that.currentQuestion < that.questionCount){-->
<!--                            setTimeout(() => {-->
<!--                                that.nextQuestion();-->
<!--                            }, 2000)-->
<!--                        }else {-->
<!--                            that.finishGame()-->
<!--                        }-->

<!--                        // dragElem.style.opacity = 0;-->
<!--                        // this.nextQuestion();-->
<!--                    }-->
<!--                })-->

<!--                function crash(obj1, obj2) {-->
<!--                    let first_Rect = getRect(obj1);-->
<!--                    let second_rect = getRect(obj2);-->

<!--                    let firstLeft = getRect(obj1).left;-->
<!--                    let firstTop = getRect(obj1).top;-->
<!--                    let firstRight = getRect(obj1).right;-->
<!--                    let firstBottom = getRect(obj1).bottom;-->

<!--                    let secondLeft = getRect(obj2).left;-->
<!--                    let secondTop = getRect(obj2).top;-->
<!--                    let secondRight = getRect(obj2).right;-->
<!--                    let secondBottom = getRect(obj2).bottom;-->
<!--                    if (firstLeft > secondRight || firstRight < secondLeft || firstTop > secondBottom || firstBottom < secondTop) {-->
<!--                        return false;-->
<!--                    } else {-->
<!--                        return true;-->
<!--                    }-->
<!--                }-->

<!--                function getRect(obj) {-->
<!--                    return obj.getBoundingClientRect();-->
<!--                }-->

<!--                this.garbageImageElem.src = this.garbages[0].src-->
<!--                this.currentQuestion = 1;-->
<!--            },-->
<!--            nextQuestion() {-->
<!--                const currentQuestionIndex = this.currentQuestion + 1 - 1 //展示逻辑-->
<!--                this.garbageImageElem.src = this.garbages[currentQuestionIndex].src-->
<!--                this.currentQuestion += 1-->

<!--                this.garbageImageContainer.style.left = "50%";-->
<!--                this.garbageImageContainer.style.top = "50%";-->
<!--                this.garbageImageContainer.style.opacity = 1-->
<!--                this.resetData();-->
<!--                this.countdown();-->
<!--            },-->
<!--            ...mapMutations({-->
<!--                endGame: END_GAME,-->
<!--                setState: SET_STATE,-->
<!--                setPointAndScore: SET_POINTS_AND_SCORE,-->

<!--            })-->

<!--        },-->
<!--        created() {-->
<!--            // 避免直接通过url访问这个页面-->
<!--            if (!this.gameMode) {-->
<!--                this.$router.push('/');-->
<!--            }-->
<!--            this.resetData();-->
<!--        },-->
<!--        mounted() {-->
<!--            this.initGame();-->
<!--            // this.showQuestion();-->
<!--            // setTimeout(() => {-->
<!--            //   this.isAnswered =true-->
<!--            //   this.isRight = true-->
<!--            //   // isAnswered && isRight-->
<!--            // },3000)-->
<!--            // setTimeout(() => {-->
<!--            //   this.resetData();-->
<!--            //   // isAnswered && isRight-->
<!--            // },5000)-->

<!--        },-->
<!--        beforeDestroy() {-->
<!--            clearInterval(this.countdownInterval);-->
<!--        },-->
<!--        watch: {-->
<!--            optionsInfo() {-->
<!--                this.isAnswered = this.optionsInfo.some(element => element.selected);-->
<!--            }-->
<!--        },-->
<!--        computed: {-->
<!--            ...mapState([-->
<!--                'openid',-->
<!--                'mute',-->
<!--                'gameMode',-->
<!--                'token',-->
<!--                'points',-->
<!--                'score',-->
<!--            ])-->
<!--        },-->
<!--        components: {-->
<!--            CountdownTimer,-->
<!--            Option,-->
<!--            ResultPage,-->
<!--            StatusBar-->
<!--        },-->

<!--    };-->
<!--</script>-->

<!--<style lang="scss" scoped src="./style.scss"></style>-->
<!--game-zone-->