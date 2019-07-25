var tests = new Bloodhound({
  datumTokenizer: function(tests) {
      return Bloodhound.tokenizers.whitespace(tests.value);
  },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: "/api/get-test/?fl=id,category,title,slug",
    filter: function(response) {
      return response.results;
    }
  }
});

// initialize the bloodhound suggestion engine
tests.initialize();

// instantiate the typeahead UI
$('.typeahead').typeahead(
  { hint: true,
    highlight: true,
    minLength: 1
  },
  {
  name: 'tests',
  displayKey: function(tests) {
    return tests.title;
  },
  source: tests.ttAdapter()
});

$('.typeahead').on('typeahead:selected', function(evt, item) {
 window.location = 'http://' + window.location.host + item['slug'] +'-test/';
})
