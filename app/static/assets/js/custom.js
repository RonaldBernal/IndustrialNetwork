$('.special.cards .image').dimmer({
    on: 'hover'
});
$('.dropdown').dropdown({
    transition: 'drop',
    on: 'hover',
});
$('.modal').modal(
    'attach events', '#add_prod', 'show'
);
$('.message .close').on('click', function() {
    $(this).closest('.message').fadeOut();
});