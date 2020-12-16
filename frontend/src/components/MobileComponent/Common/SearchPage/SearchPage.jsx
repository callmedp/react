import React, { useState, useEffect } from 'react';
import { siteDomain } from 'utils/domains';
import { useForm } from 'react-hook-form';
import useDebounce from '../../../../utils/searchUtils/debouce';
import { searchCharacters, submitData } from '../../../../utils/searchUtils/searchFunctions';
import './SearchPage.scss';

const SearchPage = (props) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const { register, handleSubmit, errors } = useForm()
    const [showResults, setShowResults] = useState(false);
    const debouncedSearchTerm = useDebounce(searchTerm, 500);

    // const handleScroll = () =>{
    //     const offset = window.scrollY;
    //     if(offset > 70){
    //         setShowResults(false)
    //     }
    //     else{
    //         setShowResults(true)
    //     }
    // }

    useEffect(() => {
        // Make sure we have a value (user has entered something in input)
        if (debouncedSearchTerm) {
            searchCharacters(debouncedSearchTerm).then(results => {
                const data = {
                    'products':[{
                        'name':'Editing',
                        'url':'https://abc.com'
                    }],
                    'courses': [{
                        'name':'Editing',
                        'url':'https://abc.com'
                    }]
                }
                setResults(data);
        });
        } else {
            setResults([]);
        }
        // window.addEventListener('scroll', handleScroll);
    },[debouncedSearchTerm]);

    return (
        <>
            <div className="m-top-search-header">
                <figure className="micon-close-white mr-20"></figure>
                <form className="form-inline w-100 ml-auto" onSubmit={handleSubmit(submitData)}>
                    <figure className="m-btn-search-black d-flex"></figure>
                    <input className="m-search-input" type="search" onChange={e => setSearchTerm(e.target.value)} onFocus={()=>setShowResults(true)} 
                        placeholder="Search anything" name="query" aria-label="Search" ref={register({required: true})} autocomplete="off" />
                    <button className="m-btn-voice-search">
                        <figure className="micon-voice-search d-flex"></figure>
                    </button>
                </form>
                {showResults ?<div className="m-header-search-result">
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

export default SearchPage;