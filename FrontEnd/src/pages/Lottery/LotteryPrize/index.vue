<template>
    <div style="background-color:#fce243;height: 100%" id="wrap">
        <PromptBox v-show="showPrompt" :promptMessage="promptMessage"/>
        <div class="banner"><img src="../../../assets/lottery/banner2.jpg"/></div>
        <div class="activity activity2">
            <div class="activity-amin">
                <h2>我的奖品</h2>

                <div class="tb0-wrapper">
                    <table class="tb0">
                        <tr>
                            <th>中奖时间</th>
                            <th>中奖奖品</th>
                            <th>状态</th>
                            <th>兑奖码</th>
                        </tr>
                        <tr v-for="(item,index) in userPrizes">
                            <td>{{ts2formatDate(item.created_time.$date)}}</td>
                            <td>{{item.prize.name}}</td>
                            <td>{{prize_key_state_map[item.delivery_state]}}</td>
                            <td @click="copyId(item.id)"><span></span></td>
                        </tr>
                    </table>
                </div>

                <a @click.prevent="backToLottery"class="a-main2 a3" id="backLotteryButton" >返回</a>
            </div>
        </div>
    </div>

</template>

<script>
    import '../../../utils/jquery-1.11.3.min';
    import '../../../utils/jquery.rotate';
    import '../../../utils/h5_game_common';
    import '../../../utils/jquery.SuperSlide.2.1.1';
    import '../../../utils/index';
    import {mapState} from "vuex";
    import {getUserPrizes} from "../../../api";
    import PromptBox from '../../../components/PromptBox';


    import copyImg from   '../../../assets/icon/copy.png'

    const prize_key_state_map ={
        0: '未受理',
        1: '已受理',
        2: '配送中',
        3: '已完成',
    }

    export default {
        methods:{
            init(){
                $("html").height("100%");
                $("body").height("100%");
                $("#app").height("100%");
                $("#wrap").height("100%");

                let html = document.querySelector('html');
                function changeRem() {
                    let width = html.getBoundingClientRect().width;
                    html.style.fontSize = width / 10 + 'px';
                }
                changeRem();
                window.addEventListener('resize', changeRem);
            },
            ts2formatDate(timestamp) {
                const now = new Date(timestamp)
                const year = now.getFullYear();  //取得4位数的年份
                const month = now.getMonth() + 1;  //取得日期中的月份，其中0表示1月，11表示12月
                const date = now.getDate();      //返回日期月份中的天数（1到31）
                let hour = now.getHours();     //返回日期中的小时数（0到23）
                let minute = now.getMinutes(); //返回日期中的分钟数（0到59）
                if (hour <= 10) {
                    hour = "0" + hour
                }
                if (minute < 10) {
                    minute = "0" + minute
                }
                return year + "-" + month + "-" + date + " " + hour + ":" + minute;
            },
            backToLottery() {
                this.$router.push({path:'/lottery'});
            },
            copyId(id) {
                const input = document.createElement('input')
                document.body.appendChild(input)
                input.setAttribute('value', id)
                input.select()
                if (document.execCommand('copy')) {
                    document.execCommand('copy')
                    this.showPromptBox("已将兑奖码复制到剪切板。")
                }
                document.body.removeChild(input)
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
        },
        beforeMount(){
            getUserPrizes({openid:this.openid, token:this.token}).then(({data}) => {

                if (data.code !== 200) {
                    return
                }
                this.userPrizes = data.data.user_prizes;
            })
        },
        mounted(){
            this.init();
        },
        computed: {
            ...mapState([
                'openid',
                'token'
            ])
        },
        components:{PromptBox},
        data(){
            return {
                userPrizes: [],
                prize_key_state_map:prize_key_state_map,
                showPrompt: false,
                promptMessage: '',
            }
        },
        name: "index"
    }
</script>

<style lang="scss" scoped src="../style.scss"></style>
<style lang="scss" scoped src="../common.scss"></style>
