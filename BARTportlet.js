(function($) {   // $.widget takes 3 parameters
   //    1) lorenzCustom.<portletName> -  This is the namespace and name of your portlet,
   //                                     the "lorenzCustom" namespace is required. <portletName>
   //                                     can be whatever you wish.
   //    2) $.lorenzSuper.portlet - This tells $.widget to inherit the super class $.lorenzSuper.portlet
   //    3) Portlet implementation, with 3 required attributes: options (object), data (function), render (function)
   $.widget("lorenzCustom.BART", $.lorenzSuper.portlet, {
      options: {
         displayName: 'BART' // human readable name of portlet
      },

      //Required function, must return an array of data sources.  "Sources" can be either deferred promises
      //or static data sources: strings, numbers, functions that return something, objects, arrays, etc...
      data: function(){
         var output;
         $.ajax({
             'async': false,
             'type': "POST",
             'global': false,
             'dataType': 'json',
             'url': "https://api.bart.gov/api/etd.aspx?cmd=etd&orig=dubl&key=MW9S-E7SL-26DU-VV8V&json=y",
             'data': { 'request': "", 'target': 'arrange_url', 'method': 'method_target' },
             'success': function (response) {
                 output = response;
             }
         });
         var etd = output.root.station[0].etd[0].estimate
         var outArray = []
         etd.forEach(function(element) {
            outArray.push(element.minutes);
         });
         return [outArray]; },

      //The function that actually renders your portlet.  Most often you will be appending to
      //this.$wrapper with your html.
      render: function(times) {
 var html = "<h1 style='font-size: 20px;'>Trains departing Dublin BART station in:</h1><h2 style='font-size: 60px;'>"+ times.join(" minutes</h2><h2 style='font-size: 60px;'>") + " minutes</h2>";
         //var html = "<h1>Trains departing Dublin BART station in:\n</h1><h2>"+ times + "</h2>";
         this.$wrapper.append(html);
      }
   });
}(jQuery));

