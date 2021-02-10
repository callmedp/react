import React, { useState, useEffect } from 'react';
import { siteDomain } from 'utils/domains';
import { useForm } from 'react-hook-form';
import useDebounce from '../../../../../utils/searchUtils/debouce';
import { searchCharacters, submitData } from '../../../../../utils/searchUtils/searchFunctions';
import { MyGA } from 'utils/ga.tracking.js';

const SearchBar = (props) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const { register, handleSubmit } = useForm()
    const [showResults, setShowResults] = useState(false);
    const debouncedSearchTerm = useDebounce(searchTerm, 500);
    let redirectPath = window.location.pathname;

    const handleScroll = () =>{
        const offset = window.scrollY;
        if(offset > 70){
            setShowResults(false)
        }
        else{
            setShowResults(true)
        }
    }

    const getMenuItems = (data, heading, noOfItems=3) => {
        return (
            <>
                <strong>{heading}</strong> 
                {data?.slice(0, noOfItems)?.map(result => (
                    <div key={Math.random()}>
                        <a href={`${siteDomain}${result.url}`}>{result.name}</a>
                    </div>
                ))}
            </> 
        )
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
            <div className={`pos-rel ${(redirectPath !== '/' || '') ? ' ml-auto' : ''}`}>
                <form className="form-inline top-search my-2 my-lg-0" onSubmit={handleSubmit(submitData)}>
                    <input className="form-control top-input" type="search" onChange={e => setSearchTerm(e.target.value)} onFocus={()=>setShowResults(true)} 
                        placeholder={props.placeHolder} name="query" aria-label="Search" ref={register({required: true})} autoComplete="off" />
                    <button className="btn btn-search" aria-label="search Button" type="submit" onClick={() => MyGA.SendEvent('click_on_search','ln_click_on_search', 'ln_search_initiated_navigation', 'ln_click_on_search', 'click_on _search','', false, true)}><figure className="icon-search"></figure></button>
                </form>
                {showResults ?
                    <div className="header-search-result">
                        { results?.skills?.length ? getMenuItems(results?.skills, 'Skills') : null }
                        { results?.courses?.length ? getMenuItems(results?.courses, 'Courses') : null }
                        { results?.products?.length ? getMenuItems(results?.products, 'Products'): null }
                    </div> : null
                }
            </div>
        </>
    );
}

export default SearchBar;