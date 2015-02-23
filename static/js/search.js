$(document).ready(function(){
  //CSRF setup from Flask-WTF docs
  var csrftoken = $('meta[name=csrf-token]').attr('content'); 

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
    }
  });


  $('.search').on("input",function(evt){
    var query = $('.search #brewery').val() + ' ' + $('.search #name').val()
        ,location = $(this).attr('action')
        ,method = $(this).attr('method')
        ,data = {'query':query}
        ,paused = false
        ;

    // strip the brewery name from the "name", also strip "brewery" "brewing" etc.
    if(query.length >= 5 && !paused) {
      paused = true;
      $.ajax({
        type: method,
        url: location,
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          console.log(result.name)
          console.log(result)
          console.log('here!!')
          $('#search-results').text(result.name);
          paused = false
        }
      });
    }
    console.log(data);
  });
});