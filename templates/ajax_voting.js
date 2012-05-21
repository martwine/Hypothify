$(function(){
  // if current viewport height is at least 70% of the previous
  if ($(document.body).height()>$.cookie('h2')*0.7)
    // retain previous scroll
    $('html,body').scrollTop($.cookie('h1'));
});
$(window).unload(function(){
  // store current scroll
  $.cookie('h1', $(window).scrollTop());
  // store current viewport height
  $.cookie('h2', $(document.body).height());
});
 
 	$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
