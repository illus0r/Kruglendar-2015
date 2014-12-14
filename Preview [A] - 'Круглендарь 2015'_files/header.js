function loadAsync(u){
  setTimeout(function(){
    var d = document, f = d.getElementsByTagName('script')[0],
    s = d.createElement('script');
    s.type = 'text/javascript'; s.async = true; s.src = u;
    f.parentNode.insertBefore(s, f);
  }, 1);
}

jQuery(function() {

  //---------------------------------------------------------------------------
  // Dropdown menus (cogs, header: context-switching, account/user dropdown menu).
  //
  jQuery('.dropdown-toggle').dropdown();

});
