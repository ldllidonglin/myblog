$(document).ready(function(){
      $("#userlogined").mouseover(function(e){
           $("#logindiv").css({"display":"block"});});
      $("#logindiv").mouseleave(function(e){
           $("#logindiv").css({"display":"none","background":"white"});
           $("this").css({"background":"white"});
      });

      $('#logindiv a').mouseover(function(e){
           $(this).css({'background':"rgb(190,190,190)"});});
      
      $("#logindiv a").mouseleave(function(e){
           $("#logindiv a").css({"background":"rgb(255,255,255"});});
      
});
