$(document).ready(function(){
  //CSRF setup from Flask-WTF docs
  var csrftoken = $('meta[name=csrf-token]').attr('content');
  var queryResults = Handlebars.templates['query-results'];

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
    }
  });

  var detailify = function(evt) {
    var detail    = $('#beer-detail')
       ,name      = $(this).find('.name').text()
       ,brewery   = $(this).find('.brewery').text()
       ,country   = $(this).find('.country').text()
       ,style     = $(this).find('.style').text()
       ,rating    = $(this).attr('data-rating')
       ,rating_txt= $(this).attr('data-rating-text')
       ,abv       = $(this).attr('data-abv')
       ,d_city    = $(this).attr('data-city')
       ,d_country = $(this).attr('data-country')
       ,d_month   = $(this).attr('data-month')
       ,d_year    = $(this).attr('data-year')
       ,beer_with = $(this).attr('data-beerwith')
       ,beer_year = $(this).attr('data-beeryear')
       ,tags      = []

    //reset rating-text
    detail.find('.rating-text').removeAttr("class").addClass("rating-text");

    detail.find('.name').text(name);
    detail.find('.brewery').text(brewery);
    detail.find('.country').text(country);
    detail.find('.style').text(style);
    detail.find('.name').text(name);
    detail.find('.abv').text(abv);
    detail.find('.rating').text(rating);
    detail.find('.rating-text').addClass(rating_txt);
    detail.find('.drink-city').text(d_city);
    detail.find('.drink-country').text(d_country);
    detail.find('.drink-month').text(d_month);
    detail.find('.drink-year').text(d_year);

    tag_node = detail.find('.tags');
    if(tags.length > 0) {
      for(tag in tags) {
        tag_node.append("<span class='tag'>"+tag+"</span>");
      }
      tag_node.show();
    } else {
      tag_node.hide();
    }

    beeryear_node = detail.find('.beer-year');
    if(beer_year) {
      beeryear_node.text(beer_year);
      beeryear_node.show();
    } else {
      beeryear_node.hide();
    }

    beerwith_node = detail.find('.beer-with');
    if(beer_with) {
     beerwith_node.text(beer_with);
     beerwith_node.show();
    } else {
     beerwith_node.hide();
    }
  }

  var query = function(evt) {
    var query = $('#query').val()
        ,data = {}
        ;

    data = {
      'query':query,
      'user':1
    }

    $('#query-results').text('Searching...');

    $.ajax({
      type: 'POST',
      url: '/beers/query',
      data: JSON.stringify(data),
      contentType: 'application/json;charset=UTF-8',
      success: function(results) {
        if(results.no_hits) { 
          $('#query-results').text('Nothing to see here.'); 
        }
        console.log(results)
        $('#query-results').html(queryResults(results));
        $('#results-count').text('Beers: ' + results.results.length);
        $('.result').click(detailify);
      }
    });
  }

  $('#query').on("input",$.debounce(query, 500));

});