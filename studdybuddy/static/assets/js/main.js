$(document).ready(function() {

setTimeout(function(){
    $('.content').fadeOut('slow');
}, 3000);

// $(".desc").each (function () {
//   if ($(this).text().length > 200)
//     $(this).text($(this).text().substring(0,200) + '...');
// });
// label
    $('input').on('focusin', function () {
       $(this).closest('.textFile').find('label').addClass('activeLabel');
       $(this).closest('.textFile').find('.lineM').addClass('activeLine');
    });
    $('input').on('focusout', function () {
       if (!this.value) {
          $(this).closest('.textFile').find('label').removeClass('activeLabel');
          $(this).closest('.textFile').find('.lineM').removeClass('activeLine');
       }
   });
});
