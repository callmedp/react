import React, { useState, useEffect } from 'react';
import { siteDomain } from 'utils/domains';
import { useForm } from 'react-hook-form';
import useDebounce from '../../../../utils/searchUtils/debouce';
import { searchCharacters, submitData } from '../../../../utils/searchUtils/searchFunctions';
import './SearchPage.scss';
import { startDictation } from '../../../../utils/searchUtils/speechRecognition';
import HeaderSearchBox from './HeaderSearch/HeaderSearchBox';

const SearchPage = (props) => {
    const { setShowSearchPage } = props
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const { register, handleSubmit, errors } = useForm()
    const [showResults, setShowResults] = useState(false);
    const debouncedSearchTerm = useDebounce(searchTerm, 500);

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
    },[debouncedSearchTerm]);

    return (
        <HeaderSearchBox setShowSearchPage={setShowSearchPage} handleSubmit={handleSubmit} setSearchTerm={setSearchTerm}
                        register={register} setShowResults={setShowResults} showResults={showResults} results={results} 
                        getMenuItems={getMenuItems} startDictation={startDictation} submitData={submitData}/>
    );
}

export default SearchPage;