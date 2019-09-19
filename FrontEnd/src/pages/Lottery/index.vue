<template>
    <div id="wrap">
        <PreloadImage
                :type="2"
                v-if="!imgLoaded"
        />
        <PromptBox v-show="showPrompt" :promptMessage="promptMessage"/>
        <div class="header clearfix">
            <a @click.prevent="toHomePage" href="" style="position: absolute;top: 20px;">
                <img src="../../assets/icon/close.svg" class="back-btn"/>
            </a>
            <a @click="toPrizePage" style="float: right" id="myWin">
                <p class="my fr">我的奖品</p>
            </a>
            <p class="rule fl" style="float: right;margin-right: 10px">活动规则</p>

            <div class="title"></div>
        </div>
        <!--轮盘-->
        <div class="rotate">
            <div class="lunpai">
                <ul class="prize running">
                    <li v-for="(prize,i) in prizes">
                        <!--                        <div :style="{backgroundImage:'url('+prize.image_url+')'}">-->
                        <div>
                            <span></span>
                            <p>{{prize.name}}</p>
                            <img class="prize-image" :src="prize.image_url" alt="">
                        </div>
                    </li>
                    <li>
                        <div>
                            <span></span>
                            <p>谢谢参与</p>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="ring"></div>
            <div id="btn"></div>
        </div>
        <div class="border">
            您还有 <span>{{points}} 积分，可抽奖</span><span id="change"> {{Math.floor(points/10)}}</span> 次
        </div>
        <!--滚动信息-->
        <!--        <div class="scroll">-->
        <!--            <p></p>-->
        <!--            <div class="sideBox">-->
        <!--                <div class="bd" id="txtMarqueeTop">-->
        <!--                    <ul class="scroll-ul">-->

        <!--                    </ul>-->
        <!--                </div>-->
        <!--            </div>-->
        <!--        </div>-->
        <!--游戏规则弹窗-->
        <div id="mask-rule">
            <div class="box-rule">
                <h2>活动规则说明</h2>
                <span id="close-rule"></span>
                <div class="con">
                    <div class="text">
                        <p>1.活动时间：2019年9月1日——2020年9月1日。<br/>
                            2.本次活动为航天凯天环保科技股份有限公司专属特权活动，仅针对目标用户参与。<br/>
                            3.每10积分可参与抽奖一次。<br/>
                            4.本次活动奖品为垃圾桶、卡通车、手提包、保温杯、和积分奖励。<br/>
                            5.用户奖品联系请凭 <strong>兑奖码</strong> 到 <strong>微信客服</strong> 或电话 <strong>0731-83051118/1128</strong> 领取。<br>
                            6.地址：长沙市长沙县楠竹园路59号中国航天凯天环保工业园能源环保事业部。
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <!--中奖提示-->

        <div>
            <div id="mask">
                <div class="blin"></div>
                btn
                <div class="caidai"></div>
                <div class="winning">
                    <p><b>恭喜您</b><br/>抽中了<span id="text1"></span></p>
                    <a href="#" target="_self" class="btn">确定</a>
                </div>

            </div>
            <!--中奖提示-->
            <div id="mask2">
                <div class="blin"></div>
                <div class="caidai"></div>
                <div class="winning">
                    <p><br/><b>谢谢参与</b></p>
                    <a href="#" target="_self" class="btn">确定</a>
                </div>
            </div>

            <div id="mask3">
                <div class="blin"></div>
                <div class="caidai"></div>
                <div class="winning">
                    <p><br/><b>服务器错误!</b></p>
                    <a href="#" target="_self" class="btn">确定</a>
                </div>
            </div>
<!--            <div id="slider" v-show="showSlider" >-->
<!--                <button style="position: absolute;left: 50%;top: 50%;background: black;z-index: 100" @click="scrollImg">haha</button>-->
<!--                <img id="scrollImg" :src="scroll_image" alt="" v-if="showSlider">-->
<!--&lt;!&ndash;                <Slider v-if="showSlider"  />&ndash;&gt;-->
<!--            </div>-->

            <div id="slider"  v-show="showSlider">
                <ScrollImage :scrolling="showSlider" :scrollImage="scrollImage"/>
            </div>

        </div>


    </div>

</template>

<script>
    import '../../utils/jquery-1.11.3.min';
    import '../../utils/jquery.rotate';
    // import '../../utils/h5_game_common';
    // import '../../utils/jquery.SuperSlide.2.1.1';
    import {getPrizes, startLottery} from "../../api";
    // import '../../utils/index';
    import {mapState, mapMutations} from 'vuex';
    import {SET_POINTS, SET_STATE} from "../../store/mutation-types";
    import Slider from '../../components/Slider';
    import PromptBox from '../../components/PromptBox';
    import PreloadImage from '../../components/PreloadImage'
    import scroll_case from '../../assets/slider/scroll_case.png'
    import ScrollImage from "../../components/ScrollImage/index";

    export default {
        data() {
            return {
                tips: null,
                $ring: null,
                $prize: null,
                $btn: null,
                $change: null,
                $ul: null,
                $li: null,
                $sNum: null,
                $eNum: null,
                $info: null,
                data: null,
                bool: null,
                timer: null,
                $maskRule: null,
                $mask: null,
                $mask2: null,
                $mask3: null,
                $slider: null,
                $winning: null,
                $card: null,
                $close: null,
                prizes: [],
                imgLoaded: false,
                showPrompt: false,
                promptMessage: '',
                refreshCount: 0,
                showSlider:false,
                scrollImage: scroll_case,
            }
        },
        methods: {
            init() {
                this.changeRem();
                window.addEventListener('resize', this.changeRem());
                this.tips = ["500M流量", "1G流量", "50元话费", "20元话费", "300M流量", "谢谢参与~"];
                this.$ring = $(".ring");
                this.$prize = $(".prize");//转盘
                this.$btn = $("#btn");//按钮
                this.$change = $("#change");//显示剩余抽奖机会
                // this.$ul = $(".scroll ul");//中奖信息滚动的盒子
                this.$li = $(".scroll li");//中奖信息滚动的盒子
                this.$sNum = $(".start-num");//手机头号，三位数
                this.$eNum = $(".end-num");//手机尾号，四位数
                this.$info = $(".info");//中奖提示信息
                this.data = {count: 10};//次数
                this.bool = false;//判断是否在旋转，true表示是，false表示否
                this.$maskRule = $("#mask-rule"),//规则遮罩层
                    this.$mask = $("#mask"),//红包遮罩层
                    this.$mask2 = $("#mask2"),//红包遮罩层
                    this.$mask3 = $("#mask3"),//红包遮罩层
                    this.$slider = $("#slider"),//红包遮罩层
                    this.$winning = $(".winning"),//红包
                    this.$card = $("#card"),
                    this.$close = $("#close");

                //link = false;//判断是否在链接跳转中

                $("html").height("100%");
                $("body").height("100%");
                $("#app").height("100%");
                $("#wrap").height("100%");

                let ring = this.$ring;

                this.timer = setInterval(() => {
                    ring.toggleClass("light");
                }, 1000);//定时器

                this.$btn.click(() => {
                    if (this.points < 10) {
                        this.showPromptBox("积分不足")
                        return
                    }

                    if (this.bool) return; // 如果在执行就退出
                    this.bool = true;
                    startLottery({openid: this.openid, token: this.token}).then(res => {
                        const ret_data = res.data
                        if (ret_data.code !== 200) {
                            return
                        }
                        let data
                        if (!ret_data.data.prize_id) {
                            data = 6
                        } else {
                            data = this.prizes.findIndex(item => {
                                return item._id === ret_data.data.prize_id;
                            }) + 1;
                        }

                        this.$prize.removeClass("running");
                        let final_points = this.points
                        final_points -= 10
                        this.setPoints(this.points - 10)

                        let text
                        if(data<6){
                            let prize_name = this.prizes[data - 1].name
                            if (prize_name.includes("积分")) {
                                final_points += parseInt(this.prizes[data - 1].name)
                            }
                            this.setPoints(final_points)
                            text = prize_name
                        }else {
                            text = "谢谢参与~"
                        }


                        this.clickFn(data, text);


                    })


                    // if (this.data.count <= 0) { //当抽奖次数为0时
                    //     this.$change.html(0);//次数显示为0
                    //     this.bool = false;
                    //     alert("没有次数了");
                    // } else { //还有次数就执行
                    //     this.data.count--;
                    //     this.data.count <= 0 && (this.data.count = 0);
                    //     this.$change.html(this.data.count);//显示剩余次数
                    //     this.$prize.removeClass("running");
                    //     this.clickFn();
                    // }
                });

                $(".rule").click(() => {
                    this.$maskRule.show();
                });
                $("#close-rule").click(() => {
                    this.$maskRule.hide();
                });

                $("#close,.win,.btn").click(() => {
                    this.$prize.addClass("running");
                    this.timer = setInterval(() => {
                        this.$ring.toggleClass("light");
                    }, 1000);
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
            changeRem() {
                const html = document.querySelector('html');
                const width = html.getBoundingClientRect().width;
                html.style.fontSize = width / 10 + 'px';
            },

            clickFn(data, text) {
                switch (data) {//中奖概率，可控。根据得到的随机数控制奖品
                    case 1:

                        this.rotateFn(1, 0, text);
                        break;
                    case 2:

                        this.rotateFn(2, -60, text);
                        break;
                    case 3:

                        this.rotateFn(3, -120, text);
                        break;
                    case 4:

                        this.rotateFn(4, 180, text);
                        break;
                    case 5:

                        this.rotateFn(5, 120, text);
                        break;
                    case 6:
                        this.rotateFn(6, 60, text);
                        break;
                }

            },
            rotateFn(awards, angle, text) {
                /*手机号的处理
                var arr = [13477735912, 13100656035, 15926909285];
                var a = arr[0] + "";
                var f = a.substr(0, 3);
                var l = a.substr(7, 4);
                */
                this.bool = true;
                this.$prize.stopRotate();
                this.$prize.rotate({
                    angle: 0,//旋转的角度数
                    duration: 4000, //旋转时间
                    animateTo: angle + 1440, //给定的角度,让它根据得出来的结果加上1440度旋转。也就是至少转4圈
                    callback: () => {
                        this.bool = false; // 标志为 执行完毕
                        // sendRaffleResult().then(ret => {
                        //     if (ret.code === 0) {
                        //         console.log("服务器错误");
                        //         text = "服务器错误"
                        //         win(text);
                        //     }
                        //     if(ret.code ===1){
                        //         win(text);
                        //         show(1, 1, text);
                        //     }
                        //
                        // })
                        // text = "服务器错误";

                        let arr = [13477735912, 13100656035, 15926909285];
                        let a = arr[0] + "";
                        let f = a.substr(0, 3);
                        let l = a.substr(7, 4);

                        this.win(f, l, text);
                        // show(1, 1, text);
                    }
                });
            },
            win(f, l, a1) {
                //遮罩层显示
                let text = a1
                if (text === "谢谢参与~") {
                    this.$mask2.show();
                } else if (text === "服务器错误") {
                    this.$mask3.show()
                } else {
                    $("#text1").html(text);
                    // $('.scroll-ul').append("<li>恭喜<span class=\"start-num\">" + f + "</span>****<span class=\"end-num\">" + l + "</span>获得<span class=\"info\">" + text + "</span></li>")
                    // $("#txtMarqueeTop").slide({
                    //     mainCell: "ul",
                    //     autoPlay: true,
                    //     effect: "topMarquee",
                    //     interTime: 50,
                    //     vis: 6
                    // })
                    this.$mask.show();
                }
                this.showSlider = true
                this.$winning.addClass("reback");


                setTimeout(() => {
                    this.$card.addClass("pull");
                }, 500);

                //关闭弹出层
                $("#close,.win,.btn").click(() => {
                    //$close.click(function () {
                    this.$mask.hide();
                    this.$mask2.hide();
                    this.$mask3.hide()
                    this.showSlider=false;
                    this.$winning.removeClass("reback");
                    this.$card.removeClass("pull");
                });

            },
            toPrizePage() {
                this.$router.push("/LotteryPrize")
            },
            toHomePage() {
                this.$router.push("/")
            },
            fetchPrizes() {
                getPrizes().then(res => {
                    this.prizes = JSON.parse(res.data.data);
                })
            },
            preloadImg() {
                const imgLength = this.prizes.length
                let count = 0

                let imgs = document.querySelectorAll('.prize-image')
                Array.from(imgs).forEach((item) => {
                    let img = new Image()
                    img.onload = () => {
                        count += 1
                        if (imgLength === count) {

                            this.imgLoaded = true;
                        }
                    }
                    img.onerror = () => {
                        this.refreshCount += 1
                        this.preloadImg()

                    }
                    img.src = item.getAttribute('src')
                })


            },
            ...mapMutations({
                setState: SET_STATE,
                setPoints: SET_POINTS,
            })


        },
        computed: {
            // points: () =>{
            //     return this.$store.state.points;
            // },
            ...mapState([
                'openid',
                'token',
                'points'
            ])
        },
        watch: {
            prizes(val, _) {
                if (this.imgLoaded || this.refreshCount > 2) return;
                if (val.length > 0) {
                    this.$nextTick(() => {
                        this.preloadImg()
                    })
                }
            }
        },
        name: "index",
        created() {

            // getPrizes().then(res => {
            //     this.prizes = JSON.parse(res.data.data);
            //
            //     this.canLoad = true
            // })
        },
        mounted() {
            this.init();
            this.fetchPrizes();
        },
        components: {
            ScrollImage,
            Slider,
            PromptBox,
            PreloadImage
        },
    }
</script>

<style lang="scss" scoped src="./style.scss"></style>
<style lang="scss" scoped src="./common.scss"></style>
