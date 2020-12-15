import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import useDebounce from './debounce';

// Usage
const TypeAhead = (props) => {
  // State and setter for search term
  const [searchTerm, setSearchTerm] = useState('');
  // State and setter for search results
  const [results, setResults] = useState([]);
  // State for search status (whether there is a pending API request)
  const [isSearching, setIsSearching] = useState(false);

  // Now we call our hook, passing in the current searchTerm value.
  // The hook will only return the latest value (what we passed in) ...
  // ... if it's been more than 500ms since it was last called.
  // Otherwise, it will return the previous value of searchTerm.
  // The goal is to only have the API call fire when user stops typing ...
  // ... so that we aren't hitting our API rapidly.
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  // Here's where the API call happens
  // We use useEffect since this is an asynchronous action
  useEffect(
    () => {
      // Make sure we have a value (user has entered something in input)
      if (debouncedSearchTerm) {
        // Set isSearching state
        setIsSearching(true);
        // Fire off our API call
        searchCharacters(debouncedSearchTerm).then(results => {
          // Set back to false since request finished
          setIsSearching(false);
          // Set results state
          const data = {"p_u":[{"name":"Editing","url":"/course/other/editing/pd-7123"},{"name":"Linkedin combo","url":"/services/level2-priya/linkedin-combo/pd-2675"},{"name":"Linkedin Priya for  4-8 years","url":"/services/level2-priya/test-product-priya/pd-2665"},{"name":"Test Linkedin test Priya","url":"/services/level2-priya/linkedin-test-priya/pd-2676"},{"name":"Resume Writing Exp for Linkedin","url":"/services/category21-2/resume-writing-3/pd-2683"},{"name":"Trading","url":"/course/other/trading/pd-7125"},{"name":"Test Linkedin","url":"/services/level2-priya/test-linkedin/pd-2677"},{"name":"Resume Writing Fresher for Linkedin","url":"/services/category21-2/resume-writing-2/pd-2682"},{"name":"Linkedin Priya -  for FR","url":"/services/level2-priya/linkedin-priya/pd-2657"}],"ct_u":[{"name":"digital-marketing","url":"/courses/category21-2/digital-marketing-2/3/"}],"c_u":[{"name":"India","url":"/course/category21-2/india/pd-9"},{"name":"new linkedin product","url":"/"}]}
          setResults(data);
        });
      } else {
        setResults([]);
      }
    },
    // This is the useEffect input array
    // Our useEffect function will only execute if this value changes ...
    // ... and thanks to our hook it will only change if the original ...
    // value (searchTerm) hasn't changed for more than 500ms.
    [debouncedSearchTerm]
  );

  // Pretty standard UI with search input and results
  return (
    <>
    <div className="ml-auto pos-rel">
        <form className="form-inline top-search my-2 my-lg-0">
            <input className="form-control top-input" type="search" onChange={e => setSearchTerm(e.target.value)} placeholder="Search anything" aria-label="Search" />
            <button className="btn btn-search" type="submit"><figure className="icon-search"></figure></button>
        </form>
      {/* {isSearching && <div>Searching ...</div>} */}
        <div className="header-search-result">
        {results?.p_u?.length ? <strong>Skills</strong> : null}
        {results?.p_u?.slice(0,3)?.map(result => (
            <div key={Math.random()}>
            <Link>{result.name}</Link>
            </div>
        ))}
        
        {results?.ct_u?.length ? <strong>Courses</strong> : null}
        {results?.ct_u?.slice(0,3)?.map(result => (
            <div key={Math.random()}>
            <Link>{result.name}</Link>
            </div>
        ))}

        {results?.c_u?.length ? <strong>Products</strong> : null}
        {results?.c_u?.slice(0,3)?.map(result => (
            <div key={Math.random()}>
            <Link>{result.name}</Link>
            </div>
        ))}
        </div>
    </div>
    </>
  );
}

// API search function
function searchCharacters(search) {
  return fetch(
    `http://127.0.0.1:8000/api/v1/search-query/?q=${search}`,
    {
      method: 'GET'
    }
  )
    .then(r => r.json())
    .catch(error => {
      console.error(error);
      return [];
    });
}

export default TypeAhead;