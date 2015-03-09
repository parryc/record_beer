Handlebars.registerHelper('badge', function(rating) {
  var parts = (""+rating).split('.');
  if(parts[1] === undefined)
    parts[1] = "0";
  parts[1] = Math.ceil(parts[1]);
  if(parts[0] === "0")
    return "bad";
  if(parts[0] === "1")
    return "meh";
  if(parts[0] === "2")
    return "ok";
  if(parts[0] === "3")
    return "good";
  if(parts[0] === "4")
    return "great";
});

Handlebars.registerHelper('date', function(date){
  var months = "Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_");
  return months[parseInt(date.substring(5,7),10)-1]+", "+date.substring(0,4);
});

Handlebars.registerHelper('style', function(style){
  if(style === 'Fruit Beer/Radler')
    return 'Fruit Beer';
  else
    return style;
});