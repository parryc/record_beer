Handlebars.registerHelper('calcRating', function(rating) {
  var parts = (""+rating).split('.');
  if(parts[1] === undefined)
    parts[1] = "0";
  parts[1] = Math.ceil(parts[1]);
  // if(parts[0] === "0")
  //   return "★";
  // if(parts[0] === "1")
  //   return "★★";
  // if(parts[0] === "2")
  //   return "★★★";
  // if(parts[0] === "3")
  //   return "★★★★";
  // if(parts[0] === "4")
  //   return "★★★★★";
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

Handlebars.registerHelper('year', function(date){
  return date.substring(0,4);
});

Handlebars.registerHelper('month', function(date){
  var months = "January_February_March_April_May_June_July_August_September_October_November_December".split("_");
  return months[parseInt(date.substring(5,7),10)-1];
});


Handlebars.registerHelper('isStrong', function(abv, options) {
  if(this.abv >= 7.0) {
    return options.fn(this);
  }
});


Handlebars.registerHelper('style', function(style){
  if(style === 'Fruit Beer/Radler')
    return 'Fruit Beer';
  if(style === 'Radler/Shandy')
    return 'Fruit Beer';
  if(style === 'Spice/Herb/Vegetable')
    return 'Spice';
  if(style === 'Abt/Quadrupel')
    return 'Quadrupel';
  if(style === 'Sour Red/Brown')
    return 'Flanders Sour';
  if(style === 'Session IPA')
    return 'IPA';
  if(style === 'Imperial/Strong Porter')
    return 'Imperial Porter';
  if(style === 'Grodziskie/Gose/Lichtenhainer')
    return 'Gose';
  if(style === 'India Pale Ale (IPA)')
    return 'IPA';
  if(style === 'Sour/Wild Ale')
    return 'Sour';
  if(style === 'Imperial/Double IPA' || style === 'Imperial IPA')
    return 'Double IPA';
  if(style === 'Strong Pale Lager/Imperial Pils' || style === 'Imperial Pils/Strong Pale Lager')
    return 'Imperial Pils';
  if(style === 'Dunkel/Tmavý')
    return 'Dunkel';
  if(style === 'German Hefeweizen')
    return 'Hefeweizen';
  if(style === 'Belgian White (Witbier)' || style === 'Witbier')
    return 'Belgian White';
  if(style === 'Golden Ale/Blond Ale')
    return 'Golden Ale';
  if(style === 'Lambic Style - Gueuze')
    return 'Gueuze';
  if(style === 'Czech Pilsner (Světlý)' || style == 'Czech Pilsner (Světloé)')
    return 'Pilsener';
  if(style === 'Oktoberfest/Märzen')
    return 'Oktoberfest';
  if(style === 'Dortmunder/Helles')
    return 'Dortmunder';
  if(style === 'Lambic Style - Fruit')
    return 'Lambic';
  if(style === 'Premium Bitter/ESB')
    return 'Premium Bitter'
  if(style === 'Amber Lager/Vienna')
    return 'Vienna'
  if(style === 'Zwickel/Keller/Landbier')
    return 'Zwickel'
  if(style === 'Sahti/Gotlandsdricke/Koduõlu')
    return 'Sahti'
  else
    return style;
});