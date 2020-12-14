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
        const options = p_u.map((i) => ({
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
      useCache={true}
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
    //   renderMenu={(results, menuProps) => (
    //     <Menu key={Math.random()} id={Math.random()}>
    //         {results.length ?<h6>Skills</h6>:null}
    //         {results.slice(0,4).map((result, index) => (
    //             <MenuItem option={result} position={index}>
    //             {result.name}
    //             </MenuItem>
    //         ))}
    //         {/* {results.length ?<h6>Courses</h6>:null}
    //         {results.slice(0,4).map((result, index) => (
    //             <MenuItem option={result} position={index}>
    //             {result.name}
    //             </MenuItem>
    //         ))} */}
    //     </Menu>
    //   )}
    renderMenuItemChildren={(option, props) => (
        <>
          <span>{option.name}</span>
        </>
      )}
    />
  );
};

export default AsyncExample;