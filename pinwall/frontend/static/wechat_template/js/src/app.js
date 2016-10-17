var weChatApp=angular.module("weChatApp",[]);

weChatApp.constant("Config",{
    imageScale:{
        thumbSmall:"-200x200",
        previewSmall:"-400x300"
    },
    ajaxUrls:{
        getProjectDetail:"../api/artifacts/:projectId"
    }
});

weChatApp.service("CFunctions",["$rootScope",function($rootScope){
    this.getFilePathInfo=function(filePath){
        var extPos=filePath.lastIndexOf(".");

        return {
            filePath:filePath.substring(0,extPos),
            ext:filePath.substring(extPos)
        }
    };
    this.getPathParam=function(){
        var path=location.href;
        var pos=path.lastIndexOf("/");
        return path.substring(pos+1);
    };
}]);

weChatApp.controller("projectDetail",["$scope","$http","Config","CFunctions",function($scope,$http,Config,CFunctions){
    var projectId=CFunctions.getPathParam();
    $scope.isAndroid=navigator.userAgent.toLowerCase().match(/android/i) == "android";
    $scope.project={};
    $http.get(Config.ajaxUrls.getProjectDetail.replace(":projectId",projectId)).success(function(data){
        $scope.project=data.artifact;
        $scope.project.boxId=data.artifact.topic_id||data.user.id;
        $scope.project.praised=data.praised;
        $scope.project.user=data.user;
        $scope.project.topic=data.topic;

        shareData.imgUrl=$scope.project.profile_image;
        shareData.descContent=$scope.project.description;
        shareData.shareTitle=$scope.project.name;

        var length=$scope.project.assets.length;
        for(var i=0;i<length;i++){
            var fileInfo=CFunctions.getFilePathInfo($scope.project.assets[i]["profile_image"]);
            $scope.project.assets[i]["profile_image"]=
                fileInfo["filePath"]+Config.imageScale.previewSmall+fileInfo["ext"];
        }
    });
}]);

weChatApp.directive("overWeiXin",function(){
    return {
        link: function (scope, element, attrs, ctrl) {
            scope.$watch("project",function(newValue){
                if(!angular.equals({},newValue)){
                    var imgUrl = newValue.profile_image;
                    var lineLink = location.href;
                    var descContent = newValue.description;
                    var shareTitle = newValue.name;
                    var appid = '';
                    function shareFriend() {
                        WeixinJSBridge.invoke('sendAppMessage',{
                            "appid": appid,
                            "img_url": imgUrl,
                            "img_width": "200",
                            "img_height": "200",
                            "link": lineLink,
                            "desc": descContent,
                            "title": shareTitle
                        }, function(res) {

                        })
                    }
                    function shareTimeline() {
                        WeixinJSBridge.invoke('shareTimeline',{
                            "appid":"",  //appid 设置空就好了。
                            "img_url": imgUrl,
                            "img_width": "200",
                            "img_height": "200",
                            "link": lineLink,
                            "desc": descContent,
                            "title": shareTitle
                        }, function(res) {

                        });
                    }
                    function shareWeibo() {
                        WeixinJSBridge.invoke('shareWeibo',{
                            "content": descContent,
                            "url": lineLink
                        }, function(res) {

                        });
                    }

                    // 当微信内置浏览器完成内部初始化后会触发WeixinJSBridgeReady事件。
                    document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {
                        alert("ready test");
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
                }

            });

        }
    }
});
weChatApp.directive('playMp4', ["$sce",function ($sce) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            element.on("click",function(){
                var src=attrs.playMp4;
                element.replaceWith("<video src='"+src+"' controls autoplay></video>");
            });
        }
    };
}]);


