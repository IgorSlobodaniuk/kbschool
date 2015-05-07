$(document).ready(function(){
var headermenu = $("#horizontal_menu");
var offset = headermenu.offset();
var left = offset.left;
var top = offset.top;
var width = $("#horizontal_menu").width();
var height = $("#horizontal_menu").height();

$(window).scroll(function(){
var scrollTop = $(window).scrollTop();
if (scrollTop > top) {

$('#horizontal_menu').css({
left:left+'px',
position:'fixed',
zIndex:'9888',
top:"0px",
width:width+"px"
});
} else {
$('#float_top').css({
width:'0px',
height:'0px'
});
$('#horizontal_menu').css({
position:'static',
});
}
});
});



