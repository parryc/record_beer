$(document).ready(function(){
  //CSRF setup from Flask-WTF docs
  var csrftoken = $('meta[name=csrf-token]').attr('content');
  var searchResults = Handlebars.templates['search-results'];

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
    }
  });

  var updateForm = function() {
    var brewery = $(this).find('.brewery').text()
       ,name    = $(this).find('.name').text()
       ,abv     = $(this).find('.abv').text()
       ,style   = $(this).find('.style').text()
       ,country = $(this).find('.country').text()

    // $('form #brewery').val(brewery);
    // $('form #name').val(name);
    $('form #style').val(style);
    $('form #abv').val(abv);
    $('form #country').val(country);
    $('form #drink_country').val($('.default-country').val());
    $('form #drink_city').val($('.default-city').val());
    $('form #drink_datetime').val($('.default-date').val());
  }

  var search = function(evt) {
    console.log('here');
    var query = $('.search #brewery').val() + ' ' + $('.search #name').val()
        ,location = 'search'
        ,method = $(this).attr('method')
        ,data = {
          'query':query,
          'user' :1}
        ,paused = false
        ;

    $('#search-results').text('Searching...');

    $('#query-results').text('Checking for duplicates...');
    // strip the brewery name from the "name", also strip "brewery" "brewing" etc.
    $.ajax({
      type: 'POST',
      url: '/beers/search',
      data: JSON.stringify(data),
      contentType: 'application/json;charset=UTF-8',
      success: function(results) {
        if(results.no_hits) { 
          $('#search-results').text('Nothing to see here.'); 
        }
        if(results.rate_limited) {
          $('#search-results').text('Looks like you are rate limited.');
        }
        console.log(results)
        $('#search-results').html(searchResults(results));
        $('.result').on("click",updateForm);
      }
    });

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
        $('#query-results').html('<h4>Record.Beer</h4>');
        $('#query-results').append(searchResults(results));
      }
    });
    console.log(data);
  }


  $('#brewery, #name').on("input",$.debounce(search, 750));
  $('#defaults').click(updateForm);

});