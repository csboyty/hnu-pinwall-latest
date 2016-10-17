/**
 * Created with JetBrains WebStorm.
 * User: ty
 * Date: 14-7-24
 * Time: 下午3:10
 * To change this template use File | Settings | File Templates.
 */
var filters=angular.module("filters",[]);
filters.filter("setMinLength", function(){
    return function(first, second){
        return first.replace("${value}",second);
    }
});
filters.filter("setMaxLength", function(){
    return function(first, second){
        return first.replace("${value}",second);
    }
});
filters.filter("getMinNumber", function(){
    return function(first, second){
        return Math.min(first,second);
    }
});
filters.filter("showActive", function(){
    return function(active){
        var string="激活";
        if(active===false){
            string="未激活";
        }

        return string;
    }
});
filters.filter("showRoles", function(){
    return function(roles){
        return roles.join(",");
    }
});
filters.filter("arrayHasElements",function(){
    return function(array,element){
        var result=false;
        var elements=element.split(",");
        var arrayLength=array.length,elementsLength=elements.length;
        for(var i=0;i<arrayLength;i++){
            for(var j=0;j<elementsLength;j++){
                if(array[i]==elements[j]){
                    result=true;
                    break;
                }
            }

            //跳出外层循环
            if(result===true){
                break;
            }
        }

        return result;
    }
});
