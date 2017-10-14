//var div = document.getElementById("dcontent");
//document.getElementById('Demo')
//div.perfectScrollbar();
$(document).ready(function(){
//Ps.initialize(container, {
  //wheelSpeed: 2,
  //wheelPropagation: true,
  //minScrollbarLength: 20
//});
    //$('#div_chatContainner').perfectScrollbar({
    $('#div_chatWrapper').perfectScrollbar({
    //$('#div_mainContainner').perfectScrollbar({
        wheelSpeed: 38,
        //wheelPropagation: true,
        //minScrollbarLength: 20
        //useBothWheelAxes: false
        suppressScrollX: true,
        //scrollXMarginOffset: 20
        scrollYMarginOffset : 20
    });
    //alert('ready');
});

function changeSize() {
    var width = parseInt($("#Width").val());
    var height = parseInt($("#Height").val());

    $("#Demo").width(width).height(height);

    // update scrollbars
    $('#Demo').perfectScrollbar('update');

    // or even with vanilla JS!
    //Ps.update(document.getElementById('Demo'));
}

//var el = document.querySelector('.container');

//Ps.initialize(el);
