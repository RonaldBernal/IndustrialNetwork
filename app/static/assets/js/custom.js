$('.special.cards .image').dimmer({
 on: 'hover'
});
$('.dropdown').dropdown({
 //transition: 'drop',
 on: 'hover',
 action: 'hide'
});
$('.modal')
 .modal('attach events', '#add_prod', 'show')
;