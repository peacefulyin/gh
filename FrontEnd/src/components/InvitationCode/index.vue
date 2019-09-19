<template>
    <transition name="slide-fade">
        <div class="code-container" @click.self="goHome">
            <div class="modal">
                <router-link to="/">
                    <img class="close-btn" src="../../assets/icon/close.svg" alt="close">
                </router-link>

                <h1 :style="{color:this.isInvited&&'black',opacity:this.isInvited&&0.8}">{{this.isInvited? "您已使用邀请" : "请填写邀请码"}}</h1>
                <hr>
                <div class="input" v-if="!this.isInvited">
                    <input
                            v-model="filledCode"
                            type="number"
                            pattern="[0-9]"
                            maxlength="6"
                            min="0"
                            max="999999"
                            placeholder="6位邀请码"
                            autofocus
                    >
                    <button
                            :class="{ active: filledCode.length === 6}"
                            @click="submitCode"
                    >
                        确定
                    </button>
                </div>
                <h2>我的邀请码</h2>
                <p>{{ invitationCode }}</p>
            </div>
        </div>
    </transition>
</template>

<script>
    import {mapActions, mapMutations, mapState} from 'vuex';
    import {invite, setInvitation} from '../../api';
    import {SET_INVITED} from "../../store/mutation-types";

    export default {
        name: 'InvitationCode',
        computed: mapState([
            'invitationCode',
            'openid',
            'token',
            'isInvited'
        ]),
        data() {
            return {
                filledCode: ''
            };
        },

        methods: {
            goHome() {
                this.$router.push('/');
            },
            submitCode() {
                if (this.filledCode.length !== 6) {
                    this.$emit('showPromptBox', '邀请码错误');
                    return;
                }
                if (this.isInvited) {
                    this.$emit('showPromptBox', '您已使用邀请功能');
                    return;
                }
                const {openid, token} = this.$store.state;
                setInvitation({openid, token,invitationCode:this.filledCode}).then(({data}) => {
                    if (data.code === 200) {
                        this.setInvited(true)
                        this.$store.commit('INVITE');
                        this.$emit('showPromptBox', data.msg);

                        this.goHome();
                    } else {
                        this.$emit('showPromptBox', data.msg);
                        this.goHome();
                    }})
                    .catch(() => {
                        this.$emit('showPromptBox', '网络错误，请重试！');
                        this.goHome();
                    });

            },
            ...mapMutations({
                setInvited:SET_INVITED
            })
        }
    };
</script>

<style lang="scss" scoped src="./style.scss"></style>
