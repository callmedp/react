var tests = new Bloodhound({
  datumTokenizer: function(tests) {
      return Bloodhound.tokenizers.whitespace(tests.value);
  },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: "/api/get-test/?nopage=true&fl=id,category,title,slug&title=%QUERY&active=true&format=json",
    wildcard: '%QUERY',
    filter: function(responses) {
      return $.map(responses, function(response){
        return { 
          value: response.title,
          slug: response.slug
        };
      });
    } 
  }
});

// initialize the bloodhound suggestion engine
tests.initialize();

// instantiate the typeahead UI
$('#bloodhound .typeahead').typeahead(
  { hint: true,
    highlight: true,
    minLength: 1
  },
  {
  displayKey: 'value',
  source: tests.ttAdapter()
});

$('.typeahead').on('typeahead:selected', function(evt, item) {
 window.location = 'http://' + window.location.host +'/practice-tests/'+ item['slug'] +'-test/';
})

$('#bloodhound_submit').click(function() {
  api_url = "/api/get-test/?nopage=true&fl=id,category,title,slug&title="+$('#bloodhound_input').val()+"&active=true&format=json"
 $.ajax({url: api_url, success: function(result){
  if(result.length == 1){
    window.location = 'http://' + window.location.host +'/practice-tests/'+ result[0]['slug'] +'-test/';
  }
  else{
    $("#bloodhound_message").show();
  }
 }});
});

