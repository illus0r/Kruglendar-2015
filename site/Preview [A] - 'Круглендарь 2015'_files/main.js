// version 3.0

lp = lp || {};
lp.text = {
  heightErrorAllowance: 16,
  getTextElementMetrics: function() {
    var metrics = {};
    this.textElements.each(function(i, e) {
      metrics[e.id] = {
        designHeight: parseInt(lp.jQuery('#'+e.id).css('height'), 10)
      };
    });
    return metrics;
  },

  adjustTextHeight: function(e, designHeight) {
    var adjust = 1;
    var maxAdjust = 50;
    var w = parseInt(lp.jQuery('#'+e.id).css('width'), 10);

    while ((lp.jQuery(e)[0].offsetHeight - this.heightErrorAllowance) > designHeight && adjust <= maxAdjust) {
      lp.jQuery(e)[0].style.width = (w + adjust) + 'px';
      adjust++;
    }
  },

  fixIELastChildIssue: function() {
     var browser = lp.jQuery.browser;

     if(browser.msie && parseFloat(browser.version) <= 8.0 ) {
       lp.jQuery("div.lp-pom-root .lp-pom-text>p:last-child").css('margin-bottom', '0px');
     }
  },

  isMobileEnabled: function() {
    var mobileStyles = lp.jQuery('style[data-page-type=main_mobile], style[data-page-type=form_confirmation_mobile]');
    return mobileStyles.length > 0;
  },

  isMobileViewport: function() {
    var mediaQuery ='screen and (max-width: 600px)';
    return window.matchMedia(mediaQuery).matches;
  },

  fixTextHeights: function() {
    if( this.isMobileEnabled() && this.isMobileViewport() ){
      return;
    }
    this.textElements = this.textElements || lp.jQuery(".lp-pom-text");
    this.textElementMetrics = this.textElementMetrics || this.getTextElementMetrics();

    var debug = '';
    var self = this;

    this.textElements.each(function(i, e) {
      e.style.height = 'auto';
      var designHeight = self.textElementMetrics[e.id].designHeight;
      debug += e.id + ':  '+designHeight+' '+e.offsetHeight+'\n';

      if ((e.offsetHeight - self.heightErrorAllowance) > designHeight) {
        self.adjustTextHeight(e, designHeight);
      }
    });

    this.fixIELastChildIssue();
  }
};

lp.jQuery(document).ready(function() {
  if(!(lp && lp.webFontLoad)) {
    lp.text.fixTextHeights();
  }
});
