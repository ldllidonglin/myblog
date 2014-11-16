function SelectCategory(cagname){ 
     alert(cagname);
     var select=document.getElementById("blogcateselect");
     for(var i=0;i<select.options.length;i++){
         if(select.options[i].value==cagname){
            select.options[i].selected="selected";
            alert(i);
          }
      }
}

