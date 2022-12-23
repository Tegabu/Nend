
$(document).ready(function(){

  $('.active-sec').on('click', function(e){
       loadPage(`/${$(this).attr('data-option')}`,'#home-feed');
  });

});
function loadPage(endpoint_url,div){
  $.ajax({url: endpoint_url,success: (data)=>{
    $(div).html(data);
  }});
}


// Chat

// Get the modal
var modal = document.getElementById("popup");
var modal2 = document.getElementById("popup2");

// Get the button that opens the modal
var btn = document.getElementsByClassName("myBtn")[0];

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
  modal2.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
  modal2.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
    modal2.style.display = "none";
  }
}

$(document).ready(function() {
    $(".pop-action").on('click',function(){
      buttonOptions($(this).attr("button-option"))
    });
})
function buttonOptions(opt){
  switch(opt){
    case "Edit Profile":
      showPopUp("Loading...");

      $.post('/profile',{},(data)=>{
        alert("Hello world")
        updatePopUp(data);
        repositionPopUp()
      });
      break;

      case "Show Message":
        showPopUp("<h1>My Message</h1>");
        break
  }
}
function showPopUp(content){
  $(".profile-edit-bg").fadeIn('fast',()=>{
    $(".profile-edit").html(content)
    $(".profile-edit").fadeIn('fast',()=>{
      repositionPopUp();
      $(".profile-edit-bg").off();
      $(".profile-edit-bg").on('click',()=>closePopUp())
    });
  })
}
function closePopUp(){
  $(".profile-edit").fadeOut('fast',()=>{
    $(".profile-edit-bg").fadeOut('fast');
  })
}
function repositionPopUp(){
  $(".profile-edit").animate({top : (($(window).height()- $(".profile-edit").height())/2)+'px',
  left : (($(window).width()- $(".profile-edit").width())/2)+'px'})
}
function updatePopUp(data){
  $(".profile-edit").html(data);
}




