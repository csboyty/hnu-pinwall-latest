/*greensock 配置*/
CSSPlugin.defaultTransformPerspective=1200;

/*定义动效*/
var animations=angular.module("animations",["ngAnimate"]);

animations.animation(".de_ext_nav",function(){
	return{
		addClass: function(element, className, done) {
			if(className=="de_ext_nav_active"){
				TweenMax.to(element,0.3,{x:-220,ease:Circ.easeOut,transformPerspective:0,onComplete:done})
			}
		},
		removeClass: function(element, className, done) {
			if(className=="de_ext_nav_active"){
				TweenMax.to(element,0.3,{x:0,ease:Circ.easeOut,transformPerspective:0,onComplete:done})
			}
		}
	}
});
animations.animation(".de_popout",function(){
	return{
		enter:function(element,done){
            //console.log(element);
			TweenMax.from(element,0.5,{z:90,opacity:0,ease:Circ.easeOut, onComplete:done});
		},
		leave:function(element,done){
			TweenMax.to(element,0.5,{z:90,opacity:0, ease:Circ.easeOut, onComplete:done})
		}
	}
});
animations.animation(".de_blackout",function(){
	return{
		addClass: function(element, className, done) {
			if(className=="ng-hide"){
				TweenMax.to(element,0.5,{opacity:0, ease:Circ.easeOut, onComplete:done})
			}
		},
		removeClass: function(element, className, done) {
			if(className=="ng-hide"){
                //console.log(element);
                //TweenMax.set(element,{opacity:0});
                TweenMax.to(element,0.5,{opacity:0.7, ease:Circ.easeOut, onComplete:done})

			}
		}
	}
});
/*animations.animation(".de_screen_project_detail",function(){
	return{
		enter:function(element,done){
            //console.log(element.scope());
			//重置de_project_detail位置到页面顶端
			window.scrollTo(0,0);
			var header=$(element).find(".de_project_header");
			var detail=$(element).find(".de_project_detail");
			TweenMax.from(element,0.4,{opacity:0,onComplete:done});
			TweenMax.from(header,0.3,{y:-100});
			TweenMax.from(detail,0.3,{y:100});
		}
	}
});*/
animations.animation(".de_loading",function(){
	return{
		addClass: function(element, className, done) {
			if(className=="ng-hide"){
				//延迟2s，避免闪烁
				TweenMax.to(element,0.5,{opacity:0, delay:2, ease:Circ.easeOut, onComplete:function(){
					//清理工作
					element.removeClass("ng-animate");
					done();
				}})
			}
		},
		removeClass: function(element, className, done) {
			if(className=="ng-hide"){
				TweenMax.killTweensOf(element);
				TweenMax.to(element,0.5,{opacity:1, ease:Circ.easeOut, onComplete:done})
			}
		}
	}
});