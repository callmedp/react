import React, { useState, useEffect } from 'react';
import { siteDomain } from 'utils/domains';
import { useForm } from 'react-hook-form';
import useDebounce from '../../../../../utils/searchUtils/debouce';
import { searchCharacters, submitData } from '../../../../../utils/searchUtils/searchFunctions';
import { MyGA } from 'utils/ga.tracking.js';

const SearchBar = (props) => {
    const [searchTerm, setSearchTerm] = useState('');
    const { place, isHomepage } = props;
    const [results, setResults] = useState([]);
    const { register, handleSubmit } = useForm()
    const [showResults, setShowResults] = useState(false);
    const debouncedSearchTerm = useDebounce(searchTerm, 500);
    // let redirectPath = props.location.pathname;

    const handleScroll = () =>{
        const offset = window.scrollY;
        if(place === 'banner') {
            if(offset > 430) setShowResults(false)
        }
        else {
            if(offset > 70) {
                setShowResults(false)
            }
            else{
                setShowResults(true)
            }
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

    const k={"products":[{"name":"Editing","url":"/course/other/editing/pd-7123"},{"name":"LinkedIn Resume","url":"/services/level2-priya/linkedin-resume/pd-8"},{"name":"Linkedin Priya -  for FR","url":"/services/level2-priya/linkedin-priya/pd-2657"},{"name":"Distribution","url":"/course/other/distribution/pd-7120"},{"name":"Test Linkedin","url":"/services/level2-priya/test-linkedin/pd-2677"},{"name":"Direct Sales","url":"/course/other/direct-sales/pd-7084"},{"name":"Trading","url":"/course/other/trading/pd-7125"},{"name":"Test Linkedin test Priya","url":"/services/level2-priya/linkedin-test-priya/pd-2676"},{"name":"Linkedin Priya for  4-8 years","url":"/services/level2-priya/test-product-priya/pd-2665"},{"name":"Linkedin combo","url":"/services/level2-priya/linkedin-combo/pd-2675"},{"name":"Resume Writing Fresher for Linkedin","url":"/services/category21-2/resume-writing-2/pd-2682"},{"name":"Resume Writing Exp for Linkedin","url":"/services/category21-2/resume-writing-3/pd-2683"}],"skills":[{"name":"digital-marketing","url":"/courses/category21-2/digital-marketing-2/3/"},{"name":"Digital Marketing","url":"/courses/sales-and-marketing/digital-marketing/32/"}],"courses":[{"name":"Digital marketing expert","url":"/"},{"name":"India","url":"/course/category21-2/india/pd-9"},{"name":"new linkedin product","url":"/"}]}

    useEffect(() => {
        // Make sure we have a value (user has entered something in input)
        if (debouncedSearchTerm) {
            searchCharacters(debouncedSearchTerm).then(results => {
            setResults(k);
        });
        } else {
            setResults([]);
        }
        window.addEventListener('scroll', handleScroll);
    },[debouncedSearchTerm]);

    return (
        <>
            <div className={`pos-rel ${ !!isHomepage ? ' ml-auto' : ''}`}>
                <form className={`form-inline my-2 my-lg-0 ${place === 'banner' ? 'top-search': 'top-search'}`} onSubmit={handleSubmit(submitData)}>
                    <input className="form-control top-input" type="search" onChange={e => setSearchTerm(e.target.value)} onFocus={()=>setShowResults(true)} 
                        placeholder={props.placeHolder ? props.placeHolder : 'Search course, assessment...'} name="query" aria-label="Search" ref={register({required: true})} autoComplete="off" />
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