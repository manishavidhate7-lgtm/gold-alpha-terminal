# 1. Economic Calendar के लिए:
components.html("""
<div class="tradingview-widget-container">
  <iframe src="https://sslecal2.forexprostools.com/?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=1,2,3&features=datepicker,timezone&countries=25,32,37,72,5&calType=day&lang=1" width="100%" height="400" frameborder="0"></iframe>
</div>
""", height=420)

# 2. Currency Strength Heatmap के लिए:
components.html("""
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>
  {
  "width": "100%",
  "height": 400,
  "currencies": ["EUR", "USD", "JPY", "GBP", "CHF", "AUD", "CAD", "NZD", "INR"],
  "isTransparent": false,
  "colorTheme": "light",
  "locale": "en"
  }
  </script>
</div>
""", height=420)
