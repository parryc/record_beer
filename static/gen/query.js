$(document).ready(function(){ var csrftoken=$('meta[name=csrf-token]').attr('content');var queryResults=Handlebars.templates['query-results'];$.ajaxSetup({beforeSend:function(xhr,settings){if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)&&!this.crossDomain){xhr.setRequestHeader("X-CSRFToken",csrftoken)}}});var detailify=function(evt){var detail=$('#beer-detail'),name=$(this).find('.name').text(),brewery=$(this).find('.brewery').text(),country=$(this).find('.country').text(),style=$(this).find('.style').text(),abv=$(this).attr('data-abv'),d_city=$(this).attr('data-city'),d_country=$(this).attr('data-country'),d_month=$(this).attr('data-month'),d_year=$(this).attr('data-year'),brew_with=$(this).attr('data-with'),brew_year=$(this).attr('data-brewyear')
detail.find('.name').text(name);detail.find('.brewery').text(brewery);detail.find('.country').text(country);detail.find('.style').text(style);detail.find('.name').text(name);detail.find('.abv').text(abv);detail.find('.drink-city').text(d_city);detail.find('.drink-country').text(d_country);detail.find('.drink-month').text(d_month);detail.find('.drink-year').text(d_year);}
var query=function(evt){var query=$('#query').val(),data={};data={'query':query,'user':1}
$('#query-results').text('Searching...');$.ajax({type:'POST',url:'/beers/query',data:JSON.stringify(data),contentType:'application/json;charset=UTF-8',success:function(results){if(results.no_hits){$('#query-results').text('Nothing to see here.');}
console.log(results)
$('#query-results').html(queryResults(results));$('.result').click(detailify);}});}
$('#query').on("input",$.debounce(query,500));});(function(){var template=Handlebars.template,templates=Handlebars.templates=Handlebars.templates||{};templates['query-results']=template({"1":function(depth0,helpers,partials,data){var helper,functionType="function",helperMissing=helpers.helperMissing,escapeExpression=this.escapeExpression;return"  <div class=\"result\" data-rating=\""
+escapeExpression(((helper=(helper=helpers.rating||(depth0!=null?depth0.rating:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"rating","hash":{},"data":data}):helper)))
+"\" \n                      data-country=\""
+escapeExpression(((helper=(helper=helpers.drink_country||(depth0!=null?depth0.drink_country:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"drink_country","hash":{},"data":data}):helper)))
+"\" \n                      data-city=\""
+escapeExpression(((helper=(helper=helpers.drink_city||(depth0!=null?depth0.drink_city:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"drink_city","hash":{},"data":data}):helper)))
+"\" \n                      data-abv=\""
+escapeExpression(((helper=(helper=helpers.abv||(depth0!=null?depth0.abv:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"abv","hash":{},"data":data}):helper)))
+"\" \n                      data-year=\""
+escapeExpression(((helpers.year||(depth0&&depth0.year)||helperMissing).call(depth0,(depth0!=null?depth0.drink_datetime:depth0),{"name":"year","hash":{},"data":data})))
+"\"\n                      data-month=\""
+escapeExpression(((helpers.month||(depth0&&depth0.month)||helperMissing).call(depth0,(depth0!=null?depth0.drink_datetime:depth0),{"name":"month","hash":{},"data":data})))
+"\"\n                      >\n    <span class=\"brewery\">"
+escapeExpression(((helper=(helper=helpers.brewery||(depth0!=null?depth0.brewery:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"brewery","hash":{},"data":data}):helper)))
+"</span>\n    <span class=\"name\">"
+escapeExpression(((helper=(helper=helpers.name||(depth0!=null?depth0.name:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"name","hash":{},"data":data}):helper)))
+"</span><br/>\n    <span class=\"beer-info\">\n      <span class=\"rating "
+escapeExpression(((helpers.calcRating||(depth0&&depth0.calcRating)||helperMissing).call(depth0,(depth0!=null?depth0.rating:depth0),{"name":"calcRating","hash":{},"data":data})))
+"\"></span> / <span class=\"style\">"
+escapeExpression(((helpers.style||(depth0&&depth0.style)||helperMissing).call(depth0,(depth0!=null?depth0.style:depth0),{"name":"style","hash":{},"data":data})))
+"</span> / <span class=\"country\">"
+escapeExpression(((helper=(helper=helpers.country||(depth0!=null?depth0.country:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"country","hash":{},"data":data}):helper)))
+"</span>\n    </span>\n  </div>\n";},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data){var stack1,buffer="\n";stack1=helpers.each.call(depth0,(depth0!=null?depth0.results:depth0),{"name":"each","hash":{},"fn":this.program(1,data),"inverse":this.noop,"data":data});if(stack1!=null){buffer+=stack1;}
return buffer;},"useData":true});})();