<template>
    <div class="scroll-img-wrapper" ref="scrollImgWrapper">
        <img id="scrollImg" :src="scrollImage" alt="" ref="scrollImg" >
    </div>
</template>

<script>
    export default {
        name: "ScrollImage",
        props:{
            scrolling: {
                type:Boolean,
                default: false
            },
            scrollImage:null
        },
        data() {
            return{
                scrollInterval: null,
                scrollSpeed: 2


            }
        },
        watch:{
            scrolling(bool) {
                console.log('bol',bool)
                if (bool) {
                    this.startScroll()
                }else {
                    this.stopScroll()
                }

            }
        },
        methods:{
            init() {
                this.$refs.scrollImg.style.left = '0px'
                if(this.scrolling){
                    this.startScroll()
                }

            },
            startScroll() {
                const {scrollImg,scrollImgWrapper} = this.$refs
                this.scrollInterval = setInterval(()=>{
                    if (scrollImg.getBoundingClientRect().right <= scrollImgWrapper.offsetWidth) {
                        scrollImg.style.left = '0px'
                        return
                    }
                    scrollImg.style.left = parseInt(scrollImg.style.left)-this.scrollSpeed +'px'
                },50)
            },
            stopScroll() {
                if(!this.scrollInterval)return
                clearInterval(this.scrollInterval)
            }
        },
        mounted() {
            this.init()
        }

    }
</script>

<style lang="scss" scoped src="./style.scss"></style>
