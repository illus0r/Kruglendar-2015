//VERSION 2.1
lp.jQuery(document).ready(function() {
  var regexBgImage = /\s*background-image\s*:\s*url\(\s*["']?([^"']+?)["']?\s*\)/g;
  var regexStart = /#lp-pom-button-\d+\s*\:\s*(hover|active)\s*{\s*/g;
  var regexEnd = /[}]/g;
  var urls = [];
  var start;
  var cssPiles = lp.jQuery('head style[title=page-styles]').html().split('\n');
  for(var j=0;j<cssPiles.length;j++){
    var cssLine = cssPiles[j];
    while(regexStart.exec(cssLine)){
      start='true';
    }
    if(start==='true'){
      while(matches =  regexBgImage.exec(cssLine)){
        var url = matches[1];
        if (lp.jQuery.inArray( url, urls ) === -1) urls.push(url);
      }
      while(regexEnd.exec(cssLine)){
        start = 'false';
      }
    }
  }
  for (var i=0,l=urls.length; i<l; i++) {
    window.document.createElement('img').src = urls[i];
  }
});
