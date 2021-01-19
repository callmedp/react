import React, { useEffect } from 'react';

const HeaderSearchBox = (props) =>{
    const {
        setShowSearchPage,
        handleSubmit,
        setSearchTerm,
        register,
        setShowResults,
        showResults,
        results,
        getMenuItems,
        startDictation,
        submitData
    } = props

    useEffect(()=>{
        document.getElementById("transcript").focus();
    }, [])

    return(
        <>
            <div className="m-top-search-header">
                <figure className="micon-close-white mr-20" onClick={()=>setShowSearchPage(false)}></figure>
                <form id="searchForm" className="form-inline w-100 ml-auto" onSubmit={handleSubmit(submitData)}>
                    <button className="m-btn-search-black d-flex align-items-center">
                        <figure className="micon-search-black d-flex"></figure>
                    </button>
                    <input className="m-search-input" type="search" onChange={e => setSearchTerm(e.target.value)} onFocus={()=>setShowResults(true)} 
                        placeHolder = 'Search course, assessment...' name="query" id="transcript" aria-label="Search" ref={register({required: true})} autoComplete="off" />
                    <button className="m-btn-voice-search">
                        <figure className="micon-voice-search d-flex" onClick={(e)=>{e.preventDefault();startDictation();}}></figure>
                    </button>
                </form>
                {showResults ?
                    <div className="m-header-search-result">
                        { results?.skills?.length ? getMenuItems(results?.skills, 'Skills') : null }
                        { results?.courses?.length ? getMenuItems(results?.courses, 'Courses') : null }
                        { results?.products?.length ? getMenuItems(results?.products, 'Products'): null }
                    </div> : null
                }
            </div>
        </>
    )
}

export default HeaderSearchBox;