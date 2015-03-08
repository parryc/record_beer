$(document).ready(function(){ var csrftoken=$('meta[name=csrf-token]').attr('content');var searchResults=Handlebars.templates['search-results'];$.ajaxSetup({beforeSend:function(xhr,settings){if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)&&!this.crossDomain){xhr.setRequestHeader("X-CSRFToken",csrftoken)}}});var updateForm=function(){console.log('beaches');var brewery=$(this).find('.brewery').text(),name=$(this).find('.name').text(),abv=$(this).find('.abv').text(),style=$(this).find('.style').text(),country=$(this).find('.country').text()
$('form #style').val(style);$('form #abv').val(abv);$('form #country').val(country);$('form #drink_country').val('USA');$('form #drink_city').val('Berkeley');$('form #drink_datetime').val('2015-01-01');}
var query=function(evt){console.log('here');var query=$('.search #brewery').val()+' '+$('.search #name').val(),location='search',method=$(this).attr('method'),data={'query':query},paused=false;$('#search-results').text('Searching...');$.ajax({type:'POST',url:'search',data:JSON.stringify(data),contentType:'application/json;charset=UTF-8',success:function(results){if(results.no_hits){$('#search-results').text('Nothing to see here.');}
console.log(results)
$('#search-results').html(searchResults(results));$('.result').on("click",updateForm);}});
console.log(data);}
$('#brewery, #name').on("input",$.debounce(query,500));});(function(){var template=Handlebars.template,templates=Handlebars.templates=Handlebars.templates||{};templates['search-results']=template({"1":function(depth0,helpers,partials,data){var helper,functionType="function",helperMissing=helpers.helperMissing,escapeExpression=this.escapeExpression;return"    <li class=\"result\">\n      <span class=\"brewery\">"
+escapeExpression(((helper=(helper=helpers.brewery||(depth0!=null?depth0.brewery:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"brewery","hash":{},"data":data}):helper)))
+"</span> <span class=\"name\">"
+escapeExpression(((helper=(helper=helpers.name||(depth0!=null?depth0.name:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"name","hash":{},"data":data}):helper)))
+"</span><br/>\n      <span class=\"abv\">"
+escapeExpression(((helper=(helper=helpers.abv||(depth0!=null?depth0.abv:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"abv","hash":{},"data":data}):helper)))
+"</span> <span class=\"style\">"
+escapeExpression(((helper=(helper=helpers.style||(depth0!=null?depth0.style:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"style","hash":{},"data":data}):helper)))
+"</span><br/>\n      <span class=\"country\">"
+escapeExpression(((helper=(helper=helpers.brewery_country||(depth0!=null?depth0.brewery_country:depth0))!=null?helper:helperMissing),(typeof helper===functionType?helper.call(depth0,{"name":"brewery_country","hash":{},"data":data}):helper)))
+"</span>\n    </li>\n";},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data){var stack1,buffer="<div id=\"search-results\">\n  <ol>\n";stack1=helpers.each.call(depth0,(depth0!=null?depth0.results:depth0),{"name":"each","hash":{},"fn":this.program(1,data),"inverse":this.noop,"data":data});if(stack1!=null){buffer+=stack1;}
return buffer+"  </ol>\n</div>";},"useData":true});})();