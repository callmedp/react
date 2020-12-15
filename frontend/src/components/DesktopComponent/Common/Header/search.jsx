import React, { useState, useEffect } from 'react';
import { Typeahead, withAsync, Input, Menu, MenuItem, Hint } from 'react-bootstrap-typeahead';
import { siteDomain } from 'utils/domains'
const AsyncTypeahead = withAsync(Typeahead);

const SEARCH_URI = 'http://127.0.0.1:8000/api/v1/search-query/';

const AsyncExample = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [options, setOptions] = useState([]);

  const handleSearch = (query) => {
    setIsLoading(true);

    fetch(`${SEARCH_URI}?q=${query}`)
      .then((resp) => resp.json())
      .then(({ p_u, ct_u, c_u }) => {
        // const p_options = p_u?.map((i) => ({
        //     name: i.name,
        //     url : i.url
        // }));

        // const ct_u_options = ct_u?.map((i) => ({
        //     name: i.name,
        //     url : i.url
        // }));

        // const c_u_options = c_u?.map((i) => ({
        //     name: i.name,
        //     url : i.url
        // }));
        // setOptions([p_options, ct_u_options, c_u_options])
        const d = [{"name":"Linkedin Priya - for FR","url":"/services/level2-priya/linkedin-priya/pd-2657"},{"name":"Trading","url":"/course/other/trading/pd-7125"},{"name":"Editing","url":"/course/other/editing/pd-7123"},{"name":"Test Linkedin","url":"/services/level2-priya/test-linkedin/pd-2677"},{"name":"Resume Writing Fresher for Linkedin","url":"/services/category21-2/resume-writing-2/pd-2682"},{"name":"Linkedin combo","url":"/services/level2-priya/linkedin-combo/pd-2675"},{"name":"Linkedin Priya for 4-8 years","url":"/services/level2-priya/test-product-priya/pd-2665"},{"name":"Test Linkedin test Priya","url":"/services/level2-priya/linkedin-test-priya/pd-2676"},{"name":"Resume Writing Exp for Linkedin","url":"/services/category21-2/resume-writing-3/pd-2683"}]
        const options = d.map((i) => ({
            name: i.name,
            url : i.url
        }));
        
        setOptions(options);
        setIsLoading(false);
      });
  };

  const filterBy = () => true;

  return (
    <AsyncTypeahead
      filterBy={filterBy}
      id="async-example"
    //   isLoading={isLoading}
      labelKey="name"
      minLength={2}
      delay={1000}
      // useCache={true}
      onSearch={handleSearch}
      options={options}
      emptyLabel="No matches found"
      inputProps = {{
          'className' : "form-control top-input",
          'aria-label' : "Search",
          'type' : "search"
      }}
      placeholder="Search anything"
      renderInput={({ inputRef, referenceElementRef, ...inputProps }) => (
        <Input
          {...inputProps}
          ref={(input) => {
            inputRef(input);
            referenceElementRef(input);
          }}
        />
      )}
      renderMenu={(results, menuProps) => (
        <Menu key={Math.random()} id={Math.random()}>
            <h6>Skills</h6>
            {results.slice(0,4).map((result, index) => (
                <MenuItem option={result} position={index}>
                {result.name}
                </MenuItem>
            ))}
            <h6>Courses</h6>
            {results.slice(0,4).map((result, index) => (
                <MenuItem option={result} position={index}>
                {result.name}
                </MenuItem>
            ))}
        </Menu>
      )}
    // renderMenuItemChildren={(option, props) => (
    //     <>
    //       <span>{option.name}</span>
    //     </>
    //   )}
    />
  );
};

export default AsyncExample;