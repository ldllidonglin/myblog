function addclick(){
   var f=document.getElementById("addcategory");
   f.style.display="block";
}
function blogsubmit(){
     var f=document.getElementById("blogform");
     f.action="/blog/edit/submitblog";
     f.submit();
}
function addcategorysubmit(){
     alert('aa');
     var f=document.getElementById("addcateform");
     f.action="/blog/edit/addcategory";
     f.submit();
}
   
