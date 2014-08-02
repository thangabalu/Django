$(document).ready(function(){
  
   $(".content_block_show_recipe").on("mousedown", ".editable_div", function(){
      $(this).empty();
   });  

});



function you_hovered(name,comment_id,recipe_type,recipe_title_url_format,commenter_name)
{
   //Getting commenter_name through id since passing it directly in javascript is causing "unterminated string literal"
   var real_div= document.getElementById(name)
   $('.textbox_button_div').hide();
   
    $(real_div).append(          // Create form append
        $("<form/>",{action:'/recipes/comments/reply/', method:'POST',name: 'form'}).append(
        //Replacing text area with editable div. Since autoexpanding is tough in that.
        $("<div/>",{class:"textbox_button_div"}).append(
        $("<div/>", {class:"editable_div", id:"editable_div_name_"+name, text:"Enter your name",contenteditable: "true", width:"325px",onkeypress: "return (this.innerText.length <= 50)" }).css("border","thin solid black"),
        $("<div />").css("margin-bottom","5px"), //br tag is not working. Using div tag for line space
        $("<div/>", {id:"editable_div_comment_"+name, text:"@"+commenter_name+":",contenteditable: "true", width:"325px",onkeypress: "return (this.innerText.length <= 256)" }).css("border","thin solid black"),        
        $("<div />").css("margin-bottom","5px"), //br tag is not working. Using div tag for line space
        $("<input/>", {type:'button', id:"mybutton_"+name, value:'Submit'}),
        $("<div />").css("margin-bottom","5px"), //br tag is not working. Using div tag for line space
        $("<input/>", {type:'hidden', name:'recipe_type', value:recipe_type}),
        $("<input/>", {type:'hidden', name:'comment_id', value:comment_id}),
        $("<input/>", {type:'hidden', name:'recipe_title_url_format', value:recipe_title_url_format})
        )
       )
     )   
 
   document.getElementById("mybutton_"+name).addEventListener("click", function () {
   var collect_name_from_div = $("#editable_div_name_"+name).text();
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