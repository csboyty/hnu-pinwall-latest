var shareData={
    imgUrl:"",
    lineLink:location.href,
    descContent:"",
    shareTitle:"",
    appId:""
};
function shareFriend() {
    WeixinJSBridge.invoke('sendAppMessage',{
        "appid": shareData.appId,
        "img_url": shareData.imgUrl,
        "img_width": "200",
        "img_height": "200",
        "link": shareData.lineLink,
        "desc": shareData.descContent,
        "title": shareData.shareTitle
    }, function(res) {

    })
}
function shareTimeline() {
    WeixinJSBridge.invoke('shareTimeline',{
        "appid":"",  //appid 设置空就好了。
        "img_url": shareData.imgUrl,
        "img_width": "200",
        "img_height": "200",
        "link": shareData.lineLink,
        "desc": shareData.descContent,
        "title": shareData.shareTitle
    }, function(res) {

    });
}
function shareWeibo() {
    WeixinJSBridge.invoke('shareWeibo',{
        "content": shareData.descContent,
        "url": shareData.lineLink
    }, function(res) {

    });
}

// 当微信内置浏览器完成内部初始化后会触发WeixinJSBridgeReady事件。
document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {
    // 发送给好友
    WeixinJSBridge.on('menu:share:appmessage', function(argv){
        shareFriend();
    });
    // 分享到朋友圈
    WeixinJSBridge.on('menu:share:timeline', function(argv){
        shareTimeline();
    });
    // 分享到微博
    WeixinJSBridge.on('menu:share:weibo', function(argv){
        shareWeibo();
    });
}, false);
