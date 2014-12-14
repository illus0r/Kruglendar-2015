// IE6+SSL fix courtesy of http://www.tribalogic.net/

;(function(window) {
  var document = window.document;
  var undefined; // make sure nobody redefines window or undefined on us
  Zenbox = {

    /*
        PUBLIC API

        Methods in the public API can be used as callbacks or as direct calls. As such,
        they will always reference "Zenbox" instead of "this." Each one is wrapped
        in a try/catch block to ensure that including Zenbox doesn't break the page.
    */

    /*
     *  Build and render the Zenbox tab and build the frame for the Zenbox overlay,
     *  but do not display it.
     *  @see Zenbox._settings for options
     *  @param {Object} options
     */
    init: function(options) {
      try {
        Zenbox._createTabElement();
        Zenbox._initOverlay();
        Zenbox.update(options);
      } catch(e) {}
    },

    /*
     * Change the Zenbox settings. Re-render tab and overlay as necessary.
     * @see Zenbox._settings for options
     * @param {Object} settings the new settings
     */
    update: function(settings) {
      try {
        var self = Zenbox;
        self._configure(settings);
        if (!self._settings.url) {
          console && console.warn && console.warn("Zendesk Dropbox must be configured with a URL.");
        } else {
          self._updateTab();
        }
      } catch(e) {}
    },

    /*
     *  Render the Zenbox. Alias for #show.
     *  @see #show
     */
    render: function(event) {
      return Zenbox.show(event);
    },

    /*
     *  Show the Zenbox. Aliased as #render.
     *  @params {Event} event the DOM event that caused the show; optional
     *  @return {false} false always, in case users want to bind it to an
     *                  onclick or other event and want to prevent default behavior.
     */
    show: function(event) {
      try {
        var self = Zenbox;
        self._render();
        var overlay = Zenbox._overlay();
        overlay.style.height = document.getElementById('zenbox_screen').style.height = self._getDocHeight() + 'px';
        document.getElementById('zenbox_main').style.top = self._getScrollOffsets().top + 50 + 'px';
        overlay.style.display = "block";
        return self._cancelEvent(event);
      } catch(e) {}
    },

    /*
     *  Hide the Zenbox.
      *  @params {Event} event the DOM event that caused the show; optional
      *  @return {false} false always, in case users want to bind it to an
      *                  onclick or other event and want to prevent default behavior.
      */
    hide: function (event){
      try {
        Zenbox._overlay().style.display = 'none';
        return Zenbox._cancelEvent(event);
      } catch(e) {}
    },

    /*
        PRIVATE API

        Methods in the private API should only be called by Zenbox itself. As such, they
        can refer to "this" instead of "Zenbox."
    */

    // @api private
    _settings: {
      dropboxID:      null, // required
      tabID:          "support",
      tabText:        "Support", // most browsers will use the tabID image rather than this text
      tabColor:       "#000000",

      // the remaining settings are optional and listed here so users of the library know what they can configure:
      assetHost:      "assets.zendesk.com",
      tabImageURL:    null,       // optional; overrides URL generated from tabID
      tabPosition:    'Left',     // or 'Right'
      hide_tab:       false,      // if true, don't display the tab after initialization
      loadingText:    " Loading&hellip;",
      closeText:      "Close",
      request_subject:      undefined,  // pre-populate the ticket submission form subject
      request_description:  undefined,  //  "     "      "     "      "        "   description
      requester_name:       undefined,  //  "     "      "     "      "        "   user name
      requester_email:      undefined   //  "     "      "     "      "        "   user email
    },

    // @api private
    _configure: function(options) {
      var prop;
      var self = this;
      for (prop in options) {
        if (options.hasOwnProperty(prop)) {
          self._settings[prop] = options[prop];
        }
      }
      self._prependSchemeIfNecessary('url');
      self._prependSchemeIfNecessary('assetHost');
    },

    _prependSchemeIfNecessary: function(urlProperty) {
      var url = this._settings[urlProperty];
      if (url && !(this._urlWithScheme.test(url))) {
        this._settings[urlProperty] = document.location.protocol + "//" + url;
      }
    },

    // @api private
    _cancelEvent: function(e) {
      var event = e || window.event || {};
      event.cancelBubble = true;
      event.returnValue = false;
      event.stopPropagation && event.stopPropagation();
      event.preventDefault && event.preventDefault();
      return false;
    },

    // @api private
    _urlWithScheme: /^([a-zA-Z]+:)?\/\//,

    // @api private
    _initOverlay: function() {
      var div = document.createElement('div');
      div.setAttribute('id', 'zenbox_overlay');
      div.style.display = 'none';
      div.innerHTML = '&nbsp;';
      document.body.appendChild(div);
    },

    // @api private
    _updateTab: function() {
      var tab = document.getElementById('zenbox_tab');
      if (this._settings.hide_tab) {
        tab.style.display = 'none';
      } else {
        this._setTabImage(tab);
        tab.setAttribute('title', this._settings.tabText);
        tab.setAttribute('class', 'ZenboxTab' + this._settings.tabPosition);
        tab.setAttribute('className', 'ZenboxTab' + this._settings.tabPosition); // IE, you suck
        tab.innerHTML = this._settings.tabText;
        tab.style.backgroundColor = this._settings.tabColor;
        tab.style.borderColor = this._settings.tabColor;
        tab.style.display = 'block';
      }
    },

    // @api private
    _setTabImage: function(tab) {
      var url = this._tabImageURL();
      var arVersion = window.navigator && window.navigator.appVersion.split("MSIE");
      var version = parseFloat(arVersion[1]);
      if ((version >= 5.5) && (version < 7) && (document.body.filters)) {
        tab.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + url + "', sizingMethod='crop')";
      } else {
        tab.style.backgroundImage = 'url(' + url + ')';
      }
    },

    // @api private
    _tabImageURL: function() {
      if (this._settings.tabImageURL) {
        return this._settings.tabImageURL;
      } else {
        var url = this._settings.assetHost + '/external/zenbox/images/tab_' + this._settings.tabID;
        if (this._settings.tabPosition === 'Right') {
          url += '_right';
        }
        url += '.png';
        return url;
      }
    },

    _createTabElement: function() {
      var tab = document.createElement('a');
      tab.setAttribute('id', 'zenbox_tab');
      tab.setAttribute('href', '#');
      tab.onclick = Zenbox.show;
      tab.style.display = 'none';
      document.body.appendChild(tab);
    },

    _getDocHeight: function(){
      return Math.max(
        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
      );
    },

    _getScrollOffsets: function(){
      var result = {};
      result.left = window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft;
      result.top = window.pageYOffset || document.documentElement.scrollTop  || document.body.scrollTop;
      return(result);
    },

    _overlay: function() {
      return document.getElementById('zenbox_overlay');
    },

    _render: function() {
      if (this.is_rendered) {
        return;
      }
      this.is_rendered = true;
      this._overlay().innerHTML = this._overlayContent();
      var iframe = document.getElementById('zenbox_iframe');
      if (iframe.attachEvent) { // IE
        iframe.attachEvent("onload", this._iFrameLoaded);
      } else if (iframe.addEventListener) { // Mozilla
        iframe.addEventListener("load", this._iFrameLoaded, false);
      }
    },

    _iFrameLoaded: function() {
      document.getElementById('overlay_loading').style.display = "none";
      document.getElementById('zenbox_iframe').style.display = "block";
    },

    _overlayContent: function() {
      return '<div id="zenbox_main">' +
          '<div id="overlay_header">' +
            '<span onclick="return Zenbox.hide();">' + this._settings.closeText + '</span>' +
          '</div>' +
          '<div id="overlay_loading">' +
            '<img src="' + this._settings.assetHost + '/images/medium_load.gif"/>' + this._settings.loadingText + '<br/>&nbsp;' +
          '</div>' +
          '<iframe src="' + this._iFrameURL() + '" id="zenbox_iframe" frameborder="0" scrolling="auto" allowTransparency="true" style="border:0;"></iframe>' +
        '</div>' +
        '<div id="zenbox_screen" onclick="return Zenbox.hide();" ></div>';
    },

    _iFrameURL: function() {
      var url = this._settings.url + "/account/dropboxes/" + this._settings.dropboxID + '?x=5';
      if (this._settings.request_subject)     { url += '&subject=' + this._settings.request_subject; }
      if (this._settings.request_description) { url += '&description=' + this._settings.request_description; }
      if (this._settings.requester_name)      { url += '&name=' + this._settings.requester_name; }
      if (this._settings.requester_email)     { url += '&email=' + this._settings.requester_email; }
      return url;
    }
  };

  if (window.zenbox_params) {
    Zenbox.init(window.zenbox_params);
  }

})(this.window || this);
