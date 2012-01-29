
/**
* Condense 0.1 - Condense and expand text heavy elements
*
* (c) 2008 Joseph Sillitoe
* Dual licensed under the MIT License (MIT-LICENSE) and GPL License,version 2 (GPL-LICENSE). 
*/
 
/*
* jQuery plugin
*
* usage:
*  
*   $(document).ready(function(){     
*     $('#example1').condense();
*   });
*
* Options:
*  condensedLength: Target length of condensed element. Default: 200  
*  minTrail: Minimun length of the trailing text. Default: 20
*  delim: Delimiter used for finding the break point. Default: " " - {space}
*  moreText: Text used for the more control. Default: [more]  
*  lessText: Text used for the less control. Default: [less]  
*  ellipsis: Text added to condensed element. Default:  ( ... )  
*  moreSpeed: Animation Speed for expanding. Default: "normal"  
*  lessSpeed: Animation Speed for condensing. Default: "normal"
*  easing: Easing algorith. Default: "linear"
*/
(function($){$.fn.condense=function(d){$.metadata?debug('metadata plugin detected'):debug('metadata plugin not present');var e=$.extend({},$.fn.condense.defaults,d);return this.each(function(){$this=$(this);var o=$.metadata?$.extend({},e,$this.metadata()):e;debug('Condensing ['+$this.text().length+']: '+$this.text());var a=cloneCondensed($this,o);if(a){$this.attr('id')?$this.attr('id','condensed_'+$this.attr('id')):false;var b=" <span class='condense_control condense_control_more' style='cursor:pointer;'>"+o.moreText+"</span>";var c=" <span class='condense_control condense_control_less' style='cursor:pointer;'>"+o.lessText+"</span>";if(o.inline){a.append(b)}else{a.append(o.ellipsis+b)}$this.after(a).hide().append(c);$('.condense_control_more',a).click(function(){debug('moreControl clicked.');triggerExpand($(this),o)});$('.condense_control_less',$this).click(function(){debug('lessControl clicked.');triggerCondense($(this),o)})}})};function cloneCondensed(a,b){if($.trim(a.text()).length<=b.condensedLength+b.minTrail){debug('element too short: skipping.');return false}var c=$.trim(a.html());var d=$.trim(a.text());var e=b.delim;var f=a.clone();var g=0;do{var h=findDelimiterLocation(c,b.delim,(b.condensedLength+g));if(b.inline){f.html($.trim(c.substring(0,(h+1)))+' '+b.ellipsis)}else{f.html($.trim(c.substring(0,(h+1))))}var i=f.text().length;var j=f.html().length;g=f.html().length-i;debug("condensing... [html-length:"+j+" text-length:"+i+" delta: "+g+" break-point: "+h+"]")}while(f.text().length<b.condensedLength)if((d.length-i)<b.minTrail){debug('not enough trailing text: skipping.');return false}debug('clone condensed. [text-length:'+i+']');return f}function findDelimiterLocation(a,b,c){var d=false;var e=c;do{var e=a.indexOf(b,e);if(e<0){debug("No delimiter found.");return a.length}d=true;while(isInsideTag(a,e)){e++;d=false}}while(!d)debug("Delimiter found in html at: "+e);return e}function isInsideTag(a,b){return(a.indexOf('>',b)<a.indexOf('<',b))}function triggerCondense(a,b){debug('Condense Trigger: '+a.html());var c=a.parent();var d=c.next();d.show();var e=d.width();var f=d.height();d.hide();var g=c.width();var h=c.height();c.animate({height:f,width:e,opacity:1},b.lessSpeed,b.easing,function(){c.height(h).width(g).hide();d.show()})}function triggerExpand(a,b){debug('Expand Trigger: '+a.html());var c=a.parent();var d=c.prev();d.show();var e=d.width();var f=d.height();d.width(c.width()+"px").height(c.height()+"px");c.hide();d.animate({height:f,width:e,opacity:1},b.moreSpeed,b.easing);if(c.attr('id')){var g=c.attr('id');c.attr('id','condensed_'+g);d.attr('id',g)}}function debug(a){if(window.console&&window.console.log){window.console.log(a)}};$.fn.condense.defaults={condensedLength:200,minTrail:20,delim:" ",moreText:"[more]",lessText:"[less]",ellipsis:" ( ... )",inline:true,moreSpeed:"normal",lessSpeed:"normal",easing:"linear",}})(jQuery);