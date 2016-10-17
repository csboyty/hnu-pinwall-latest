/**
 * Created with JetBrains WebStorm.
 * User: ty
 * Date: 14-7-24
 * Time: 下午3:10
 * To change this template use File | Settings | File Templates.
 */
var directives=angular.module("directives",["services"]);
directives.directive('pwdCheck', function(){
    return {
        require: 'ngModel',
        link: function (scope, elem, attrs, ctrl) {
            var firstPassword = angular.element(document.getElementById(attrs.pwdCheck));
            elem.on('keyup', function () {
                scope.$apply(function () {
                    var v = elem.val()===firstPassword.val();
                    ctrl.$setValidity('noMatch', v);
                });
            });
            firstPassword.on('keyup', function () {
                scope.$apply(function () {
                    var v = elem.val()===firstPassword.val();
                    ctrl.$setValidity('noMatch', v);
                });
            });
        }
    }
});
directives.directive('preventEnterSubmit', function(){
    return {
        link: function (scope, elem, attrs) {
            elem.on("keydown",function(event){
                if(event.keyCode==13){
                    return false;
                }
            })
        }
    }
});
directives.directive("isEmail",function(){
    return {
        require:"ngModel",
        link:function(scope,elem,attrs,ctrl){
            elem.bind("keyup",function(){
                if(ctrl.$viewValue){
                    scope.$apply(function(){
                        var reg=/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*$/;

                        ctrl.$setValidity("emailExist",reg.test(ctrl.$viewValue));
                    });

                }else{
                    scope.$apply(function(){
                        ctrl.$setValidity("emailExist",true);
                    });
                }
            });
        }
    }
});
/**
 *支持embed
 */
directives.directive('embedSrc', ["$sce",function ($sce) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var current = element;
            scope.$watch(function() { return attrs.embedSrc; }, function () {
                var clone = element
                    .clone()
                    .attr('src', attrs.embedSrc);
                current.replaceWith(clone);
                current = clone;
            });
        }
    };
}]);
/**
 *重写required，不然ie里面页面一展示就提示错误,还是要配合required，不然submit的disable会失效
 */
directives.directive("ownRequired",function(){
    return {
        require:"ngModel",
        link:function(scope,elem,attrs,ctrl){
            elem.bind("keyup",function(){
                if(ctrl.$viewValue){
                    scope.$apply(function(){
                        ctrl.$setValidity("ownRequired",true);
                    });

                }else{
                    scope.$apply(function(){
                        ctrl.$setValidity("ownRequired",false);
                    });
                }
            });

            //console.log(ctrl);
        }
    }
});
directives.directive("emailExist",function($http){
    return {
        require:"ngModel",
        link:function(scope,elem,attrs,ctrl){
            elem.bind("keyup",function(){
                if(ctrl.$viewValue){
                    $http.get("email_exists",{
                        params:{email:ctrl.$viewValue},
                        transformRequest:function(data, headersGetter){
                            return JSON.stringify(data);
                        },
                        transformResponse:function(data, headersGetter){
                            return JSON.parse(data);
                        }
                    }).success(function(data,status,headers,config){
                            if(data.exist){
                                ctrl.$setValidity("emailExist",false);
                            }else{
                                ctrl.$setValidity("emailExist",true);
                            }
                        }).error(function(data,status,headers,config){
                            ctrl.$setValidity('emailExist', true);
                        });
                }else{
                    ctrl.$setValidity("emailExist",true);
                }
            });
        }
    }
});
directives.directive("drag",function(){
    return {
        link:function(scope,elem,attrs,ctrl){
            var targetOl=elem[0];
            var item=attrs.drag;
            var eleDrag = null;//被拖动的元素

            //console.log(elem[0]);
            //console.log(document.getElementById("mediaList"));

            targetOl.onselectstart=function(event){
                if(event.target.className.match(item)!==null){

                    event.preventDefault();
                    event.stopPropagation();
                }
            };
            targetOl.ondragstart=function(event){
                if(event.target.className.match(item)!==null){
                    event.dataTransfer.effectAllowed = "move";
                    event.dataTransfer.setData("text","移动中");
                    eleDrag = event.target||event.srcElement;

                    return true;
                }
            };
            targetOl.ondragend=function(event){
                if(event.target.className.match(item)!==null){
                    eleDrag=null;

                    event.preventDefault();
                    event.stopPropagation();
                }
            };

            //在元素中滑过
            targetOl.ondragover = function (event) {
                event.preventDefault();
                event.stopPropagation();
            };

            targetOl.ondrop=function(event){

                event.preventDefault();
                event.stopPropagation();
            };

            //ol作为最大的容器也要处理拖拽事件，当在li上滑动的时候放到li的前面，当在ol上滑动的时候放到ol的最后面
            targetOl.ondragenter = function (event) {
                var target=event.toElement||event.target;
                var targetParent=target.parentNode;
                if (target == targetOl) {
                    targetOl.appendChild(eleDrag);
                }else{
                    if(target.tagName=="LI"){
                        targetOl.insertBefore(eleDrag, target);
                    }else{
                        targetOl.insertBefore(eleDrag, targetParent);
                    }
                }

                event.preventDefault();
                event.stopPropagation();
            };
        }
    }
});
directives.directive("toggleLockBox",["toaster","Box","Config",function(toaster,Box,Config){
    return {
        link: function (scope, element, attrs, ctrl) {
            element.on('click', function (event) {
                var params=attrs.toggleLockBox.split(",");
                var targetStatus=params[1]==Config.boxStatus.open?Config.boxStatus.closed:Config.boxStatus.open;
                Box.resource.setBoxStatus({boxId:params[0]},{id:params[0],status:targetStatus},function(data){
                    if(params[2]){
                        scope.boxes[params[2]]["topic"]["status"]=targetStatus;
                    }else{
                        scope.box.status=targetStatus;
                    }
                    toaster.pop('success',Config.messages.successTitle,Config.messages.operationSuccess,null,null);
                });
            });
        }
    }
}]);
directives.directive('clickToHideModalPanel', function(){
    return {
        link: function (scope, element, attrs, ctrl) {
            element.on('click', function (event) {
                var target=event.target||event.srcElement;
                //判断是否隐藏侧边菜单
                if($(target).parents("#de_ext_nav").length==0 && !$(target).is("#de_ext_nav")){
                    scope.$apply(function(){
                        scope.mainFlags.extMenuActive="";
                    });
                }
            });
        }
    }
});
directives.directive("windowStateChange",["$window","CFunctions","LocationChanger","safeApply",
    function($window,CFunctions,LocationChanger,safeApply){
    return {
        link:function(scope,element,attrs){

            //$window是被element函数封装过的
            $window.addEventListener("popstate",function(event){
                scope.initPage(location.pathname);
                //safeApply();
                //LocationChanger.canReload();
            });
        }
    }
}]);
directives.directive("panOnMouseWheel",["$window","$document","$timeout","$interval","Config","Storage","Project",
    function($window,$document,$timeout,$interval,Config,Storage,Project){
    return {
        link:function(scope,element,attrs){
            var targetElement=element[0];
            var mousewheelEvt= document.onmousewheel !== undefined ? "mousewheel" : "DOMMouseScroll";
            var mousewheelHandler=function (evt) {                
                var left=0;
                evt = window.event || evt;
                if(evt.wheelDelta <0 || evt.detail>0){
                    left=targetElement.scrollLeft+500;
                }else{
                    left=targetElement.scrollLeft-500;
                }
                TweenMax.to(targetElement, 0.5, {scrollTo:{x:left}});

                //兼容ie
                if(evt.preventDefault){
                    evt.preventDefault();
                    evt.stopPropagation(); 
                }else{
                    evt.returnValue=false;
                    evt.cancelBubble = false;
                }
                //evt.preventDefault(); 
            };
            
            var scrollHandler=function(evt){
                if(Storage.scrollTimer){
                        $timeout.cancel(Storage.scrollTimer);
                        Storage.scrollTimer=null;
                }

                Storage.scrollTimer=$timeout(function(){
                    if(targetElement.scrollWidth-$window.innerWidth<=targetElement.scrollLeft&&
                        Storage.lastLoadedId!=Config.hasNoMoreFlag&&Storage.lastLoadedId!=0){
                        Project.getProjects().$promise.then(function(data){
                            var count= 0,length=data.artifacts.length;
                            var inter=$interval(function(){
                                if(count<length){
                                    scope.projects.push(data.artifacts[count]);
                                    count++;
                                }else{
                                    $interval.cancel(inter);
                                }
                            },200);
                        });
                    }
                },200);
            
            }
            
            targetElement.addEventListener(mousewheelEvt, mousewheelHandler);
            targetElement.addEventListener("scroll", scrollHandler);

            //释放内存
            scope.$on("$destroy",function( event ) {
                $timeout.cancel( Storage.scrollTimer);
                Storage.scrollTimer=null;
                angular.element($window).unbind("scroll");
            });
            
        }
    }
}]);
directives.directive("windowScroll",["$window","$document","$timeout","$interval","Config","Storage","Project","Box","User",
    function ($window,$document,$timeout,$interval,Config,Storage,Project,Box,User) {
        return {
            link: function(scope, element, attrs) {

                //由于在多个view里面有绑定，所以每次绑定前解除，不然会重复绑定,在scope销毁的时候解除
                //angular.element($window).unbind("scroll");
                angular.element($window).bind("scroll", function() {
                    if(Storage.scrollTimer){
                        $timeout.cancel(Storage.scrollTimer);
                        Storage.scrollTimer=null;
                    }
                    Storage.scrollTimer=$timeout(function(){
                        var scrollTop=0;
                        if($window.scrollY){
                            scrollTop=$window.scrollY;
                        }else{
                            scrollTop=document.documentElement.scrollTop;
                        }

                        if(Storage.currentScrollScreenType &&
                            $document[0].body.scrollHeight-$window.innerHeight<=scrollTop &&

                            Storage.lastLoadedId!=Config.hasNoMoreFlag&&Storage.lastLoadedId!=0&&scope.mainFlags.showMainWrapper&&
                            scope.popFlags.popTemplateUrl===""){

                            switch(Storage.currentScrollScreenType){
                                case Config.scrollScreenType.project:
                                    Project.getProjects().$promise.then(function(data){
                                        var count= 0,length=data.artifacts.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.projects.push(data.artifacts[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);
                                    });

                                    break;
                                case Config.scrollScreenType.box:
                                    Box.getBoxes(scope.filter.scope,scope.filter.keyword).$promise.then(function(data){
                                        var count= 0,length=data.topics.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.boxes.push(data.topics[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);

                                    });

                                    break;
                                case Config.scrollScreenType.boxDetail:
                                    Box.getBoxProjects(scope.boxId).$promise.then(function(data){
                                        var count= 0,length=data.artifacts.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.projects.push(data.artifacts[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);
                                    });

                                    break;
                                case Config.scrollScreenType.searchResult:
                                    Project.getSearchResult(scope.searchContent).$promise.then(function(data){
                                        var count= 0,length=data.artifacts.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.projects.push(data.artifacts[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);
                                    });

                                    break;
                                case Config.scrollScreenType.userDetail:
                                    User.getUserProjects(scope.user.id).$promise.then(function(data){
                                        var count= 0,length=data.artifacts.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.projects.push(data.artifacts[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);
                                    });
                                    break;
                            }
                        }
                    },200);

                });

                //释放内存
                scope.$on("$destroy",function( event ) {
                    $timeout.cancel( Storage.scrollTimer);
                    Storage.scrollTimer=null;
                    angular.element($window).unbind("scroll");
                });
            }
        }
}]);

directives.directive("watchHeight",["$window","$document","$interval","$timeout","Config","Storage","Project","Box","User",
    function($window,$document,$interval,$timeout,Config,Storage,Project,Box,User){
        return {
            link:function(scope,element,attrs){
                var watch=scope.$watch(function(){return element[0].scrollHeight;},function(newValue,oldValue){

                    //防止第一屏不出现滚动条xx
                    if(Storage.scrollTimer){
                        $timeout.cancel(Storage.scrollTimer);
                        Storage.scrollTimer=null;
                    }
                    Storage.scrollTimer=$timeout(function(){
                        if(newValue!==oldValue&&newValue>450&&$document[0].body.scrollHeight<=$window.innerHeight){
                            switch(Storage.currentScrollScreenType){
                                case Config.scrollScreenType.project:
                                    Project.getProjects().$promise.then(function(data){
                                        var count= 0,length=data.artifacts.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.projects.push(data.artifacts[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);
                                    });

                                    break;
                                case Config.scrollScreenType.box:
                                    Box.getBoxes(scope.filter.scope,scope.filter.keyword).$promise.then(function(data){
                                        var count= 0,length=data.topics.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.boxes.push(data.topics[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);

                                    });

                                    break;
                                case Config.scrollScreenType.boxDetail:
                                    Box.getBoxProjects(scope.boxId).$promise.then(function(data){
                                        var count= 0,length=data.artifacts.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.projects.push(data.artifacts[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);
                                    });

                                    break;
                                case Config.scrollScreenType.searchResult:
                                    Project.getSearchResult(scope.searchContent).$promise.then(function(data){
                                        var count= 0,length=data.artifacts.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.projects.push(data.artifacts[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);
                                    });

                                    break;
                                case Config.scrollScreenType.userDetail:
                                    User.getUserProjects(scope.user.id).$promise.then(function(data){
                                        var count= 0,length=data.artifacts.length;
                                        var inter=$interval(function(){
                                            if(count<length){
                                                scope.projects.push(data.artifacts[count]);
                                                count++;
                                            }else{
                                                $interval.cancel(inter);
                                            }
                                        },200);
                                    });
                                    break;
                            }
                        }else{
                            //执行一次，取消watch
                            if(newValue>450){
                                watch();
                            }
                        }
                    });
                });
            }
        }
    }]);
