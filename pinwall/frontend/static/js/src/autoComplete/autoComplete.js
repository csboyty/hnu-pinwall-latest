/**
 * Created with JetBrains WebStorm.
 * User: ty
 * Date: 14-8-15
 * Time: 上午9:30
 * To change this template use File | Settings | File Templates.
 */
angular.module("autoComplete",[]).
    constant("autoCompleteConfig",{
        version:"1.0"
    }).
    factory("AutoComplete",["$http",function($http){
        return {
            selectedEvent:null,
            getResultUrl:"",
            resultFilter:null, //对后台来的数据进行组装
            autoComplete:function(param){
                this.getResultUrl=param.url;
                this.selectedEvent=param.selectedEvent;
                this.resultFilter=param.filter;
            },
            getResult:function(text){
                var me=this;
                if(me.getResultUrl){
                    return $http.get(me.getResultUrl,{
                        params:{
                            text:text
                        },
                        transformRequest:function(data, headersGetter){
                            return JSON.stringify(data);
                        },
                        transformResponse:function(data, headersGetter){
                            return JSON.parse(data);
                        }
                    }).then(function(res){
                        //console.log("1");
                        var results=[];
                        var data=res.data;
                        if(data.success){
                            if(me.resultFilter){
                                data=me.resultFilter(data);
                            }

                            results=data.items;
                        }

                        return results;
                    });
                }
            }
        }
    }]).
    controller("ctrl",["$scope","AutoComplete",function($scope,AutoComplete){
        $scope.showBlackOut();
        $scope.showResult=false;
        $scope.items=[];
        $scope.content="";
        $scope.currentItemIndex=0;

        $scope.setCurrent=function(index){
            $scope.currentItemIndex=index;
        };
        $scope.selectItem=function(content){
            $scope.content=content;
            $scope.items=[];
            AutoComplete.selectedEvent($scope.content);
        };
        $scope.keyDownEvent=function(event){
            if(event.keyCode==13&&$scope.content!=""){
                $scope.items=[];
                AutoComplete.selectedEvent($scope.content);
            }
        };
        $scope.keyUpEvent=function(){
            if($scope.content!=""&&$scope.content.length>=2){
                AutoComplete.getResult($scope.content).then(function(data){
                    //console.log("2");
                    $scope.items=data;
                });
            }
        }
    }]).
    directive("autoComplete",[function(){
        return {
            replace:true,
            templateUrl:"js/src/autoComplete/tpl.html",
            link:function($scope,element){

            }
        }
    }]);

