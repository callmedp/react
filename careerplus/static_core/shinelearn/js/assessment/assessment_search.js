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

var test_fa = new Bloodhound({
  datumTokenizer: function(test_fa) {
      return Bloodhound.tokenizers.whitespace(test_fa.value);
  },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: "/api/get-category-level-products/?nopage=true&fl=id,title,slug&title=%QUERY&format=json",
    wildcard: '%QUERY',
    filter: function(responses) {
      return $.map(responses, function(response){
        return { 
          title: response.title,
          slug: response.slug
        };
      });
    } 
  }
});

// initialize the bloodhound suggestion engine
tests.initialize();
test_fa.initialize();

// instantiate the typeahead UI
$('#bloodhound .typeahead').typeahead(
  { 
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'practice_test',
    source: tests.ttAdapter(),
    displayKey: 'value',
    limit: 4,
    templates: {
        header: '<h3 class="search_heading">Practice Tests</h3>'
    }
  },
  {
    name: 'functional_area',
    source: test_fa.ttAdapter(),
    displayKey: 'title',
    limit: 4,
    templates: {
        header: '<h3 class="search_heading">Functional Area</h3>'
    }
  }

//   {
//   displayKey: 'value',
//   source: tests.ttAdapter()
// }
);

$('.typeahead').on('typeahead:selected', function(evt, item) {
  if(item['title']){
    window.location = 'http://' + window.location.host +'/practice-tests/'+ item['slug'] +'/';}
  else{
    window.location = 'http://' + window.location.host +'/practice-tests/'+ item['slug'] +'-test/';
  }
})

$('#bloodhound_submit').click(function() {
  api_url = "/api/get-test/?nopage=true&fl=id,category,title,slug&title="+$('#bloodhound_input').val()+"&active=true&format=json"
 $.ajax({url: api_url, success: function(result){
  if(result.length == 1){
    if(item['title']){
      window.location = 'http://' + window.location.host +'/practice-tests/'+ result[0]['slug'] +'/';}
    else{
      window.location = 'http://' + window.location.host +'/practice-tests/'+ result[0]['slug'] +'-test/';
    }
  }
  else{
    $("#bloodhound_message").show();
  }
 }});
});

