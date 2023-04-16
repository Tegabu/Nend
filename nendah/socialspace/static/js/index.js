
$(document).ready(function(){

  $('.active-sec').on('click', function(e){
       loadPage(`/${$(this).attr('data-option')}`,'#home-feed');
  });

  $(`my`)

  $('.like-bi').off()
  $('.like-bi').on('click',(eve)=>{
    likePost(eve.target);
  })

});
function loadPage(endpoint_url,div){
  $.ajax({url: endpoint_url,success: (data)=>{
    $(div).html(data);
  }});
}
async function likePost(btn){
   let response = await fetch($(btn).attr('path-details'));
   let state=JSON.parse(await response.text());
   if(state.likedStatus==1){
   $(btn).prop('src','/static/images/redheart.png')
   $($(btn).parent().children()[1]).html(`${state.likes>0 ? state.likes : '+'} like`)
   }else{
    $(btn).prop('src','/static/images/like.png')
    $($(btn).parent().children()[1]).html(state.likes>0 ? `${state.likes} <span>like</span>` : '+<span>like</span>')
   }
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


// popup code set

$(document).ready(function(){
  
  $(`.uploadbtn`).click(function(){
    showPopUpWindow('Sell',"test hfhgfhcontent",()=>{},'300px');
  });

  $('.showpop').click(()=>{
    //alert('hello')
     showPopUpWindow('Upload File',$(".upload-content").html(),()=>{},'50%');
  });

  $('.showprod').click(()=>{
    //alert('hello')
     showPopUpWindow('Upload File',$(".product-desc").html(),()=>{},'50%');
  });

  $('.booking-pop').click(()=>{
    //alert('hello')
    showPopUpWindow('Upload File',$(".stay-booking").html(),()=>{},'50%');
  });
  
  $('.cart-btn').click(()=>{
    //alert('hello')
    showPopUpWindow('Upload File',$(".cart-cont").html(),()=>{},'50%');
  });

  $('.sell-prod').click(()=>{
    //alert('hello')
    showPopUpWindow('Upload File',$(".upload").html(),()=>{},'50%');
  });

  $('.edit-prof').click(()=>{
    //alert('hello')
    showPopUpWindow('Upload File',$(".edit-page").html(),()=>{},'50%');
  });

});

function showPopUpWindow(title, content, callback=()=>{}, width = "60%") {
  $(".top-bar").html(`<span>${title}<span><div class="closex">X</div>`);
  $(".closex").on("click", () => {
    $(".modal_content").fadeOut("fast", () => {
      $(".modal-alert").fadeOut("fast");
    });
  });

  document.querySelector(".modal_content").style.width = width;
  setTimeout(() => {
    $(".modal_inner_content").html(content);
    callback();
    document.querySelector(".modal_content").style.marginLeft = `${
      ($(window).width() - $(".modal_content").width()) / 2
    }px`;
    document.querySelector(".modal_content").style.marginTop = `${
      ($(window).height() - $(".modal_content").height()) / 2
    }px`;
  }, 100);

  document.querySelector(".modal-alert").style.display = "block";
  document.querySelector(".modal_content").style.display = "block";
}





