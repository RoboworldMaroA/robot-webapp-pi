// topPartDrivingController.addEventListener("submit", (e) => {
//   e.preventDefault();

//   // handle submit
// });


middlePartDrivingController.addEventListener('click', (e) => {
  e.preventDefault();

  // handle submit
});




bottomPartDrivingController.addEventListener('click', (e) => {
  e.preventDefault();

  // handle submit
});




// GO - RUN MOTORS FORWARD
// Variable used to get a value from the button with id=go
const TURN_MOTORS_ON = document.getElementById('go');

// wait for click and execute function go()
TURN_MOTORS_ON.addEventListener('click', e => go(e));

//Function go used to activate FLASK rout forrward and prevent refresh a page
function go(e){
  //doing custom things with myVal

  //here I want to prevent default
  
  e.preventDefault();
  console.log("GO GO");
  window.location.href='forward';
}



// RUN SERVO UP OR DOWN (CAMERA UP OR DOWN)
// Variable used to get a value from the button with id=go
const TURN_SERVO_ON = document.getElementById('move-horizontal-servo-up-or-down');

// wait for click and execute function go()
TURN_MOTORS_ON.addEventListener('click', e => moveHorizontalServoUpOrDown(e));

//Function go used to activate FLASK rout forrward and prevent refresh a page
function moveHorizontalServoUpOrDown(e){
  //doing custom things with myVal

  //here I want to prevent default
  
  e.preventDefault();
  console.log("Move camera up or down");
  window.location.href='move-horizonatal-servo-up-or-down';
}

