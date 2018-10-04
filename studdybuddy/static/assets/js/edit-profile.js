$(document).ready(function() {

    $('.layerBg, .close').click(function(){
        $('.layerBg').fadeOut();
        $('.skillsList').removeClass('showSkills');
    });

    $('#teachingSkills').click(function(){
        $('.layerBg').fadeIn();
        $('.skillsList').addClass('showSkills');
    });

});
