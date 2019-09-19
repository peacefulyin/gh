<template>
<!--  <div class="loading-mask" v-if="show">-->
  <div class="loading-mask"  v-if="!hidePreload" style="height: 100%" >
    <div style="height: 100%" v-if="type===1">
      <img  id="rocketGif" src="../../assets/pre_load.gif" alt="" style="width: 100%;height: 100%">
    </div>
    <div class="sk-cube-grid" v-if="type===2">
      <div class="sk-cube sk-cube1"></div>
      <div class="sk-cube sk-cube2"></div>
      <div class="sk-cube sk-cube3"></div>
      <div class="sk-cube sk-cube4"></div>
      <div class="sk-cube sk-cube5"></div>
      <div class="sk-cube sk-cube6"></div>
      <div class="sk-cube sk-cube7"></div>
      <div class="sk-cube sk-cube8"></div>
      <div class="sk-cube sk-cube9"></div>
    </div>
    <div class="loading-text-wrapper" v-if="type===1">
      <p>{{ percentage }}%</p>
    </div>

  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: 'PreloadImage',
  props: {
    imgArr: {
      type: Array,
    },
    type:{
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      loadedCount: 0,
      show: true,
      isHanging:true
    };
  },
  methods: {
    // 无序加载图片
    unorderedPreload() {
      this.imgArr.forEach((imgUrl) => {
        const imgObj = new Image();
        imgObj.addEventListener('load', this.imageLoaded);
        imgObj.addEventListener('error', this.imageLoaded);
        imgObj.src = imgUrl;
      });
    },
    // 加载完成后执行的回调
    imageLoaded() {
      this.loadedCount += 1;
      if (this.loadedCount >= this.imgArr.length) {
        this.show = false;
      }
    },

  },
  computed: {
    percentage() {
      return Math.round((this.loadedCount / this.imgArr.length) * 100)*0.9;
    },
    hidePreload() {
      if (this.type === 1) {
        return (this.show===false && this.dataFetched===true && this.isHanging===false);
      }

      if (this.type === 2) {
        return (this.show===false);
      }

    },
    ...mapState([
      'dataFetched'
    ])
  },
  created() {
    if (this.type === 1) {
      this.unorderedPreload();
      return
    }
    if (this.type === 2) {

    }
  },
  mounted() {
    this.isHanging = false
    // setTimeout(()=>{
    //   this.isHanging = false
    // },4000)
  }
};
</script>

<style lang="scss" scoped src="./style.scss"></style>
