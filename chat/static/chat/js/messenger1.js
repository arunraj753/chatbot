for ( var i = 0; i < 3; i++ ) (function(i){ 
  buttons[i].onclick = function() {
    sendMessage(suggetions[i])
    console.log(suggetions[i])
  }
})(i);