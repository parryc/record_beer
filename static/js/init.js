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
  if(style === 'Flavored - Fruit' || style === "Radler / Shandy")
    return 'Fruit Beer';
  if(style === 'Flavored - Pumpkin / Vegetables')
    return 'Spice';
  if(style === 'Quadrupel / Abt')
    return 'Quadrupel';
  if(style === 'Sour - Flanders Red / Bruin')
    return 'Flanders Sour';
  if(style === 'ISA - Session IPA')
    return 'IPA';
  if(style === 'Porter - Imperial' || style === 'Porter - Imperial Flavored')
    return 'Imperial Porter';
  if(style === 'Gose - Flavored')
    return 'Gose';
  if(style.includes('IPA') && !style.includes('IIPA'))
    return 'IPA';
  if(style.includes('IIPA'))
    return 'Double IPA';
  if(style === 'Sour / Wild Beer')
    return 'Sour';
  if(style === 'Pilsener - Imperial')
    return 'Imperial Pils';
  if(style === 'Dark Lager - Dunkel / Tmavý')
    return 'Dunkel';
  if(style === 'Weissbier - Hefeweizen')
    return 'Hefeweizen';
  if(style === 'Witbier / Belgian White Ale')
    return 'Belgian White';
  if(style === 'Blonde Ale / Golden Ale')
    return 'Golden Ale';
  if(style === 'Lambic - Gueuze')
    return 'Gueuze';
  if(style === 'Pilsener - Czech / Svetlý')
    return 'Pilsener';
  if(style === 'Märzen / Oktoberfest Bier')
    return 'Oktoberfest';
  if(style === 'Helles / Dortmunder Export')
    return 'Dortmunder';
  if(style === 'Lambic - Fruit')
    return 'Lambic';
  if(style === 'Bitter - Premium / Strong / ESB')
    return 'Premium Bitter'
  if(style === 'Amber Lager - Intl / Vienna')
    return 'Vienna'
  if(style === 'Zwickelbier/Kellerbier/Landbier')
    return 'Zwickel'
  if(style === 'Gotlandsdricke/ Koduõlu/ Sahti')
    return 'Sahti'
  if(style.includes('Stout') && !style.includes('Imperial'))
    return 'Stout'
  if(style.includes('Stout') && style.includes('Imperial'))
    return 'Imperial Stout'
  if(style === 'Kölsch / Kölsch-Style' || style === "Kรถlsch / Kรถlsch-Style")
    return 'Kölsch'
  if(style.includes('Pale Ale') && style.includes('APA'))
    return 'American Pale Ale'
  if(style.includes('Pale Ale') && style.includes('English'))
    return 'English Pale Ale'
  if(style.includes('Pale Ale'))
    return 'Pale Ale'
  if(style === "Scotch Ale / Wee Heavy")
    return "Scotch Ale"
  return style;
});