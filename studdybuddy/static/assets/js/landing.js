$(document).ready(function(){

    window.sr = ScrollReveal({ duration: 800, delay : 300,  reset:true});

    sr.reveal('.laptop', { duration:700, delay : 600, easing : 'ease', origin: 'bottom', distance: '60px', });

    sr.reveal('.steps .col', 100);

    sr.reveal('.testimonial .col', { duration:600, delay : 600, easing : 'ease', origin: 'bottom', distance: '60px', });

});
