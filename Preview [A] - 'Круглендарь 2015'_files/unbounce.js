// Production and Integration environments request via AWS.
// Dev and Test pull directly from here.
window.ub = function() {

  var getVisitorIdFromCookie = function() {
    var cookies = document.cookie.split(';');
    var visitorId;
    for (var i=0; i < cookies.length; i++) {
      if (cookies[i] !== null &&
          cookies[i] !== undefined &&
          jQuery.trim(cookies[i]).match(/^ubvs=/i)) {
        visitorId = cookies[i].split('=')[1];
        break;
      }
    }
    return visitorId;
  };

  return {
    page: {
      id: '',
      variantId: '',
      visitorId: getVisitorIdFromCookie(),
      name: ''
    }
  };
}();
