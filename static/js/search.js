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
    console.log('beaches');
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
    $('form #drink_country').val('USA');
    $('form #drink_city').val('Berkeley');
    $('form #drink_datetime').val('2015-01-01');
  }

  var query = function(evt) {
    console.log('here');
    var query = $('.search #brewery').val() + ' ' + $('.search #name').val()
        ,location = 'search'
        ,method = $(this).attr('method')
        ,data = {'query':query}
        ,paused = false
        ;

    $('#search-results').text('Searching...');
    // strip the brewery name from the "name", also strip "brewery" "brewing" etc.
    $.ajax({
      type: 'POST',
      url: 'search',
      data: JSON.stringify(data),
      contentType: 'application/json;charset=UTF-8',
      success: function(results) {
        if(results.no_hits) { 
          $('#search-results').text('Nothing to see here.'); 
        }
        console.log(results)
        $('#search-results').html(searchResults(results));
        $('.result').on("click",updateForm);
      }
    });

    // $.ajax({
    //   type: 'POST',
    //   url: 'duplicate',
    //   data: JSON.stringify(data),
    //   contentType: 'application/json;charset=UTF-8',
    //   success: function(results) {
    //     if(results.no_hits) { 
    //       $('#search-results').text('Nothing to see here.'); 
    //     }
    //     console.log(results)
    //     $('#search-results').append('<h3>Duplicates</h3>');
    //     $('#search-results').append(searchResults(results));
    //     $('.result').on("click",updateForm);
    //   }
    // });
    console.log(data);
  }


  $('#brewery, #name').on("input",$.debounce(query, 500));

});