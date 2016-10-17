/**
 * Created with JetBrains WebStorm.
 * User: ty
 * Date: 14-7-23
 * Time: 下午3:38
 * To change this template use File | Settings | File Templates.
 */
var services=angular.module("services",["ngResource","toaster"]);

/* *
 * constant类型的service中的值不会被改变，value定义的service中的值可以被改变
 */
services.constant("Config",{
    thumbs:{
        defaultThumb:"images/app/default_thumb_500.png",
        smallThumb:"images/app/default_small_thumb.png",
        defaultUserProfile:"images/app/default_user_photo.png"
    },
    perLoadCount:10,//作品、评论、资源等每次加载的个数
    hasNoMoreFlag:-1,//作品、评论、资源等没有更多的标志,当没有更多的时候将其的loadId设置为-1
    qNUploadDomain:'http://qiniu-plupload.qiniudn.com/',
    qNBucketDomain:"http://design-pinwall.qiniudn.com/",
    qNImagePreviewSuffix:"?imageMogr2/gravity/Center/crop/:size",
    captcha:"captcha.jpg",
    mainMenu:{
        project:"project",
        box:"box"
    },
    boxStatus:{
        open:0,
        closed:1
    },
    titles:{
        "signIn":"登陆",
        "signUp":"注册",
        "forgetPwd":"忘记密码",
        "editPwd":"修改密码",
        "editInfo":"修改资料",
        "search":"探索"
    },
    templateUrls:{
        "signIn":"views/signIn.html",
        "signUp":"views/signUp.html",
        "forgetPwd":"views/forgetPwd.html",
        "editPwd":"views/changePwd.html",
        "editInfo":"views/editInfo.html",
        "search":"views/searchPanel.html",
        "projectDetail":"views/projectDetail.html"
    },
    urls:{  //用到的路径，主要是用于initPage
        "projectDetail":"projects/:projectId",
        "projectDetailReg":/projects\/\d+/,
        "signIn":"login",
        "signUp":"register",
        "editPwd":"change_password",
        "editInfo":"users/:userId/update",
        "editInfoReg":/users\/[\d]+\/update/,
        "search":"search",
        "searchResult":"search/:content",
        "searchResultReg":/search\/.+/,
        "forgetPwd":"forget_password",
        "boxes":"topics",
        "userHome":"users/:userId"
    },
    imageScale:{
        thumbMedium:"-400x400",
        thumbSmall:"-200x200",
        previewSmall:"-400x300"
    },
    uploadSize:{
        maxMediaSize:"300m", //最大的媒体文件上传大小
        maxImageSize:"2m"//最大的图片文件上传大小
    },
    mediaFilters:{  //媒体类型格式刷选器
        image:"jpg,gif,png,jpeg",
        ppt:"pptx",
        pdf:"pdf",
        mp4:"mp4",
        _3d:"3d",
        zip:"zip",
        swf:"swf",
        html5:"zip"
    },
    mediaTypes:{  //媒体类型
        image:"1",
        ppt:"2",
        pdf:"128",
        _3d:"16",
        mp4:"4",
        zip:"32",
        swf:"64",
        html5:"256"
    },
    mediaTitles:{
        1:"图片",
        2:"ppt文件",
        128:"pdf文件",
        16:"3d文件",
        4:"视频",
        32:"压缩文件",
        64:"swf动画",
        256:"HTML5应用"
    },
    searchTypes:{
        names:{
            fullName:"用户名",
            projectTitle:"作品标题",
            commentContent:"评论内容",
            term:"标签"
        },
        values:{
            fullName:"user_name",
            projectTitle:"artifact_name",
            commentContent:"comment_content",
            term:"term"
        }
    },
    mediaObj:{  //媒体对象
        mediaPos:"pos",
        mediaTitle:"name",
        mediaMemo:"description",
        mediaType:"type",
        mediaThumbFilePath:"profile_image",
        mediaThumbFilename:"profile_filename",
        mediaFilename:"filename",
        mediaFilePath:"media_file",
        mediaId:"mediaId"
    },
    userStatus:{   //用户状态（禁言、激活）
        enabled:"enabled",
        disabled:"disabled"
    },
    emailStatus:{
        pending:"pending",
        invalid:"invalid",
        actively:"actively"
    },
    scrollScreenType:{ //当前在哪个页面滚动
        project:"project",
        box:"box",
        searchResult:"searchResult",
        boxDetail:"boxDetail",
        userDetail:"userDetail" //用户页的用户作品,
    },
    emailUrls:{
        163:"http://mail.163.com",
        126:"http://mail.126.com",
        yeah:"http://www.yeah.net/",
        sina:"http://mail.sina.com.cn",
        yahoo:"http://mail.yahoo.com",
        sohu:"http://mail.sohu.com",
        gmail:"http://mail.google.com",
        hotmail:"http://www.hotmail.com" ,
        live:"http://www.hotmail.com",
        outlook:"http://www.hotmail.com",
        qq:"http://mail.qq.com",
        139:"http://mail.10086.cn"
    },
    validError:{
        required:"请输入此字段！",
        email:"请输入正确的邮箱格式！",
        emailExist:"邮箱已经存在！",
        maxLength:"此字段最多输入${value}个字！",
        minLength:"此字段最少输入${value}个字！",
        pwdEqualError:"两次输入的密码不一致，请重新输入！",
        usernameRequired:"请输入用户名！",
        usernameExist:"用户名已经被注册，请填写其他用户名！",
        validCodeRequired:"请输入验证码！",
        descriptionLengthError:"最多输入140个字！"
    },
    messages:{  //错误提示
        errorTitle:"错误提示",
        clickToSet:"点击上传完成的媒体文件进行设置！",
        deleteConfirm:"确定删除吗？",
        successTitle:"成功提示",
        operationSuccess:"操作成功！",
        optSuccRedirect:"操作成功，稍后跳转到管理页！",
        timeout:"登录超时，请关闭后刷新页面并登录！",
        networkError:"网络连接失败，请稍后重试！",
        captchaError:"验证码错误！",
        operationError:"操作失败，请稍后重试！",
        imgSizeError:"图片不是1:1比例或者宽度非500-800px！",
        peopleImgSizeError:"图片不是1:1比例或者宽度非200-500px！",
        userActiveError:"用户已经激活！",
        loadDataError:"请求数据失败！",
        nameOrPwdError:"用户名或者密码错误！",
        oldPwdError:"原始密码不正确！",
        emailNotExist:"输入的邮箱不存在！",
        activeSuccess:"操作成功，请进入邮箱查看激活邮件！",
        mediaHasNoThumb:"有媒体文件没有上传缩略图，请上传后再预览！",
        hasNoMedia:"没有上传媒体文件或者有上传错误的媒体文件，请上传或者删除后再预览！",
        uploadUnComplete:"当前文件上传未完成，不能选择其他文件！",
        boxUnComplete:"标题、标签、描述等没有填写完整",
        stepOneUnComplete:"标题、标签、描述、缩略图等没有填写完整！",
        pptHasNotUploaded:"此资源还没有被上传到资源服务器，暂时不能查看！",
        pptUploadError:"此资源上传到资源服务器出错，无法查看！",
        systemError:"系统发生错误，请稍后重试！",
        resourceIsInOperation:"资源正在处理，请稍后查看！",
        notFound:"资源丢失，将跳转到首页！",
        topicClosed:"投稿箱已关闭，不能做此操作！"
    },
    ajaxUrls:{
        signIn:"login",
        signUp:"register",
        editInfo:"api/users/:userId/setting",
        changePwd:"change_password",
        forgetPwd:"reset",
        getCurrentUser:"api/users/whoami",
        addUploadedKey:"api/qiniu/add_key",
        createBox:"api/topics\\/",
        updateBox:"api/topics/:boxId",
        getAllBoxes:"api/topics\\/",
        getBoxDetail:"api/topics/:boxId",
        getBoxProjects:"api/topics/:boxId/artifacts",
        setBoxStatus:"api/topics/:boxId/change_status",
        deleteBox:"api/topics/:boxId",
        setUserActive:"confirm",
        setUserRole:"api/users/:userId/role",
        getUserDetail:"api/users/:userId",
        getUserProjects:"api/users/:userId/artifacts",
        getManageUsers:"api/admin/users\\/",
        getManageComments:"api/admin/comments\\/",
        getManageProjects:"api/admin/artifacts\\/",
        upload:"api/qiniu/uptoken",
        getAllProjects:"api/artifacts\\/", //获取首页作品媒体文件
        getProjectDetail:"api/artifacts/:projectId", //获取作品（资源）详情
        deleteProject:"api/artifacts/:projectId",
        toggleShowProject:"api/artifacts/:projectId/visible/toggle",
        praiseProject:"api/artifacts/:projectId/scores/toggle",
        projectCreate:"api/artifacts\\/",
        projectUpdate:"api/artifacts/:projectId",
        addProjectToBox:"api/topics/:boxId/artifacts/append",
        getProjectComments:"api/artifacts/:projectId/comments",
        getSimilarProjects:"data/projects.json",
        addComment:"api/artifacts/:projectId/comments/append",
        deleteComment:"api/artifacts/:projectId/comments/:commentId/remove",
        getAllComments:"data/commentsManage.json",
        getCompleteUrl:"api/search/text_like",
        getSearchProjects:"api/search\\/"
    },
    roles:{   //角色
        admin:"admin",
        user:"user",
        vip:"vip"
    }
});
services.constant("App",{
    version:"1.0"
});
/*services.provider("App",function(){
    //调用的时候返回的是一个包含$get函数的对象
    return {
        $get: function() {
            return {
                showLoading:function(){
                    //$rootScope.showLoading=true;
                },
                hideLoading:function(){
                    //$rootScope.showLoading=false;
                }
            };
        }

    };
});*/
/*services.provider("App",function(){
    //调用的时候返回的是一个包含$get函数的对象
    this.$get=function() {
        return {
            showLoading:function(){
                //$rootScope.showLoading=true;
            },
            hideLoading:function(){
                //$rootScope.showLoading=false;
            }
        };
    }
});*/
/*services.provider("App",{
    //调用的时候返回的是一个包含$get函数的对象
    $get: function() {
        return {
            showLoading:function(){
                //$rootScope.showLoading=true;
            },
            hideLoading:function(){
                //$rootScope.showLoading=false;
            }
        };
    }
});*/

services.service("AjaxErrorHandler",["toaster","Config","CFunctions",function(toaster,Config,CFunctions){
    this.ajaxReturnErrorHandler=function(data){
        //console.log(data);
        var errorCode=data.error_code;
        var message="";
        switch(errorCode){
            case "UNAUTHORIZED":
                message=Config.messages.timeout;
                CFunctions.timeoutRedirect("./",true);
                break;
            case "USER_NOT_EXIST":
                message=Config.messages.nameOrPwdError;
                break;
            case "INVALID_PASSWORD":
                message=Config.messages.nameOrPwdError;
                break;
            case "EMAIL_ALREADY_ASSOCIATED":
                message=Config.messages.emailExist;
                break;
            case "PASSWORD_NOT_SET":
                message=Config.messages.pwdEqualError;
                break;
            case "PASSWORD_NOT_MATCH":
                message=Config.messages.oldPwdError;
                break;
            case "UNEXPECTED_ERROR":
                message=Config.messages.systemError;
                break;
            case "USER_ALREADY_CONFIRMED":
                message=Config.messages.userActiveError;
                break;
            case "CAPTCHA_NOT_MATCH":
                message=Config.messages.captchaError;
                break;
            case "NOT_FOUND":
                message=Config.messages.notFound;
                CFunctions.timeoutRedirect("./",true);
                break;
            case "TOPIC_CLOSED":
                message=Config.messages.topicClosed;
                break;
            default :
                message=Config.messages.loadDataError;
                break;
        }
        toaster.pop('error',Config.messages.errorTitle,message,null,null);
    };

    this.ajaxErrorHandler=function(){
        toaster.pop('error',Config.messages.errorTitle,Config.messages.networkError,null,null);
    };
}]);

services.service("CFunctions",["$rootScope","$location","$http","$timeout","toaster","Config","LocationChanger","Storage",
    function($rootScope,$location,$http,$timeout,toaster,Config,LocationChanger,Storage){

    var postCfg={
        headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
        transformRequest:this.transform
    };

    /**
     * 序列化参数
     * @param obj
     * @returns {string}
     */
    function param(obj){
        var query = '', name, value, fullSubName, subName, subValue, innerObj, i;

        for(name in obj) {
            value = obj[name];

            if(value instanceof Array) {
                for(i=0; i<value.length; ++i) {
                    subValue = value[i];
                    fullSubName = name + '[' + i + ']';
                    innerObj = {};
                    innerObj[fullSubName] = subValue;
                    query += param(innerObj) + '&';
                }
            }
            else if(value instanceof Object) {
                for(subName in value) {
                    subValue = value[subName];
                    fullSubName = name + '[' + subName + ']';
                    innerObj = {};
                    innerObj[fullSubName] = subValue;
                    query += param(innerObj) + '&';
                }
            }
            else if(value !== undefined && value !== null)
                query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
        }

        return query.length ? query.substr(0, query.length - 1) : query;
    }

    /**
     * 发送post请求时的数据处理操作
     * @param data
     * @returns {string}
     */
    function transform(data){
        return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
    }

    /**
     * 提交表单
     * @param {Object} params 对象属性formUrl:"表单提交地址",formParam:"表单数据对象",successCb:"提交成功后回调函数"
     */
    this.ajaxSubmit=function(params){
        $http.post(params.formUrl,params.formParam).
            success(function(data, status, headers, config){
                params.successCb(data);
            }).error(function(data, status, headers, config){
                params.errorCb();
            });

        $http.post(param.formUrl,param.formParam,postCfg). success(param.successCb).
            error(function(data, status, headers, config){
                console.log(data);
            });
    };


    this.timeoutRedirect=function(url,refresh,replace){
        $timeout(function(){
            if(refresh){
                window.location.href=url;
            }else{
                LocationChanger.withReplace(url,replace);
            }

        },3000);

    };

    this.checkMobile=function(){
        var userAgentList = new Array("2.0 MMP", "240320", "AvantGo","BlackBerry", "Blazer",
            "Cellphone", "Danger", "DoCoMo", "Elaine/3.0", "EudoraWeb", "hiptop", "IEMobile", "KYOCERA/WX310K", "LG/U990",
            "MIDP-2.0", "MMEF20", "MOT-V", "NetFront", "Newt", "Nintendo Wii", "Nitro", "Nokia",
            "Opera Mini", "Opera Mobi",
            "Palm", "Playstation Portable", "portalmmm", "Proxinet", "ProxiNet",
            "SHARP-TQ-GX10", "Small", "SonyEricsson", "Symbian OS", "SymbianOS", "TS21i-10", "UP.Browser", "UP.Link",
            "Windows CE", "WinWAP", "Android", "iPhone", "iPod", "iPad", "Windows Phone", "HTC"/*, "GTB"*/);
        var appNameList = new Array("Microsoft Pocket Internet Explorer");

        var userAgent = navigator.userAgent.toString();
        var appName = navigator.appName.toString();
        var agentLength=userAgentList.length,appLength=appNameList.length;
        var i= 0,j=0;

        for (; i<agentLength; i++) {
            if (userAgent.indexOf(userAgentList[i]) >= 0) {
                return true;
            }
        }

        for (; j<appLength; j++) {
            if (appName.indexOf(appNameList[j]) >= 0) {
                return true;
            }
        }

        return false;
    };
    this.getFilePathInfo=function(filePath){
        var extPos=filePath.lastIndexOf(".");

        return {
            filePath:filePath.substring(0,extPos),
            ext:filePath.substring(extPos)
        }
    };
    this.getRandom=function(){
        var date = new Date();
        var mo = (date.getMonth() + 1) < 10 ? ('0' + '' + (date.getMonth() + 1)) : date.getMonth() + 1;
        var dd = date.getDate() < 10 ? ('0' + '' + date.getDate()) : date.getDate();
        var hh = date.getHours() < 10 ? ('0' + '' + date.getHours()) : date.getHours();
        var mi = date.getMinutes() < 10 ? ('0' + '' + date.getMinutes()) : date.getMinutes();
        var ss = date.getSeconds() < 10 ? ('0' + '' + date.getSeconds()) : date.getSeconds();
        var retValue = date.getFullYear() + '' + mo + '' + dd + '' + hh + '' + mi + '' + ss + '';
        for (var j = 0; j < 4; j++) {
            retValue += '' + parseInt(10 * Math.random()) + '';
        }
        if (arguments.length == 1) {
            return arguments[0] + '' + retValue;
        }else{
            return retValue;
        }
    };
    this.setCookie=function(name,value,days){
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var thisCookie = name + "=" + encodeURIComponent(value) +
            ((days) ? "; expires=" + date.toGMTString() : "");
        document.cookie = thisCookie;
    };
    this.getCookie=function(name){
        var nameSG = name + "=";
        if (document.cookie == null || document.cookie.indexOf(nameSG) == -1)
            return null;

        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameSG) == 0) return decodeURIComponent(c.substring(nameSG.length,c.length));
        }

        return null;
    };
    this.createUploader=function(param){
        var uploader = Qiniu.uploader({
            runtimes: 'html5,flash,html4',    //上传模式,依次退化
            browse_button: param.browseButton,       //上传选择的点选按钮，**必需**
            uptoken_url:  Config.ajaxUrls.upload,
            multi_selection:param.multiSelection,
            domain: Config.qNUploadDomain,
            container: param.container,           //上传区域DOM ID，默认是browser_button的父元素，
            filters: {
                mime_types : [
                    { title : "media files", extensions : param.filter }
                ]
                //max_file_size:'1m'
            },
            multipart_params:param.multipartParams,
            max_file_size: param.maxSize,           //最大文件体积限制,qiniu中需要写在这里，而不是卸载filters中
            flash_swf_url: '../lib/Moxie.swf',  //引入flash,相对路径
            max_retries: 3,                   //上传失败最大重试次数
            chunk_size: '4mb',                //分块上传时，每片的体积
            auto_start: true,                 //选择文件后自动上传，若关闭需要自己绑定事件触发上传
            init: {
                'Init':function(up,info){
                    //console.log(up.getOption("max_file_size"));
                },
                'FilesAdded': function(up, files) {
                    if(typeof param.fileAddCb==="function"){
                        param.fileAddCb(up,files);
                    }
                },
                'BeforeUpload':function(up,file){
                    var initObj=up.getOption("init");
                    var keyFunction=initObj.Key;

                    //每次上传都需要告知后台
                    var src = Config.qNBucketDomain + keyFunction(up,file);
                    $http.put(Config.ajaxUrls.addUploadedKey,{key:src},{
                        transformRequest:function(data, headersGetter){
                            //console.log(data);
                            return JSON.stringify(data);
                        },
                        transformResponse:function(data, headersGetter){
                            return JSON.parse(data);
                        }
                    });
                },
                'UploadProgress': function(up, file) {
                    if(typeof param.progressCb==="function"){
                        param.progressCb(up,file);
                    }
                },
                'FileUploaded': function(up, file, info) {
                    if(typeof param.uploadedCb==="function"){
                        param.uploadedCb(file,info);
                    }
                },
                'Error': function(up, err, errTip) {
                    toaster.pop('error',Config.messages.errorTitle,errTip,null,null);

                    //由于qiniu处理了错误信息，在这里要调用$apply来通知view改变状态
                    $rootScope.$apply();

                    up.refresh();
                },
                'Key': function(up, file) {

                    // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
                    // 该配置必须要在 unique_names: false , save_key: false 时才生效
                    var random=Math.floor(Math.random()*10+1)*(new Date().getTime());
                    var filename=file.name;
                    var extPos=filename.lastIndexOf(".");


                    // do something with key here
                    return Storage.currentUser.id+"/"+random+filename.substring(extPos);

                    //return file.name;
                }
            }
        });

        return uploader;
    };
    this.getPathParam=function(){
        var path=location.href;
        var pos=path.lastIndexOf("/");
        return path.substring(pos+1);
    };
    this.getEmailDomain=function(email){
        var domain=email.substring(email.indexOf("@")+1);
        domain=domain.substring(0,domain.lastIndexOf("."));
        domain=domain.replace(/vip.|.com|.cn/g,"");
        return domain;
    };
    this.hideProjectDetail=function(refreshScope){
        var target=$(".de_screen_project_detail");
        var header=target.find(".de_project_header");
        var detail=target.find(".de_project_detail");
        TweenMax.to(header,0.3,{y:-100});
        TweenMax.to(detail,0.3,{y:100});
        TweenMax.to(target,0.4,{opacity:0,onComplete:function(){
            refreshScope();
        }});
    };

    this.formatDate=function(format,dateTime){
        var string,currentDate,year,month,day, h, m, s,fMonth,fDay,fH,fM,fS;

        if(typeof format ==="number"){
            dateTime=format;
            format=null;
        }

        currentDate =dateTime?new Date(dateTime):new Date();
        year=currentDate.getFullYear();
        fMonth=month=currentDate.getMonth()+1;
        fDay=day=currentDate.getDate();
        fH=h=currentDate.getHours();
        fM=m=currentDate.getMinutes();
        fS=s=currentDate.getSeconds();

        if(fMonth<10){
            fMonth="0"+fMonth;
        }
        if(fDay<10){
            fDay="0"+fDay;
        }
        if(fH<10){
            fH="0"+fH;
        }
        if(fM<10){
            fM="0"+fM;
        }
        if(fS<10){
            fS="0"+fS;
        }

        switch(format){
            case "Y-MM-DD hh:mm:ss":
                string=year+"-"+fMonth+"-"+fDay+" "+fH+":"+fM+":"+fS;
                break;
            case "Y-M-D h:m:s":
                string=year+"-"+month+"-"+day+" "+h+":"+m+":"+s;
                break;
            default :
                string=year+"-"+fMonth+"-"+fDay+" "+fH+":"+fM+":"+fS;
                break;
        }

        return string;
    };
	
}]);

services.service("Storage",function(){
    this.lastLoadedId=0;
    this.scrollTimer=null;
    this.currentScrollScreenType="";
    this.loadedProjects=[];
    this.loadedTopProjects=[];


    this.clearScrollData=function(currentScrollScreenType){
        this.lastLoadedId=0;
        this.scrollTimer=null;
        this.currentScrollScreenType=currentScrollScreenType?currentScrollScreenType:"";
        this.loadedProjects=[];
        this.loadedTopProjects=[];
    };

    this.currentUser={  //当前登录的用户信息
        id:0,
        name:"",
        profile:"",
        roles:[],
        description:"",
        email:"",
        active:true,
        commentActive:true
    };

    //用于修改的时候使用
    this.editUserObj={
        profile:"",
        email:"",
        description:""
    };
    this.clearCurrentUser=function(){
        this.currentUser.id=0;
        this.currentUser.name="";
        this.currentUser.roles=[];
        this.currentUser.email="";
        this.currentUser.description="";
        this.currentUser.active=true;
        this.currentUser.commentActive=true;
    };
    this.initEditUserObj=function(){
        this.editUserObj.id=this.currentUser.id;
        this.editUserObj.profile=this.currentUser.profile;
        this.editUserObj.email=this.currentUser.email;
        this.editUserObj.description=this.currentUser.description;
    };
    this.initCurrentUser=function(data){
        this.currentUser.id=data.id?data.id:this.currentUser.id;
        this.currentUser.profile=data.setting.profile_image?data.setting.profile_image:this.currentUser.profile;
        this.currentUser.roles=data.roles?data.roles:this.currentUser.roles;
        this.currentUser.name=data.name?data.name:this.currentUser.name;
        this.currentUser.email=data.email?data.email:this.currentUser.email;
        this.currentUser.description=data.setting.description?data.setting.description:this.currentUser.description;
        this.currentUser.active=typeof data.active !=="undefined"?data.active:this.currentUser.active;
        this.currentUser.commentActive=typeof data.setting.comment_active !=="undefined"?data.setting.comment_active:this.currentUser.commentActive;

        this.initEditUserObj();
    };
});

services.factory('safeApply', ["$rootScope",function($rootScope) {
    return function(scope, fn) {
        fn = angular.isFunction(fn) ? fn : angular.noop;
        scope = scope && scope.$apply ? scope : $rootScope;
        fn();
        if (!scope.$$phase) {
            scope.$apply();
        }
    }
}]);

services.service('LocationChanger', ['$location', '$route', '$rootScope',
    function ($location, $route, $rootScope) {

        this.rootScopeEvent=null;

        //阻止ngView的刷新,返回this是方便链式调用
        this.skipReload = function () {
            var lastRoute = $route.current;
            var me=this;

            //这里绑定过后面会一直响应，关闭弹出层的时候要取消绑定，绑定的时候会返回取消绑定的函数
            me.rootScopeEvent=$rootScope.$on('$locationChangeSuccess', function () {

                $route.current = lastRoute;

                //相应过后，立即取消绑定的事件
                me.rootScopeEvent();
            });


            return me;
        };

        this.canReload=function(){

            //取消$rootScope.$on('$locationChangeSuccess'的绑定
            if(typeof this.rootScopeEvent ==="function"){
                this.rootScopeEvent();
            }

            return this;
        };

        this.withReplace = function (url, doesReplace) {
            if(doesReplace){
                $location.path(url).replace();
            }
            else {
                $location.path(url || '/');
            }

            return this;
        };


}]);

/* $resource default actions
{ 'get':    {method:'GET'},
    'save':   {method:'POST'},
    'query':  {method:'GET', isArray:true},
    'remove': {method:'DELETE'},
    'delete': {method:'DELETE'} };
    */
services.factory("Project",["$rootScope","$resource","Storage","CFunctions","Config",
    function($rootScope,$resource,Storage,CFunctions,Config){
        return {
            getProjects:function(){
                var me= this.resource.query({page:Storage.lastLoadedId+1},function(data){

                    //console.log(data);
                    if(data.artifacts.length<Config.perLoadCount){
                        Storage.lastLoadedId=Config.hasNoMoreFlag;
                    }else{
                        Storage.lastLoadedId++;
                    }

                });

                //手机上使用小图片
                me.$promise.then(function(data){

                    var length=data.artifacts.length;
                    if(CFunctions.checkMobile()){
                        for(var i=0;i<length;i++){
                            var fileInfo=CFunctions.getFilePathInfo(data.artifacts[i]["artifact"]["profile_image"]);
                            data.artifacts[i]["artifact"]["profile_image"]=
                                fileInfo["filePath"]+Config.imageScale.thumbSmall+fileInfo["ext"];
                        }
                    }else{
                        for(var i=0;i<length;i++){
                            var fileInfo=CFunctions.getFilePathInfo(data.artifacts[i]["artifact"]["profile_image"]);
                            data.artifacts[i]["artifact"]["profile_image"]=
                                fileInfo["filePath"]+Config.imageScale.thumbMedium+fileInfo["ext"];
                        }
                    }
                });
                return me;
            },
            getSearchResult:function(content){
                var me= this.resource.getSearchResult({offset:Storage.lastLoadedId,q:content},function(data){
                    //console.log("In services");
                    if(data.artifacts.length<Config.perLoadCount){
                        Storage.lastLoadedId=Config.hasNoMoreFlag;
                    }else{
                        Storage.lastLoadedId+=Config.perLoadCount;
                    }

                });
                me.$promise.then(function(data){

                    var length=data.artifacts.length;
                    if(CFunctions.checkMobile()){
                        for(var i=0;i<length;i++){
                            var fileInfo=CFunctions.getFilePathInfo(data.artifacts[i]["artifact"]["profile_image"]);
                            data.artifacts[i]["artifact"]["profile_image"]=
                                fileInfo["filePath"]+Config.imageScale.thumbSmall+fileInfo["ext"];
                        }
                    }else{
                        for(var i=0;i<length;i++){
                            var fileInfo=CFunctions.getFilePathInfo(data.artifacts[i]["artifact"]["profile_image"]);
                            data.artifacts[i]["artifact"]["profile_image"]=
                                fileInfo["filePath"]+Config.imageScale.thumbMedium+fileInfo["ext"];
                        }
                    }
                });
                return me;
            },
            resource: $resource(Config.ajaxUrls.getAllProjects,{},{
                query:{method:"get",params:{"page":1,"count":Config.perLoadCount}},
                getManageProjects:{method:"get",url:Config.ajaxUrls.getManageProjects,params:{"count":10}},
                get:{method:"get",url:Config.ajaxUrls.getProjectDetail,params:{projectId:0}},
                delete:{method:"delete",url:Config.ajaxUrls.deleteProject,params:{projectId:0}},
                remove:{method:"delete",url:Config.ajaxUrls.deleteProject,params:{projectId:0}},
                save:{method:"post",url:Config.ajaxUrls.projectUpdate,
                    transformResponse:function(data, headersGetter){
                        return JSON.parse(data);
                    }
                },
                add:{method:"put",url:Config.ajaxUrls.projectCreate,params:{},
                    transformResponse:function(data, headersGetter){
                        return JSON.parse(data);
                    }
                },
                addToBox:{method:"put",url:Config.ajaxUrls.addProjectToBox,params:{boxId:0},
                    transformResponse:function(data, headersGetter){
                        return JSON.parse(data);
                    }
                },
                toggleShowProject:{method:"post",url:Config.ajaxUrls.toggleShowProject,params:{projectId:0}},
                praiseProject:{method:"post",url:Config.ajaxUrls.praiseProject,params:{projectId:0}},
                getProjectDetail:{method:"get",url:Config.ajaxUrls.getProjectDetail,params:{projectId:0}},
                getProjectAttachments:{method:"get",url:Config.ajaxUrls.getProjectAttachments,params:{id:0}},
                getSearchResult:{method:"get",url:Config.ajaxUrls.getSearchProjects,params:{offset:0,q:"","count":Config.perLoadCount}},
                getSimilarProjects:{method:"get",url:Config.ajaxUrls.getSimilarProjects,params:{id:0}}
            })
        };
}]);
services.factory("User",["$rootScope","$resource","CFunctions","Storage","Config",function($rootScope,$resource,CFunctions,Storage,Config){
    return {
        getUserProjects:function(userId){
            var me= this.resource.getUserProjects({userId:userId,last_id:Storage.lastLoadedId},function(data){

                if(data.artifacts.length<Config.perLoadCount){
                    Storage.lastLoadedId=Config.hasNoMoreFlag;
                }else{
                    Storage.lastLoadedId=data.artifacts[Config.perLoadCount-1]["artifact"]["id"];
                }

            });
            me.$promise.then(function(data){

                var length=data.artifacts.length;
                if(CFunctions.checkMobile()){
                    for(var i=0;i<length;i++){
                        var fileInfo=CFunctions.getFilePathInfo(data.artifacts[i]["artifact"]["profile_image"]);
                        data.artifacts[i]["artifact"]["profile_image"]=
                            fileInfo["filePath"]+Config.imageScale.thumbSmall+fileInfo["ext"];
                    }
                }else{
                    for(var i=0;i<length;i++){
                        var fileInfo=CFunctions.getFilePathInfo(data.artifacts[i]["artifact"]["profile_image"]);
                        data.artifacts[i]["artifact"]["profile_image"]=
                            fileInfo["filePath"]+Config.imageScale.thumbMedium+fileInfo["ext"];
                    }
                }
            });
            return me;
        },
        resource:$resource(Config.ajaxUrls.getManageUsers,{},{
            query:{method:"get",params:{"count":10}},
            get:{method:"get",url:Config.ajaxUrls.getUserDetail,params:{userId:0}},
            getUserProjects:{method:"get",url:Config.ajaxUrls.getUserProjects,params:{userId:0,last_id:0,"count":Config.perLoadCount}},
            save:{method:"post",url:Config.ajaxUrls.editInfo,params:{userId:0},
                transformRequest:function(data, headersGetter){
                    return JSON.stringify(data);
                },
                transformResponse:function(data, headersGetter){
                    return JSON.parse(data);
                }
            },
            remove:{method:"delete",url:Config.ajaxUrls.deleteProject,params:{id:0}},
            delete:{method:"delete",url:Config.ajaxUrls.deleteProject,params:{id:0}},
            add:{method:"put",url:Config.ajaxUrls.signUp,
                transformRequest:function(data, headersGetter){
                    return JSON.stringify(data);
                },
                transformResponse:function(data, headersGetter){
                    return JSON.parse(data);
                }
            },
            setUserActive:{method:"post",url:Config.ajaxUrls.setUserActive},
            setUserRole:{method:"post",url:Config.ajaxUrls.setUserRole,params:{userId:0}},
            getCurrentUser:{method:"get",url:Config.ajaxUrls.getCurrentUser},
            forgetPwd:{method:"post",url:Config.ajaxUrls.forgetPwd,
                transformRequest:function(data, headersGetter){
                    return JSON.stringify(data);
                },
                transformResponse:function(data, headersGetter){
                    return JSON.parse(data);
                }
            },
            login:{method:"post",url:Config.ajaxUrls.signIn,
                transformRequest:function(data, headersGetter){
                    return JSON.stringify(data);
                },
                transformResponse:function(data, headersGetter){
                    return JSON.parse(data);
                }
            },
            changePwd:{method:"post",url:Config.ajaxUrls.changePwd,
                transformRequest:function(data, headersGetter){
                    return JSON.stringify(data);
                },
                transformResponse:function(data, headersGetter){
                    return JSON.parse(data);
                }
            }
        })
    }
}]);

services.factory("Box",["$rootScope","$resource","CFunctions","Config","Storage",
    function($rootScope,$resource,CFunctions,Config,Storage){
        return {
            getBoxes:function(scope,keyword){

                var me=this.resource.query({scope:scope,keyword:keyword,page:Storage.lastLoadedId+1},function(data){

                    if(data.topics.length<Config.perLoadCount){
                        Storage.lastLoadedId=Config.hasNoMoreFlag;
                    }else{
                        Storage.lastLoadedId++;
                    }

                });

                me.$promise.then(function(data){
                    var length=data.topics.length;
                    if(CFunctions.checkMobile()){
                        for(var i=0;i<length;i++){
                            for(var j= 0,len=data.topics[i]["artifacts"].length;j<len;j++){
                                var fileInfo=CFunctions.getFilePathInfo(data.topics[i]["artifacts"][j]["artifact"]["profile_image"]);
                                data.topics[i]["artifacts"][j]["artifact"]["profile_image"]=
                                    fileInfo["filePath"]+Config.imageScale.thumbSmall+fileInfo["ext"];
                            }
                        }
                    }else{
                        for(var i=0;i<length;i++){
                            for(var j= 0,len=data.topics[i]["artifacts"].length;j<len;j++){
                                var fileInfo=CFunctions.getFilePathInfo(data.topics[i]["artifacts"][j]["artifact"]["profile_image"]);
                                data.topics[i]["artifacts"][j]["artifact"]["profile_image"]=
                                    fileInfo["filePath"]+Config.imageScale.thumbMedium+fileInfo["ext"];
                            }
                        }
                    }
                });
                return me;
            },
            getBoxProjects:function(boxId){
                var me= this.resource.getBoxProjects({boxId:boxId,last_id:Storage.lastLoadedId},function(data){

                    if(data.artifacts.length<Config.perLoadCount){
                        Storage.lastLoadedId=Config.hasNoMoreFlag;
                    }else{
                        Storage.lastLoadedId=data.artifacts[Config.perLoadCount-1]["artifact"]["id"];
                    }

                });
                me.$promise.then(function(data){
                    var length=data.artifacts.length;
                    if(CFunctions.checkMobile()){
                        for(var i=0;i<length;i++){
                            var fileInfo=CFunctions.getFilePathInfo(data.artifacts[i]["artifact"]["profile_image"]);
                            data.artifacts[i]["artifact"]["profile_image"]=
                                fileInfo["filePath"]+Config.imageScale.thumbSmall+fileInfo["ext"];
                        }
                    }else{
                        for(var i=0;i<length;i++){
                            var fileInfo=CFunctions.getFilePathInfo(data.artifacts[i]["artifact"]["profile_image"]);
                            data.artifacts[i]["artifact"]["profile_image"]=
                                fileInfo["filePath"]+Config.imageScale.thumbMedium+fileInfo["ext"];
                        }
                    }
                });
                return me;
            },
            resource:$resource(Config.ajaxUrls.getAllBoxes,{},{
                query:{method:"get",params:{page:1,count:Config.perLoadCount,scope:"",keyword:""}},
                get:{method:"get",url:Config.ajaxUrls.getBoxDetail,params:{boxId:0}},
                remove:{method:"delete",url:Config.ajaxUrls.deleteBox,params:{boxId:0},
                    transformResponse:function(data, headersGetter){
                        return JSON.parse(data);
                    }
                },
                add:{method:"put",url:Config.ajaxUrls.createBox,
                    transformResponse:function(data, headersGetter){
                        return JSON.parse(data);
                    }
                },
                save:{method:"post",url:Config.ajaxUrls.updateBox,params:{boxId:0},
                    transformResponse:function(data, headersGetter){
                        return JSON.parse(data);
                    }
                },
                setBoxStatus:{method:"post",url:Config.ajaxUrls.setBoxStatus,params:{boxId:0}},
                toggleLock:{method:"post",url:Config.ajaxUrls.getSimilarProjects,params:{id:3,lock:true}},
                getBoxProjects:{method:"get",url:Config.ajaxUrls.getBoxProjects,
                    params:{boxId:0,last_id:0,count:Config.perLoadCount}}
            })
        };
}]);
services.factory("Comment",["$rootScope","$resource","Config",function($rootScope,$resource,Config){
    return $resource(Config.ajaxUrls.getManageComments,{},{
        query:{method:"get",params:{"count":10}},
        get:{method:"get",url:Config.ajaxUrls.getProjectDetail,params:{id:0}},
        save:{method:"post",url:"#",params:{id:0}},
        remove:{method:"delete",url:Config.ajaxUrls.deleteComment,params:{projectId:0,commentId:0}},
        delete:{method:"delete",url:Config.ajaxUrls.deleteComment,params:{projectId:0,commentId:0}},
        getCommentsByProject:{method:"get",url:Config.ajaxUrls.getProjectComments,params:{projectId:0}},
        add:{method:"put",url:Config.ajaxUrls.addComment,params:{projectId:0}}
    });
}]);
