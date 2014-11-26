$(document).ready(function(){
      $(".manbtnlink").click(function(e){ $(this).css({"background-color":"#D9D9D9"});});
});
function CategoryEdit(id){
    var categoryname=$("#"+id).text();
    var appendHTML="<input value='"+categoryname+"'></input><a id='"+id+"' href='#' onclick='SaveEdit(this)'>保存</a>";
    if(categoryname!="保存"){
   	 $("#"+id).html(appendHTML);
    }
}

function SaveEdit(dome){
   var oldcategoryname=dome.id;
   var newcategoryname=$("#"+dome.id+" input")[0].value;
   var localurl=window.location.href.slice(-15,-1)+"/edit";
   $.ajax({
    type:'POST',
    url:localurl,
    data:{oldname:oldcategoryname,newname:newcategoryname},
    success:function(data){
     alert("Data Loaded:成功");
    },
    error:function(error){
     alert(error.response);
    }
  });
}
