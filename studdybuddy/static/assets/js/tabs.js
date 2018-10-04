$(document).ready(function() {
    //
    $('.tabs .tabsControl a').on('click', function(event) {
      var currentAttributeValue = $(this).attr('href');
      // Show/Hide Tabs
      $('.tabs ' + currentAttributeValue).show().siblings().hide();
      // Change/remove current tab to active
      $(this).parent('li').addClass('activeOpt').siblings().removeClass('activeOpt');
      event.preventDefault();
    });
});
