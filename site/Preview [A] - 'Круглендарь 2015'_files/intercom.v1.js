(function(){
  var per_app_intercom_widget;

  function getAppId() {
    if (typeof window.intercomSettings !== 'undefined' &&
      typeof(window.intercomSettings.app_id) !== 'undefined') {
      return window.intercomSettings.app_id
    } else if (typeof window.analytics !== 'undefined' &&
      typeof window.analytics._integrations !== 'undefined' &&
      typeof analytics._integrations.Intercom !== 'undefined' &&
      typeof analytics._integrations.Intercom.options !== 'undefined' &&
      typeof analytics._integrations.Intercom.options.appId !== 'undefined') {
      return analytics._integrations.Intercom.options.appId;
    } else {
      return '';
    }
  }

  per_app_intercom_widget = 'https://widget.intercom.io/widget/' + getAppId();
  var script_tag = document.createElement('script');
  script_tag.type = 'text/javascript';
  script_tag.async = true;
  script_tag.src = per_app_intercom_widget;

  var existing_script = document.getElementsByTagName('script')[0];
  existing_script.parentNode.insertBefore(script_tag, existing_script);
})();
