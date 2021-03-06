$(document).ready(function(){
   //Menu bar - If "menu" is clicked, menu bar will be displayed. If clicked again, it will be disappeared
   $('span.navmenu_button').click(function () {
       $('div.navmenu').toggle();

   })

   $(window).resize(function () {
       if ( $(window).width() > 510 ) {
           $('div.navmenu').show();
       }
   })


   //When mouse key is down on the editable name div, it empties the content
   $(".content_block_show_recipe").on("mousedown", ".editable_div", function(){
      var input = $(this).text();
      if (input == "Enter your name") {
         $(this).empty();
      }
   });  

   //When mouse key leaves the editable name div, it fills the content back
   $(".content_block_show_recipe").on("mouseleave", ".editable_div", function(){
      if ($(this).is(':empty'))
      {
         $(this).text('Enter your name')
      }
   });
   // The below is if user has cleared the existing "Enter your name" and pressed
   // the tab button, it will again write "Enter your name"
   $(".content_block_show_recipe").on("focusout", ".editable_div", function(){
      if ($(this).is(':empty'))
      {
         $(this).text('Enter your name')
      }
   });

   
   $("#search").keyup(function(){

      $.ajax({
         type:"POST",
         url : "/search_titles/",
         data:{
               'search_text' : $('#search').val(),
               'csrfmiddlewaretoken' :$("input[name=csrfmiddlewaretoken]").val()
         },
         success: searchSuccess,
         dataType: 'html'
         
      });
           
   });
   // use window.location.href = "file2.html" to open on same window.
   //$("#searchbar_top_page").keydown(function(){
   //   window.open("/search/")
   //});

   $("#searchbar_top_page").mousedown(function(){
      window.open("/search/")
   });


   $("#send_button").click(function(event){
      $name   = $('#name').val(),
      $subject= $('#subject').val(),
      $email  = $('#email').val(),
      $message= $('#message').val()
      
      if ($name == null || $name == "" || $email == null || $email == "" || $subject == null || $subject == "" || $message == null || $message == "") {
        alert("Fields cannot be empty")
      }
      else{
         $.ajax({
            type:"POST",
            url : "/contact_submit/",
            async : false,
            data:{
               'name' : $('#name').val(),
               'subject' : $('#subject').val(),
               'email' : $('#email').val(),
               'message' : $('#message').val(),
               'csrfmiddlewaretoken' :$("input[name=csrfmiddlewaretoken]").val()
            },
            success: questionSuccess
         });
      }
      }); 
   
});

function questionSuccess(data,textStatus,jqXHR) {   
   $("#name").val("");
   $("#subject").val("");
   $("#email").val("");
   $("#message").val("");
   alert("Thanks for your message. We will reply as soon as possible")
}


function searchSuccess(data,textStatus,jqXHR) {
   $("#search_results").html(data);
}

//Thank you comment for comment and reply comment.
function thank_you() {
   alert("Thank you for the comment")
   return true
}


function you_hovered(name,comment_id,recipe_type,recipe_title_url_format,commenter_name)
{
   //Getting commenter_name through id since passing it directly in javascript is causing "unterminated string literal"
   var real_div= document.getElementById(name)
   $('.textbox_button_div').hide();
   
    $(real_div).append(          // Create form append
        $("<form/>",{action:'/recipes/comments/reply/', method:'POST',name: 'form'}).append(
        //Replacing text area with editable div. Since autoexpanding is tough in that.
        $("<div/>",{class:"textbox_button_div"}).append(
        $("<div />").css("margin-bottom","10px"), //br tag is not working. Using div tag for line space
        $("<span/>").text("You are replying to the above comment"),
        $("<div/>", {class:"editable_div", id:"editable_div_name_"+name, text:"Enter your name",contenteditable: "true", width:"325px",onkeypress: "return (this.innerText.length <= 50)" }).css("border","thin solid black"),
        $("<div />").css("margin-bottom","5px"), //br tag is not working. Using div tag for line space
        $("<div/>", {id:"editable_div_comment_"+name, text:"@"+commenter_name+":",contenteditable: "true", width:"325px",onkeypress: "return (this.innerText.length <= 256)" }).css("border","thin solid black"),        
        //$("<div />").css("margin-bottom","5px"), //br tag is not working. Using div tag for line space
        $("<input/>", {type:'button', id:"mybutton_"+name, value:'Submit'}),
        //$("<div />").css("margin-bottom","5px"), //br tag is not working. Using div tag for line space
        $("<input/>", {type:'hidden', name:'recipe_type', value:recipe_type}),
        $("<input/>", {type:'hidden', name:'comment_id', value:comment_id}),
        $("<input/>", {type:'hidden', name:'recipe_title_url_format', value:recipe_title_url_format})
        )
       )
     )   
 
   document.getElementById("mybutton_"+name).addEventListener("click", function () {
   var collect_name_from_div = $("#editable_div_name_"+name).text();
   // The below loop is done to clean up the textarea if the user has not typed name.Otherwise "Enter your name" will go to database
   if (collect_name_from_div == "Enter your name") {
      collect_name_from_div =""
   }
   var collect_comment_from_div = $("#editable_div_comment_"+name).text();

   $("form").append(
   $("<input/>", {type:'hidden', name:'name', value:collect_name_from_div}),
   $("<input/>", {type:'hidden', name:'comment', value:collect_comment_from_div})
   )
   $("form").submit();
   });   
   $(".reply_button").prop('disabled',false);
   //$('.enableOnInput').prop('disabled', true);
   document.getElementsByName(name)[0].disabled = true;
}
