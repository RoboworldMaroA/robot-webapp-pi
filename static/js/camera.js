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



// ******* RUN SERVO UP OR DOWN (CAMERA UP OR DOWN) *********************


//MOVE CAMERA DOWN
// Variable used to get a value from the button 
const MOVE_SERVO_HOME = document.getElementById('move-horizontal-servo-home');

// wait for click and execute function moveHorizontalServoUporDwon()
MOVE_SERVO_HOME.addEventListener('click', e => moveHorizontalServoHome(e));

//Function go used to activate FLASK rout forrward and prevent refresh a page
function moveHorizontalServoHome(e){
  
  e.preventDefault();
  console.log("Move camera home");
  window.location.href='move-horizontal-servo-home';
}




//MOVE CAMERA UP
// Variable used to get a value from the button 
const TURN_SERVO_ON = document.getElementById('move-horizontal-servo-up');

// wait for click and execute function moveHorizontalServoUporDwon()
TURN_SERVO_ON.addEventListener('click', event => moveHorizontalServoUp(event));

//Function go used to activate FLASK rout forrward and prevent refresh a page
function moveHorizontalServoUp(e){
  //here I want to prevent default  
  e.preventDefault();
  console.log("Move camera up or down");
  window.location.href='move-horizontal-servo-up';
}


//MOVE CAMERA DOWN
// Variable used to get a value from the button 
const MOVE_SERVO_DOWN = document.getElementById('move-horizontal-servo-down');

// wait for click and execute function moveHorizontalServoUporDwon()
MOVE_SERVO_DOWN.addEventListener('click', e => moveHorizontalServoDown(e));

//Function go used to activate FLASK rout forrward and prevent refresh a page
function moveHorizontalServoDown(e){
  
  e.preventDefault();
  console.log("Move camera down");
  window.location.href='move-horizontal-servo-down';
}


//MOVE CAMERA LEFT
// Variable used to get a value from the button 
const MOVE_SERVO_LEFT = document.getElementById('move-vertical-servo-left');

// wait for click and execute function moveHorizontalServoUporDwon()
MOVE_SERVO_LEFT.addEventListener('click', e => moveVerticalServoLeft(e));

//Function go used to activate FLASK rout forrward and prevent refresh a page
function moveVerticalServoLeft(e){
  
  e.preventDefault();
  console.log("Move camera left");
  // Triger route at the backend on this address
  window.location.href='move-vertical-servo-left';
}

//MOVE CAMERA RIGHT
// Variable used to get a value from the button 
const MOVE_SERVO_RIGHT = document.getElementById('move-vertical-servo-right');

// wait for click and execute function 
MOVE_SERVO_RIGHT.addEventListener('click', e => moveVerticalServoRight(e));

//Function go used to activate FLASK rout forrward and prevent refresh a page
function moveVerticalServoRight(e){
  
  e.preventDefault();
  console.log("Move camera right");
  // Triger route at the backend on this address
  window.location.href='move-vertical-servo-right';
}


//MEASURE DISTANCE USING SONAR
// Variable used to get a value from the button 
const MEASURE_DISTANCE_USING_SONAR = document.getElementById('measure-distance-sonar');

// wait for click and execute function 
MEASURE_DISTANCE_USING_SONAR.addEventListener('click', e => measureDistanceUsingSonar(e));

//Function go used to activate FLASK rout forrward and prevent refresh a page
function measureDistanceUsingSonar(e){
  
  e.preventDefault();
  console.log("Measuring distance");
  // Triger route at the backend on this address
  window.location.href='measure-distance-sonar';
}

//Read data from flask



