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
const TURN_MOTORS_ON = document.getElementById('go');



TURN_MOTORS_ON.addEventListener('click', e => go(e));


function go(e){
  //doing custom things with myVal

  //here I want to prevent default
  
  e.preventDefault();
  console.log("GO GO");
  window.location.href='forward';
}
