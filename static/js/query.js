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

  var hideDetails = function() {
    $('#results-column').removeClass('mobile-results');
    $('#detail-column').removeClass('mobile-detail').hide();
    $('.search').show();
    history.pushState('', document.title, window.location.pathname);
  }

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
       ,brew_with = $(this).attr('data-brewwith')
       ,brew_year = $(this).attr('data-brewyear')
       ,tags      = $(this).attr('data-tags')

    $('#start').hide();

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

    tag_list_node = detail.find('.tags-list');
    tag_node      = detail.find('.tags');
    if(tags !== undefined && tags.length > 0) {
      tags = tags.split(',');
      tag_list_node.html("");
      tags.forEach(function(tag){
        tag_list_node.append("<span class='tag'>"+tag+"</span>");
      });
      tag_node.removeClass('hidden').show();
    } else {
      tag_node.hide();
    }

    brewyear_node = detail.find('.brew-year');
    if(brew_year) {
      brewyear_node.text(brew_year);
      brewyear_node.removeClass('hidden').show();
    } else {
      brewyear_node.hide();
    }

    brewwith_node = detail.find('.brew-with');
    if(brew_with) {
     brewwith_node.text(brew_with);
     brewwith_node.removeClass('hidden').show();
    } else {
     brewwith_node.hide();
    }


    //Check mobile version
    if($('#mobilizer').css('display') === 'block') {
      $('#detail-column').show().addClass('mobile-detail');
      // $('#results-column').attr('data-scroll',$('body').scrollTop());
      $('#results-column').addClass('mobile-results');
      // $('#results-column').hide();
      $('#detail-back').show();
      $('.search').hide();

      window.location.hash = new Date().getTime();
      window.onhashchange = function() {
        if (!location.hash){
          hideDetails();
        }
      }
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
        $('#search-results-header').text('Search Results');
        $('.result').click(detailify);
      }
    });
  }

  $('#query').on("input",$.debounce(query, 500));
  $('#detail-back').click(hideDetails);
  $('.result').click(detailify);

});