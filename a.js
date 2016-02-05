var asmjy = document.getElementById("rectPlyr_Playerlistodi");
var asdf = asmjy.getElementsByTagName("a");
var asdfext = ".html";
for(var asdfinc =0 ; asdfinc < asdf.length;asdfinc++){
  if(asdf[asdfinc].href.indexOf(asdfext)!=-1){
    console.log(asdf[asdfinc].href);
  }
}
