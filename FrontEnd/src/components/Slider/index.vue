<template>
    <!-- Make a div wrapped slider,set height and width -->
    <div style="width:100%;margin:20px auto;height:100%" >
        <!-- Using the slider component -->
        <slider ref="slider" :options="options">
            <!-- slideritem wrapped package with the components you need -->
            <slideritem v-for="(item,index) in imgList" :key="index" ><img :src="item" alt="" style="width: 100%"></slideritem>
            <!-- Customizable loading -->
            <div slot="loading">loading...</div>
        </slider>
    </div>
</template>
<script>
    // import slider components
    import { slider, slideritem } from 'vue-concise-slider'
    import case1 from '../../assets/slider/case1.png'
    import case2 from '../../assets/slider/case2.png'
    import case3 from '../../assets/slider/case3.png'
    import case4 from '../../assets/slider/case4.png'
    import case5 from '../../assets/slider/case5.png'
    import case6 from '../../assets/slider/case6.png'


    export default {
        name: 'Slider',
        data () {
            return {
                //data list [array]
                someList:[
                    {
                        html: '案例1',
                        style: {
                            'background': '#1bbc9b'
                        }
                    },
                    {
                        html: '案例2',
                        style: {
                            'background': '#4bbfc3'
                        }
                    },
                    {
                        html: '案例3',
                        style: {
                            'background': '#7baabe'
                        }
                    }
                ],
                imgList:[case1,case2,case3,case4,case5,case6],
                //Slider configuration [obj]
                options: {
                    currentPage: 0,
                    autoplay:'3000',
                    loop: true,
                }
            }
        },
        components: {
            slider,
            slideritem
        },
    }
</script>