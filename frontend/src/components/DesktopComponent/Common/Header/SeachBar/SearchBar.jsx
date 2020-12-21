import React, { useState, useEffect } from 'react';
import { siteDomain } from 'utils/domains';
import { useForm } from 'react-hook-form';
import useDebounce from '../../../../../utils/debouce';

// API search function
const searchCharacters = search =>{
    return fetch(`${siteDomain}/api/v1/search-query/?q=${search}`,
        { method: 'GET' }).then(r => r.json())
        .catch(error => {
            console.error(error);
            return [];
        }
    );
}

const SearchBar = (props) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const { register, handleSubmit, errors } = useForm()
    const [showResults, setShowResults] = useState(false);

    const debouncedSearchTerm = useDebounce(searchTerm, 500);

    const onSubmit = async (values, event) => {
        const searchedQuery = values?.query
        if(searchedQuery){
            window.location.replace(`${siteDomain}/search/results/?q=${searchedQuery}`);
        }
    }

    const handleScroll = () =>{
        const offset = window.scrollY;
        if(offset > 70){
            setShowResults(false)
        }
        else{
            setShowResults(true)
        }
    }

    useEffect(() => {
        // Make sure we have a value (user has entered something in input)
        if (debouncedSearchTerm) {
            searchCharacters(debouncedSearchTerm).then(results => {
            setResults(results);
        });
        } else {
            setResults([]);
        }
        window.addEventListener('scroll', handleScroll);
    },[debouncedSearchTerm]);

    return (
        <>
            <div className="ml-auto pos-rel">
                <form className="form-inline top-search my-2 my-lg-0" onSubmit={handleSubmit(onSubmit)}>
                    <input className="form-control top-input" type="search" onChange={e => setSearchTerm(e.target.value)} onFocus={()=>setShowResults(true)} 
                        placeholder="Search anything" name="query" aria-label="Search" ref={register({required: true})} autoComplete="off" />
                    <button className="btn btn-search" type="submit"><figure className="icon-search"></figure></button>
                </form>
                {showResults ?<div className="header-search-result">
                    {results?.skills?.length ? 
                        <>
                            <strong>Skills</strong> 
                            {results?.skills?.slice(0,3)?.map(result => (
                                <div key={Math.random()}>
                                <a href={`${siteDomain}${result.url}`}>{result.name}</a>
                                </div>
                            ))}
                        </> : null
                    }

                    {results?.courses?.length ? 
                        <>
                            <strong>Courses</strong> 
                            {results?.courses?.slice(0,3)?.map(result => (
                                <div key={Math.random()}>
                                <a href={`${siteDomain}${result.url}`}>{result.name}</a>
                                </div>
                            ))}
                        </> : null
                    }

                    {results?.products?.length ? 
                        <>
                            <strong>Products</strong>
                            {results?.products?.slice(0,3)?.map(result => (
                                <div key={Math.random()}>
                                <a href={`${siteDomain}${result.url}`}>{result.name}</a>
                                </div>
                            ))}
                        </> : null
                    }
                </div>:null}
            </div>
        </>
    );
}

export default SearchBar;