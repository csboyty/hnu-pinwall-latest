/**
 * Created with JetBrains WebStorm.
 * User: ty
 * Date: 14-7-24
 * Time: 下午3:12
 * To change this template use File | Settings | File Templates.
 */
/**
 * Created with JetBrains WebStorm.
 * User: ty
 * Date: 14-7-17
 * Time: 下午3:42
 * To change this template use File | Settings | File Templates.
 */
var viewControllers=angular.module("viewControllers",["services","toaster","directives","ngTable"]);

viewControllers.controller("projects",['$scope',"$interval","$location","Config","Storage","Project",
    function($scope,$interval,$location,Config,Storage,Project){

    //覆盖了super里面的，一定要分开写，不然无法覆盖（这样可以覆盖的原理是因为对象是地址类型）
    $scope.mainFlags.currentMenu=Config.mainMenu.project;
    $scope.mainFlags.extMenuActive=false;

    Storage.clearScrollData(Config.scrollScreenType.project);


    Storage.loadedProjects=$scope.projects=[];
    Project.getProjects().$promise.then(function(data){
        //console.log("In views");
        var count= 0,length=data.artifacts.length;
        var inter=$interval(function(){
            if(count<length){
                $scope.projects.push(data.artifacts[count]);
                count++;
            }else{
                $interval.cancel(inter);
            }
        },200);

        //弹出层页面初始进来都是加载作品数据
        var path=$location.path();

        if(path.indexOf(Config.urls.editPwd)!==-1||path.indexOf(Config.urls.signIn)!==-1||
            path.indexOf(Config.urls.signUp)!==-1||path.match(Config.urls.editInfoReg)!==null||
            path.indexOf(Config.urls.forgetPwd)!==-1||
            (path.indexOf(Config.urls.search)!==-1&&path.match(Config.urls.searchResultReg)==null)){
            $scope.showBlackOut();
        }
    });
}]);

viewControllers.controller("timeline",['$scope',"$interval","$location","Config","Storage","Project",
    function($scope,$interval,$location,Config,Storage,Project){

    //覆盖了super里面的，一定要分开写，不然无法覆盖（这样可以覆盖的原理是因为对象是地址类型）
    $scope.mainFlags.currentMenu=Config.mainMenu.project;
    $scope.mainFlags.extMenuActive=false;

    Storage.clearScrollData(Config.scrollScreenType.project);


    Storage.loadedProjects=$scope.projects=[];
    Project.getProjects().$promise.then(function(data){
        //console.log("In views");
        var count= 0,length=data.artifacts.length;
        var inter=$interval(function(){
            if(count<length){
                $scope.projects.push(data.artifacts[count]);
                count++;
            }else{
                $interval.cancel(inter);
            }
        },200);

        //弹出层页面初始进来都是加载作品数据
        var path=$location.path();

        if(path.indexOf(Config.urls.editPwd)!==-1||path.indexOf(Config.urls.signIn)!==-1||
            path.indexOf(Config.urls.signUp)!==-1||path.match(Config.urls.editInfoReg)!==null||
            path.indexOf(Config.urls.forgetPwd)!==-1||
            (path.indexOf(Config.urls.search)!==-1&&path.match(Config.urls.searchResultReg)==null)){
            $scope.showBlackOut();
        }
    });
}]);

viewControllers.controller("projectDetail",["$scope","$window","Storage","Config","CFunctions","Project","Comment","toaster","LocationChanger",
    function($scope,$window,Storage,Config,CFunctions,Project,Comment,toaster,LocationChanger){

        function loadMore(){
            var count=Config.perLoadCount;
            if($scope.commentObj.allComments.length<Config.perLoadCount){
                count=$scope.commentObj.allComments.length;
            }

            $scope.commentObj.showComments=
                $scope.commentObj.showComments.concat($scope.commentObj.allComments.splice(0,count));

            //判断是否还有
            if($scope.commentObj.allComments.length==0){
                $scope.commentObj.hasMore=false;
            }
        }

        var projectId=CFunctions.getPathParam();
        //console.log(projectId);

        $scope.mainFlags.extMenuActive=false;
        $scope.mainFlags.showProjectDetailFlag=true;
        $scope.mainFlags.showMainWrapper=false;

        $scope.hideProjectDetail=function(){
			//重置de_project_detail位置到页面顶端
			$scope.closeProjectDetailPanel();
			LocationChanger.skipReload();
			history.back();
			
			//关闭动画
            /*CFunctions.hideProjectDetail(function(){
                //重置de_project_detail位置到页面顶端
                $scope.closeProjectDetailPanel();
                LocationChanger.skipReload();
                history.back();
            });*/
        };

        $scope.project={};
        Project.resource.getProjectDetail({projectId:projectId},function(data){
            $scope.project=data.artifact;
            $scope.project.boxId=data.artifact.topic_id||data.user.id;
            $scope.project.praised=data.praised;
            $scope.project.user=data.user;
            $scope.project.topic=data.topic;

            //手机上使用小图片
            if($scope.isMobile){
                var length=$scope.project.assets.length;
                for(var i=0;i<length;i++){
                    var fileInfo=CFunctions.getFilePathInfo($scope.project.assets[i]["profile_image"]);
                    $scope.project.assets[i]["profile_image"]=
                        fileInfo["filePath"]+Config.imageScale.previewSmall+fileInfo["ext"];
                }
            }
        });

        $scope.commentObj={
            newComment:"",
            allComments:[],
            showComments:[],
            hasMore:true
        };
        Comment.getCommentsByProject({projectId:projectId},function(data){
            $scope.commentObj.allComments=data.comments;
            loadMore();
        });

        $scope.loadMoreComments=function(){
            loadMore();
        };
        $scope.addComment=function(projectId,content){

            Comment.add({projectId:projectId},{content:content},function(data){
                if($scope.commentObj.hasMore){
                    $scope.commentObj.allComments.push({
                        comment:{
                            id:data.comment_id,
                            content:content,
                            commented_at:CFunctions.formatDate()
                        },
                        user:{
                            id:$scope.currentUser.id,
                            fullname:$scope.currentUser.name,
                            setting:{
                                profile_image:$scope.currentUser.profile
                            }
                        }
                    });
                }else{
                    $scope.commentObj.showComments.push({
                        comment:{
                            id:data.comment_id,
                            content:content,
                            commented_at:CFunctions.formatDate()
                        },
                        user:{
                            id:$scope.currentUser.id,
                            fullname:$scope.currentUser.name,
                            setting:{
                                profile_image:$scope.currentUser.profile
                            }
                        }
                    });

                }

                //跟新view面板的数据
                var length=Storage.loadedProjects.length;
                for(var i=0;i<length;i++){
                    if(Storage.loadedProjects[i]["artifact"]["id"]==projectId){
                        Storage.loadedProjects[i]["artifact"]["comment_count"]++;
                    }
                }

                $scope.commentObj.newComment="";
                $scope.project.comment_count++;
                toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);
            });
        };
        $scope.deleteComment=function(id,index,projectId){
            if(confirm(Config.messages.deleteConfirm)){
                Comment.delete({projectId:projectId,commentId:id},function(data){

                    //跟新view面板的数据
                    var length=Storage.loadedProjects.length;
                    for(var i=0;i<length;i++){
                        if(Storage.loadedProjects[i]["artifact"]["id"]==projectId){
                            Storage.loadedProjects[i]["artifact"]["comment_count"]--;
                        }
                    }
                    $scope.project.comment_count--;
                    $scope.commentObj.showComments.splice(index,1);
                    toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);
                });
            }
        };

        /*$scope.similarProjects=[];
        Project.resource.getSimilarProjects({id:projectId},function(data){

            $scope.similarProjects=data.artifacts;

            //这里也要处理手机上的图片
            *//*====================================================================*//*

        });*/

        $scope.deleteProject=function(id){
            if(confirm(Config.messages.deleteConfirm)){
                Project.resource.delete({projectId:id},function(data){

                    //跟新view面板的数据
                    var length=Storage.loadedProjects.length,length1=Storage.loadedTopProjects.length;
                    for(var i=0;i<length;i++){
                        if(Storage.loadedProjects[i]["artifact"]["id"]==id){
                            Storage.loadedProjects.splice(i,1);
                            break;
                        }
                    }

                    //更新优秀作品数据
                    if(length1!=0){
                        for(var j=0;j<length;j++){
                            if(Storage.loadedTopProjects[j]["artifact"]["id"]==id){
                                Storage.loadedTopProjects.splice(j,1);
                                break;
                            }
                        }
                    }
                    toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);


                    $scope.hideProjectDetail();
                });
            }
        };

        $scope.praiseProject=function(id){
            if($scope.currentUser.id){
                Project.resource.praiseProject({projectId:id},{},function(data){

                    //跟新view面板的数据
                    var length=Storage.loadedProjects.length;
                    var rolesString=$scope.currentUser.roles.join(",");
                    for(var i=0;i<length;i++){
                        if(Storage.loadedProjects[i]["artifact"]["id"]==id){
                            if($scope.project.praised==false){
                                if(rolesString.match(Config.roles.vip)!==null){
                                    Storage.loadedProjects[i]["artifact"]["honor_count"]++;
                                    $scope.project.honor_count++;
                                }else{
                                    Storage.loadedProjects[i]["artifact"]["praise_count"]++;
                                    $scope.project.praise_count++;
                                }
                            }else{
                                if(rolesString.match(Config.roles.vip)!==null){
                                    Storage.loadedProjects[i]["artifact"]["honor_count"]--;
                                    $scope.project.honor_count--;
                                }else{
                                    Storage.loadedProjects[i]["artifact"]["praise_count"]--;
                                    $scope.project.praise_count--;
                                }
                            }

                            //跳出循环
                            break;

                        }
                    }
                    $scope.project.praised=!$scope.project.praised;

                });
            }else{
                $scope.login(true);
            }
        };
        $scope.toggleShowProject=function(id){
            Project.resource.toggleShowProject({projectId:id},{},function(data){
                $scope.project.visible=!$scope.project.visible;
                toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);
            });
        };
}]);

viewControllers.controller("projectUpdate",["$scope","$routeParams","$http","$route","toaster","safeApply","Config","Storage","Box","CFunctions","Project",
    function($scope,$routeParams,$http,$route,toaster,safeApply,Config,Storage,Box,CFunctions,Project){
        var currentMediaUpload=null,currentFileObj=null;

        function addTag(tag){

            //indexOf是ECMAScript5的新方法
            if($scope.project.terms.indexOf(tag)===-1&&tag!==""){
                $scope.project.terms.push(tag);
            }

            $scope.newTag="";
        }
        function imageAddedCb(files){
            var fileLength=files.length;
            var random="";
            for (var i = 0; i < fileLength; i++) {
                random=CFunctions.getRandom("random_");
                var obj=$scope.project.medias[random]={};
                obj[Config.mediaObj.mediaThumbFilePath]=Config.thumbs.smallThumb;
                obj[Config.mediaObj.mediaThumbFilename]="0%";
                obj[Config.mediaObj.mediaType]=Config.mediaTypes.image;

                fileIdToMediaIdHash[files[i]["id"]]=random;
            }
            $scope.$apply();
        }
        function fileAddedCb(up,files,type){
            currentMediaUpload=up;
            currentFileObj=files[0];
            $scope.currentMediaObj[Config.mediaObj.mediaFilename]="0%";
            $scope.currentMediaObj[Config.mediaObj.mediaType]=type;
            $scope.mediaMenuActive=false;
            $scope.$apply();
        }
        function imageProgressCb(up,file){
            if($scope.project.medias[fileIdToMediaIdHash[file.id]]){
                $scope.project.medias[fileIdToMediaIdHash[file.id]][Config.mediaObj.mediaThumbFilename]=file.percent+"%";
                $scope.$apply();
            }
        }
        function fileProgressCb(up,file){
            if($scope.currentMediaObj[Config.mediaObj.mediaFilename]){
                $scope.currentMediaObj[Config.mediaObj.mediaFilename]=file.percent+"%";
                //$scope.$apply();
                safeApply();
            }
        }
        function imageUploadedCb(file,info){
            var currentMedia=$scope.project.medias[fileIdToMediaIdHash[file.id]];
            if(currentMedia){
                var res = JSON.parse(info);
                var path = Config.qNBucketDomain + res.key; //获取上传成功后的文件的Url
                currentMedia[Config.mediaObj.mediaThumbFilePath]=path;
                currentMedia[Config.mediaObj.mediaThumbFilename]=file.name;
                currentMedia[Config.mediaObj.mediaFilename]="";
                currentMedia[Config.mediaObj.mediaFilePath]="";
                currentMedia[Config.mediaObj.mediaMemo]="";
                currentMedia[Config.mediaObj.mediaTitle]="";
            }
            $scope.$apply();
        }
        function fileUploadedCb(file,info){
            if($scope.currentMediaObj[Config.mediaObj.mediaFilename]){
                var res = JSON.parse(info);
                var path = Config.qNBucketDomain + res.key; //获取上传成功后的文件的Url
                $scope.currentMediaObj[Config.mediaObj.mediaFilename]=file.name;
                $scope.currentMediaObj[Config.mediaObj.mediaFilePath]=path;

                $scope.$apply();
            }

        }
        function createMediaUploader(buttonId,containerId,type){
            var filter=Config.mediaFilters.image;
            var maxSize=Config.uploadSize.maxMediaSize;
            switch(type){
                case Config.mediaTypes.mp4:
                    filter=Config.mediaFilters.mp4;
                    break;
                case Config.mediaTypes.pdf:
                    filter=Config.mediaFilters.pdf;
                    break;
                case Config.mediaTypes.ppt:
                    filter=Config.mediaFilters.ppt;
                    break;
                case Config.mediaTypes.zip:
                    filter=Config.mediaFilters.zip;
                    break;
                case Config.mediaTypes.swf:
                    filter=Config.mediaFilters.swf;
                    break;
                case Config.mediaTypes.html5:
                    filter=Config.mediaFilters.html5;
                    break;
            }

            CFunctions.createUploader({
                browseButton:buttonId,
                multiSelection:false,
                container:containerId,
                multipartParams:null,
                maxSize:maxSize,
                filter:filter,
                fileAddCb:function(up,files){
                    fileAddedCb(up,files,type);
                },
                progressCb:fileProgressCb,
                uploadedCb:function(file,info){
                    fileUploadedCb(file,info);
                }
            });
        }

        function initProjectData(id){
            Project.resource.get({projectId:id},function(data){
                var random;
                var length=data.artifact.assets.length;

                $scope.project.id=data.artifact.id;
                $scope.project.profile_image=data.artifact.profile_image;
                //$scope.project.assets=data.artifact.assets;
                $scope.project.terms=data.artifact.terms;
                $scope.project.name=data.artifact.name;
                $scope.project.description=data.artifact.description;
                $scope.project.user={
                    id:data.user.id,
                    name:data.user.fullname,
                    profile:data.user.setting.profile_image
                };

                //初始化附件
                for (var i = 0; i < length; i++) {
                    random=CFunctions.getRandom(i+"_");
                    $scope.project.medias[random]=data.artifact.assets[i];
                }
            });
        }

        function initBoxData(id){
            Box.resource.get({boxId:id},function(data){
                $scope.box.name=data.topic.name;
            });
        }

        var fileIdToMediaIdHash={};

        $scope.project={
            id:0,
            profile_image:Config.thumbs.defaultThumb,
            medias:{},
            terms:[],
            assets:[],
            user:$scope.currentUser,
            name:"",
            description:""
        };
        $scope.box={
            id:0,
            name:""
        };

        if($routeParams.boxId){
            $scope.box.id=$routeParams.boxId;
            initBoxData($scope.box.id);
        }


        $scope.currentMediaObj={};

        $scope.uploadMediaMenuActive=false;
        $scope.currentTab=1;
        $scope.newTag="";
        $scope.mainFlags.extMenuActive=false;
        $scope.mainFlags.currentMenu="";

        $scope.closeProjectDetailPanel();

        Storage.clearScrollData();

        if($routeParams.projectId){
            initProjectData($routeParams.projectId);
        }


        $scope.getPreviewMedias=function(mediaClass,attr){

            //每次都重新获取
            $scope.project.assets=[];
            var mediaItems=document.getElementsByClassName(mediaClass);
            var length=mediaItems.length;
            var mediaId="";
            for(var i=0;i<length;i++){

                //console.log(mediaItems[i].getAttribute('data-media-id'));
                mediaId=mediaItems[i].getAttribute(attr);
                $scope.project.medias[mediaId][Config.mediaObj.mediaPos]=i+1;
                $scope.project.assets.push($scope.project.medias[mediaId]);

            }
        };

        $scope.setTabActive=function(index){

            //判断是否数据都填写完整,才能执行界面转换
            if(index>1){
                if(!$scope.project.name||$scope.project.terms.length==0||
                    $scope.project.profile_image==Config.thumbs.defaultThumb||!$scope.project.description){

                    toaster.pop('error',Config.messages.errorTitle,Config.messages.stepOneUnComplete,null,null);
                    return false;
                }
            }

            if(index==3){
                var hasUnCompleteUpload=false,noMedia=false;

                //判断媒体文件是否上传完整
                if(angular.equals({},$scope.project.medias)){
                    noMedia=true;
                }else{
                    //文件名中是可以使用%的,要配合判断是否带后缀才能判断是否完成了上传
                    if(!angular.equals({},$scope.currentMediaObj)&&
                        $scope.currentMediaObj[Config.mediaObj.mediaFilename].match("%")!==null&&
                        $scope.currentMediaObj[Config.mediaObj.mediaFilename].indexOf(".")==-1){
                        hasUnCompleteUpload=true;
                    }else{
                        for(var obj in $scope.project.medias){
                            if($scope.project.medias[obj][Config.mediaObj.mediaThumbFilename].match("%")!==null&&
                                $scope.project.medias[obj][Config.mediaObj.mediaThumbFilename].indexOf(".")==-1){
                                hasUnCompleteUpload=true;
                                break;
                            }
                        }
                    }
                }

                if(hasUnCompleteUpload){
                    toaster.pop('error',Config.messages.errorTitle,Config.messages.uploadUnComplete);
                    return false;
                }else if(noMedia){
                    toaster.pop('error',Config.messages.errorTitle,Config.messages.hasNoMedia);
                    return false;
                }
            }

            //在点击的时候需要去掉媒体文件的active状态
            if(!angular.equals({},$scope.currentMediaObj)&&index!=2){
                $scope.currentMediaObj.active=undefined;
                delete $scope.currentMediaObj.active;
                $scope.currentMediaObj={};
            }

            //设置状态
            $scope.currentTab=index;

        };

        $scope.deleteTag=function(index){
            $scope.project.terms.splice(index,1);
        };
        $scope.keyDownAddTag=function($event,tag){
            if($event.which==13){
                addTag(tag);
            }
        };
        $scope.blurAddTag=function(tag){
            addTag(tag);
        };

        $scope.createThumbUploader=function(buttonId,containerId){
            CFunctions.createUploader({
                browseButton:buttonId,
                multiSelection:false,
                container:containerId,
                multipartParams:null,
                maxSize:Config.uploadSize.maxImageSize,
                fileAddCb:null,
                progressCb:null,
                filter:Config.mediaFilters.image,
                uploadedCb:function(file,info){
                    var res = JSON.parse(info);
                    var src= Config.qNBucketDomain + res.key; //获取上传成功后的文件的Url

                    //判断是否是1：1
                    $http.get(src+"?imageInfo",{
                        transformRequest:function(data, headersGetter){
                            return JSON.stringify(data);
                        },
                        transformResponse:function(data, headersGetter){
                            return JSON.parse(data);
                        }
                    }).success(function(data,status,headers,config,statusText ){
                        //console.log(data);
                        if(data.width===data.height&&data.width<=800&&data.width>=500){
                            $scope.project.profile_image = src;
                            //$scope.$apply();
                        }else{
                            toaster.pop('error',Config.messages.errorTitle,Config.messages.imgSizeError,null,null);
                        }

                    });
                }
            });
        };

        $scope.showMediaMenu=function(){
            $scope.uploadMediaMenuActive=true;
        };
        $scope.hideMediaMenu=function(){
            $scope.uploadMediaMenuActive=false;
        };

        $scope.createImageUploader=function(buttonId,containerId){
            CFunctions.createUploader({
                browseButton:buttonId,
                multiSelection:true,
                container:containerId,
                multipartParams:null,
                maxSize:Config.uploadSize.maxImageSize,
                filter:Config.mediaFilters.image,
                fileAddCb:function(up,files){
                    imageAddedCb(files);
                },
                progressCb:imageProgressCb,
                uploadedCb:function(file,info){
                    imageUploadedCb(file,info);
                }
            });
        };

        $scope.createPptUploader=function(buttonId,containerId){
            createMediaUploader(buttonId,containerId,Config.mediaTypes.ppt);
        };

        $scope.createPdfUploader=function(buttonId,containerId){
            createMediaUploader(buttonId,containerId,Config.mediaTypes.pdf);
        };

        $scope.createZipUploader=function(buttonId,containerId){
            createMediaUploader(buttonId,containerId,Config.mediaTypes.zip);
        };

        $scope.createMp4Uploader=function(buttonId,containerId){
            createMediaUploader(buttonId,containerId,Config.mediaTypes.mp4);
        };
        $scope.createSwfUploader=function(buttonId,containerId){
            createMediaUploader(buttonId,containerId,Config.mediaTypes.swf);
        };
        $scope.createHtml5Uploader=function(buttonId,containerId){
            createMediaUploader(buttonId,containerId,Config.mediaTypes.html5);
        };
        $scope.deleteMedia=function(mediaId){
            if(confirm(Config.messages.deleteConfirm)){
                if(angular.equals($scope.currentMediaObj,$scope.project.medias[mediaId])){
                    $scope.currentMediaObj={};
                }

                $scope.project.medias[mediaId]=undefined;
                delete $scope.project.medias[mediaId];
            }
        };

        /*****************媒体设置部分********************/
        $scope.showSetPanel=function(mediaId){
            if($scope.currentMediaObj[Config.mediaObj.mediaThumbFilename]!=
                $scope.project.medias[mediaId][Config.mediaObj.mediaThumbFilename]){

                //有文件没上传完成的时候，不能选择其他项
                if(!angular.equals({},$scope.currentMediaObj)&&
                    $scope.currentMediaObj[Config.mediaObj.mediaFilename].match("%")!==null){
                    toaster.pop("error",Config.messages.errorTitle,Config.messages.uploadUnComplete);
                }else{
                    $scope.currentMediaObj.active=undefined;
                    delete $scope.currentMediaObj.active;

                    $scope.currentMediaObj = $scope.project.medias[mediaId];
                    $scope.currentMediaObj["active"]=true;
                }
            }
        };

        $scope.setMediaTitle=function(title){
            $scope.currentMediaObj[Config.mediaObj.mediaTitle]=title;
        };
        $scope.setMediaMemo=function(memo){
            $scope.currentMediaObj[Config.mediaObj.mediaMemo]=memo;
        };
        $scope.deleteBindFile=function(){
            if(confirm(Config.messages.deleteConfirm)){
                if(currentMediaUpload){
                    currentMediaUpload.removeFile(currentFileObj);
                    currentMediaUpload.stop();
                }

                $scope.currentMediaObj[Config.mediaObj.mediaFilename]="";
                $scope.currentMediaObj[Config.mediaObj.mediaFilePath]="";
                $scope.currentMediaObj[Config.mediaObj.mediaType]=Config.mediaTypes.image;
            }
        };

        $scope.mediaSetThumbUploader=function(buttonId,containerId){
            CFunctions.createUploader({
                browseButton:buttonId,
                multiSelection:false,
                container:containerId,
                multipartParams:null,
                maxSize:Config.uploadSize.maxImageSize,
                fileAddCb:null,
                progressCb:null,
                filter:Config.mediaFilters.image,
                uploadedCb:function(file,info){
                    var res = JSON.parse(info);
                    var path=Config.qNBucketDomain + res.key; //获取上传成功后的文件的Url
                    $scope.currentMediaObj[Config.mediaObj.mediaThumbFilePath] =path;
                    $scope.currentMediaObj[Config.mediaObj.mediaThumbFilename]=file.name;

                    $scope.$apply();
                }
            });
        };

        $scope.uploadFormSubmit=function(){
            if($scope.project.id){
                Project.resource.save({projectId:$scope.project.id},$scope.project,function(data){
                    toaster.pop("success",Config.messages.successTitle,Config.messages.optSuccRedirect,null,null);
                });
            }else{
                if($scope.box.id!==0){
                    Project.resource.addToBox({boxId:$scope.box.id},$scope.project,function(data){
                        toaster.pop("success",Config.messages.successTitle,Config.messages.optSuccRedirect,null,null);
                    });
                }else{
                    Project.resource.add($scope.project,function(data){
                        toaster.pop("success",Config.messages.successTitle,Config.messages.optSuccRedirect,null,null);
                    });
                }
            }

            CFunctions.timeoutRedirect(Config.urls.userHome.replace(":userId",$scope.currentUser.id),false,true);
        }
    }]);

viewControllers.controller("projectsManage",['$scope',"toaster","ngTableParams","Project","Config",
    function($scope,toaster,ngTableParams,Project,Config){

        $scope.mainFlags.currentMenu="";

        $scope.types=[{
            name:Config.searchTypes.names.projectTitle,
            value:Config.searchTypes.values.projectTitle
        },{
            name:Config.searchTypes.names.term,
            value:Config.searchTypes.values.term
        }];
        $scope.type=$scope.types[0]["value"];
        $scope.keyword="";
        $scope.projects=[];
        $scope.mainFlags.extMenuActive=false;

        $scope.table= new ngTableParams({
            count:Config.perLoadCount,
            page:1,
            sorting: {
                name: 'asc'     // initial sorting
            },
            filter:{
                type:$scope.type,
                keyword:$scope.keyword
            }
        },{
            total:0,
            getData:function($defer,params){
                Project.resource.getManageProjects(params.url(), function(data) {

                    // update table params
                    params.total(data.total);

                    // set new data
                    $scope.projects=data.artifacts;
                    $defer.resolve($scope.projects);
                });
            }
        });

        $scope.tableSearch=function(){
            $scope.table.page(1);

            $scope.table.filter({
                type:$scope.type,
                keyword:$scope.keyword
            });

            //$scope.table.reload();//这个函数不会动态更改filter
        };

        $scope.deleteProject=function(projectId,index){
            if(confirm(Config.messages.deleteConfirm)){
                Project.resource.delete({projectId:projectId},function(data){
                    toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);
                    $scope.projects.splice(index,1);
                });
            }
        };

        $scope.toggleShowProject=function(projectId,index){
            Project.resource.toggleShowProject({projectId:projectId},{},function(data){
                $scope.projects[index]["artifact"]["visible"]=!$scope.projects[index]["artifact"]["visible"];
                toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);
            });
        };

    }]);

viewControllers.controller("commentsManage",['$scope',"toaster","ngTableParams","Comment","CFunctions","Config",
    function($scope,toaster,ngTableParams,Comment,CFunctions,Config){
        $scope.mainFlags.currentMenu="";

        $scope.types=[{
            name:Config.searchTypes.names.commentContent,
            value:Config.searchTypes.values.commentContent
        },{
            name:Config.searchTypes.names.fullName,
            value:Config.searchTypes.values.fullName
        },{
            name:Config.searchTypes.names.projectTitle,
            value:Config.searchTypes.values.projectTitle
        }];
        $scope.type=$scope.types[0]["value"];
        $scope.keyword="";

        $scope.comments=[];
        $scope.mainFlags.extMenuActive=false;

        $scope.table= new ngTableParams({
            count:Config.perLoadCount,
            page:1,
            sorting: {
                name: 'asc'     // initial sorting
            },
            filter:{
                type:$scope.type,
                keyword:$scope.keyword
            }
        },{
            total:0,
            getData:function($defer,params){
                Comment.query(params.url(), function(data) {
                    if(data.success){
                        // update table params
                        params.total(data.total);

                        // set new data
                        $scope.comments=data.comments;
                        $defer.resolve($scope.comments);
                        //$defer.resolve(data.comments);
                    }
                });
            }
        });

        $scope.tableSearch=function(){
            $scope.table.page(1);

            $scope.table.filter({
                type:$scope.type,
                keyword:$scope.keyword
            });

            //$scope.table.reload();//这个函数不会动态更改filter
        };

        $scope.deleteComment=function(id,projectId,index){

            if(confirm(Config.messages.deleteConfirm)){
                Comment.delete({projectId:projectId,commentId:id},function(data){
                    $scope.comments.splice(index,1);
                    toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);
                });
            }
        };

    }]);

viewControllers.controller("boxes",['$scope',"$interval","$routeParams","Config","Storage","Box",function($scope,$interval,$routeParams,Config,Storage,Box){

    var inter=null;
    //覆盖了super里面的，一定要分开写，不然无法覆盖（这样可以覆盖的原理是因为对象是地址类型）
    $scope.mainFlags.currentMenu=Config.mainMenu.box;
    $scope.mainFlags.extMenuActive=false;



    $scope.boxes=[];
    $scope.loadedData=false;
    $scope.filter={
        scope:"",
        keyword:""
    };

    if($routeParams.userId){
        $scope.filter.scope="me";
    }

    $scope.keyDownSearch=function(event){
        if(event.keyCode==13){
            $scope.loadBoxes();
        }
    };

    $scope.loadBoxes=function(){
        Storage.clearScrollData(Config.scrollScreenType.box);
        $interval.cancel(inter);//清除一下，因为这个面板不重新加载
        $scope.boxes=[];
        $scope.loadedData=false;
        Box.getBoxes($scope.filter.scope,$scope.filter.keyword).$promise.then(function(data){

            //console.log("In views");
            var count= 0,length=data.topics.length;
            inter=$interval(function(){
                if(count<length){
                    $scope.boxes.push(data.topics[count]);
                    count++;
                }else{
                    //如果没有数据了，清除掉interval
                    $interval.cancel(inter);
                }

                if(!$scope.loadedData){
                    $scope.loadedData=!$scope.loadedData;
                }
            },200);

        });
    };
    $scope.loadBoxes();

}]);

viewControllers.controller("boxDetail",['$scope',"$routeParams","Box","Storage","Config","CFunctions",
    function($scope,$routeParams,Box,Storage,Config,CFunctions){


    //覆盖了super里面的，一定要分开写，不然无法覆盖（这样可以覆盖的原理是因为对象是地址类型）
    $scope.boxId=$routeParams.boxId;
    $scope.mainFlags.currentMenu="";
    $scope.mainFlags.extMenuActive=false;


    Storage.clearScrollData(Config.scrollScreenType.boxDetail);

    $scope.box={};
    Box.resource.get({boxId:$scope.boxId},function(data){
        $scope.box=data.topic;
        $scope.box.user=data.user;
        Storage.loadedTopProjects=$scope.box.projects=data.artifacts;
        var length=$scope.box.projects.length;
        if(CFunctions.checkMobile()){
            for(var j= 0;j<length;j++){
                var fileInfo=CFunctions.getFilePathInfo($scope.box.projects[j]["artifact"]["profile_image"]);
                $scope.box.projects[j]["artifact"]["profile_image"]=
                    fileInfo["filePath"]+Config.imageScale.thumbSmall+fileInfo["ext"];
            }

        }else{
            for(var j= 0;j<length;j++){
                var fileInfo=CFunctions.getFilePathInfo($scope.box.projects[j]["artifact"]["profile_image"]);
                $scope.box.projects[j]["artifact"]["profile_image"]=
                    fileInfo["filePath"]+Config.imageScale.thumbMedium+fileInfo["ext"];
            }
        }
    });

    Storage.loadedProjects=$scope.projects=[];
    Box.getBoxProjects($scope.boxId).$promise.then(function(data){
        $scope.projects=$scope.projects.concat(data.artifacts);
    });
}]);

viewControllers.controller("boxUpdate",["$scope","$routeParams","toaster","CFunctions","Config","Box",
    function($scope,$routeParams,toaster,CFunctions,Config,Box){
        function addTag(tag){

            //indexOf是ECMAScript5的新方法
            if(tag!==""&&$scope.box.terms.indexOf(tag)===-1){
                $scope.box.terms.push(tag);
            }

            $scope.newTag="";
        }

        function initData($scope,id){
            Box.resource.get({boxId:id},{id:id},function(data){
                $scope.box.name=data.topic.name;
                $scope.box.artifact_count=data.topic.artifact_count;
                $scope.box.status=data.topic.status;
                $scope.box.terms=data.topic.terms;
                $scope.box.description=data.topic.description;
            });
        }

        $scope.mainFlags.currentMenu="";
        $scope.mainFlags.extMenuActive=false;
        $scope.newTag="";
        $scope.boxId=$routeParams.boxId;

        $scope.box={
            terms:[]
        };

        //修改的时候需要初始化数据
        if($scope.boxId){
            initData($scope,$scope.boxId);
        }

        $scope.deleteTag=function(index){
            $scope.box.terms.splice(index,1);
        };

        $scope.deleteBox=function(id){
            if(confirm(Config.messages.deleteConfirm)){
                Box.resource.remove({boxId:id},function(data){
                    toaster.pop("success",Config.messages.successTitle,Config.messages.optSuccRedirect,null,null);
                    CFunctions.timeoutRedirect(Config.urls.boxes,false,true);
                });
            }
        };

        $scope.keyDownAddTag=function($event,tag){
            if($event.which==13){
                addTag(tag);
            }
        };
        $scope.blurAddTag=function(tag){
            addTag(tag);
        };

        $scope.boxUpdateSubmit=function(){
            if($scope.box.name&&$scope.box.description&&$scope.box.terms.length!=0){
                if($scope.boxId){
                    Box.resource.save({boxId:$scope.boxId},$scope.box,function(data){
                        toaster.pop("success",Config.messages.successTitle,Config.messages.optSuccRedirect,null,null);
                    });
                }else{
                    Box.resource.add($scope.box,function(data){
                        toaster.pop("success",Config.messages.successTitle,Config.messages.optSuccRedirect,null,null);
                    });
                }
                CFunctions.timeoutRedirect("topics",false,true);
            }else{
                toaster.pop('error',Config.messages.errorTitle,Config.messages.boxUnComplete,null,null);
                return false;
            }
        };
}]);

viewControllers.controller("userHome",['$scope',"$routeParams","$interval","User","Storage","Config","CFunctions",
    function($scope,$routeParams,$interval,User,Storage,Config,CFunctions){

    //覆盖了super里面的，一定要分开写，不然无法覆盖（这样可以覆盖的原理是因为对象是地址类型）
    var userId=$routeParams.userId;

    $scope.mainFlags.currentMenu="";
    $scope.mainFlags.extMenuActive=false;
    $scope.closeProjectDetailPanel();

    Storage.clearScrollData(Config.scrollScreenType.userDetail);

    $scope.user={};
    $scope.user.id=userId;
    User.resource.get({userId:userId},function(data){
        $scope.user=data.user;
        $scope.user.artifact_count=data.artifact_count;
        $scope.user.honor_sum=data.honor_sum;
        Storage.loadedTopProjects=$scope.user.topProjects=data.artifacts;

        var length=$scope.user.topProjects.length;
        if(CFunctions.checkMobile()){
            for(var j= 0;j<length;j++){
                var fileInfo=CFunctions.getFilePathInfo($scope.user.topProjects[j]["artifact"]["profile_image"]);
                $scope.user.topProjects[j]["artifact"]["profile_image"]=
                    fileInfo["filePath"]+Config.imageScale.thumbSmall+fileInfo["ext"];
            }

        }else{
            for(var j= 0;j<length;j++){
                var fileInfo=CFunctions.getFilePathInfo($scope.user.topProjects[j]["artifact"]["profile_image"]);
                $scope.user.topProjects[j]["artifact"]["profile_image"]=
                    fileInfo["filePath"]+Config.imageScale.thumbMedium+fileInfo["ext"];
            }
        }
    });

    Storage.loadedProjects=$scope.projects=[];
    User.getUserProjects(userId).$promise.then(function(data){
        var count= 0,length=data.artifacts.length;
        var inter=$interval(function(){
            if(count<length){
                $scope.projects.push(data.artifacts[count]);
                count++;
            }else{
                $interval.cancel(inter);
            }
        },200);
    });

}]);

viewControllers.controller("usersManage",['$scope',"toaster","ngTableParams","User","Config",
    function($scope,toaster,ngTableParams,User,Config){

        $scope.mainFlags.currentMenu="";
        $scope.types=[{name:Config.searchTypes.names.fullName,value:Config.searchTypes.values.fullName}];

        $scope.type=$scope.types[0]["value"];
        $scope.keyword="";

        $scope.mainFlags.extMenuActive=false;
        $scope.users=[];

        $scope.table= new ngTableParams({
            count:Config.perLoadCount,
            page:1,
            filter:{
                keyword:$scope.keyword,
                type:$scope.type
            }
        },{
            total:0,
            getData:function($defer,params){
                User.resource.query(params.url(), function(data) {

                    // update table params
                    params.total(data.total);

                    // set new data
                    $scope.users=data.users;
                    $defer.resolve($scope.users);
                    //$defer.resolve(data.users);
                });
            }
        });

        $scope.tableSearch=function(){

            //如果不手动设置到第一页，那么会有两次请求
            $scope.table.page(1);

            $scope.table.filter({
                keyword:$scope.keyword,
                type:$scope.type
            });

            //$scope.table.reload();//这个函数不会动态更改filter
        };

        $scope.setUserRole=function(userId,role,index){
            User.resource.setUserRole({userId:userId},{role:role},function(data){
                toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);
                $scope.users[index]["user"]["roles"]=[role];
                //$scope.table.reload();
            });
        }


}]);

viewControllers.controller("searchResult",["$scope","$interval","$routeParams","Project","Config","Storage",
    function($scope,$interval,$routeParams,Project,Config,Storage){
        $scope.searchContent=$routeParams.content;

        $scope.mainFlags.currentMenu="";

        $scope.mainFlags.extMenuActive=false;

        Storage.clearScrollData(Config.scrollScreenType.searchResult);

        $scope.closePop(true);

        Storage.loadedProjects=$scope.projects=[];
        $scope.loadedData=false;
        Project.getSearchResult($scope.searchContent).$promise.then(function(data){
            var count= 0,length=data.artifacts.length;
            var inter=$interval(function(){
                if(count<length){
                    $scope.projects.push(data.artifacts[count]);
                    count++;
                }else{
                    $interval.cancel(inter);
                }
                if(!$scope.loadedData){
                    $scope.loadedData=!$scope.loadedData;
                }
            },200);
        });
}]);







