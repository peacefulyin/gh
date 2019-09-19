import wx from 'weixin-jsapi'
import Axios from 'axios'
import {apiLocalRoot} from "../api";

console.log('wx',wx);
const wxApi = {
    wxRegister (callback) {
        // 这边的接口请换成你们自己的
        Axios.post(`${apiLocalRoot}/wechat/get_jssdk_config`, { url: window.location.href.replace(location.hash, '') }, { timeout: 5000, withCredentials: true }).then((res) => {
            let data = res.data.data // PS: 这里根据你接口的返回值来使用
            console.log('res.data.data',res.data.data);
            wx.config({
                debug: false, // 开启调试模式
                appId: data.appid, // 必填，公众号的唯一标识
                timestamp: data.timestamp, // 必填，生成签名的时间戳
                nonceStr: data.nonceStr, // 必填，生成签名的随机串
                signature: data.signature, // 必填，签名，见附录1
                jsApiList: ['onMenuShareTimeline','onMenuShareAppMessage','onMenuShareQQ','onMenuShareWeibo'] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
            })
        }).catch((error) => {
            console.log(error)
        })
        wx.ready((res) => {
            // 如果需要定制ready回调方法
            if (callback) {
                callback()
                console.log("callback seted")
            }
        })
    },
    /**
     * [ShareTimeline 微信分享到朋友圈]
     * @param {[type]} option [分享信息]
     * @param {[type]} success [成功回调]
     * @param {[type]} error   [失败回调]
     */
    ShareTimeline (option) {
        console.log('ShareTimeline')
        wx.onMenuShareTimeline({
            title: option.title, // 分享标题
            link: option.link, // 分享链接
            imgUrl: option.imgUrl, // 分享图标
            success () {
                // 用户成功分享后执行的回调函数
                option.success()
            },
            cancel () {
                // 用户取消分享后执行的回调函数
                // option.error()
            },
            error() {
                option.error()

            }
        })
    },
    /**
     * [ShareAppMessage 微信分享给朋友]
     * @param {[type]} option [分享信息]
     * @param {[type]} success [成功回调]
     * @param {[type]} error   [失败回调]
     */
    ShareAppMessage (option) {
        console.log('Shared friend')
        wx.onMenuShareAppMessage({
            title: option.title, // 分享标题
            desc: option.desc, // 分享描述
            link: option.link, // 分享链接
            imgUrl: option.imgUrl, // 分享图标
            success () {
                // 用户成功分享后执行的回调函数
                option.success()
            },
            cancel () {
                // 用户取消分享后执行的回调函数
                option.error()
            }
        })
    }
}

export default wxApi