import React, { useState, useEffect } from 'react';
import { siteDomain } from 'utils/domains';
import { useForm } from 'react-hook-form';
import useDebounce from '../../../../../utils/searchUtils/debouce';
import { searchCharacters, submitData } from '../../../../../utils/searchUtils/searchFunctions';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const SearchBar = (props) => {
    const [searchTerm, setSearchTerm] = useState('');
    const { place, isHomepage, pageTitle } = props;
    const [results, setResults] = useState([]);
    const { register, handleSubmit } = useForm()
    const [showResults, setShowResults] = useState(false);
    const debouncedSearchTerm = useDebounce(searchTerm, 500);
    const sendLearningTracking = useLearningTracking();

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

    const sendMultipleEvents = (name) => {

        MyGA.SendEvent('ln_new_homepage', 'ln_search_course', 'ln_search_initiated', stringReplace(name), '', false, true);

        sendLearningTracking({
            productId: '',
            event: `${stringReplace(name)}_searchbar_searched`,
            pageTitle:`${pageTitle}`,
            sectionPlacement: `searchbar`,
            eventCategory: '',
            eventLabel: '',
            eventAction: 'search',
            algo: '',
            rank: '',
        })
    }

    const getMenuItems = (data, heading, noOfItems=3) => {
        return (
            <>
                <strong>{heading}</strong> 
                {data?.slice(0, noOfItems)?.map(result => (
                    <div key={Math.random()}>
                        <a href={`${siteDomain}${result.url}`} onClick = { () => sendMultipleEvents(result.name)}>{result.name}</a>
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
            <div className={`pos-rel ${ !isHomepage ? ' ml-auto' : ''}`}>
                <form className={`form-inline my-2 my-lg-0 ${place === 'banner' ? 'top-search': 'top-search'}`} onSubmit={handleSubmit(submitData)}>
                    <input className="form-control top-input" type="search" id={ !!isHomepage ? 'Search' : 'Search-Box' } onChange={e => setSearchTerm(e.target.value)} onFocus={()=>setShowResults(true)} 
                        placeholder={props.placeHolder ? props.placeHolder : 'Search course, assessment...'} name="query" aria-label="Search" ref={register({required: true})} autoComplete="off" />
                    <button className="btn btn-search" aria-label="search Button" type="submit" onClick={() => !isHomepage ? MyGA.SendEvent('click_on_search','ln_click_on_search', 'ln_search_initiated_navigation', 'ln_click_on_search','', false, true) : MyGA.SendEvent('ln_new_homepage','ln_search_course', 'ln_search_initiated', searchTerm,'', false, true) }><figure className="icon-search"></figure></button>
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