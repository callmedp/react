import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import './findJob.scss';
import { useForm } from 'react-hook-form';
import { InputField, SelectIntentBox, MultiSelectBox } from 'formHandler/desktopFormHandler/formFields';
import Autocomplete from 'formHandler/desktopFormHandler/AutoComplete';
import UserIntentForm from 'formHandler/desktopFormHandler/formData/userIntent';
import { fetchCareerChangeData, fetchFindRightJobsData } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';
import useDebounce from 'utils/searchUtils/debouce';
import { IndianState } from 'utils/constants';
import { userSearch, relatedSearch, userSkillSearch } from 'utils/searchUtils/searchFunctions';

const FindJob = (props) => {
    const [chips, setChips] = useState([]);
    const { register, handleSubmit, errors } = useForm();
    const dispatch = useDispatch();
    const { history, type } = props;

    //Job title events handling
    //-------------------------------------------------------------------
    const jobTitle = useRef();
    const [results, setResults] = useState([]);
    const [jtError, setJtError] = useState(false)
    const [showResults, setShowResults] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const debouncedSearchTerm = useDebounce(searchTerm, 500);
    const [skillSet, setSkillSet] = useState([])

    const handleInput = (e) => {
        setJtError(false)
        setSearchTerm(e.target.value);
        e.target.value ?
            setCheckedClass('form-group checked') :
            setCheckedClass('form-group')
    }
    //-------------------------------------------------------------------

    //Skill Options handling
    //-------------------------------------------------------------------
    const skillsKey = useRef();
    const [skillResults, setSkillResults] = useState([]);
    const [searchSkillTerm, setSearchSkillTerm] = useState('');
    const [showSkillResults, setShowSkillResults] = useState(false);
    const debounceSkillSearch = useDebounce(searchSkillTerm, 500);

    const handleSkillsClick = () => {
        handleAppend(skillsKey.current.value)
        skillsKey.current.value = ''
    }

    const suggestSkills = (e) => {
        setSearchSkillTerm(e.target.value);
    }

    //-------------------------------------------------------------------

    //Handling of Green ticks
    const [checkedClass, setCheckedClass] = useState('form-group')
    
    //Getting Form values
    const addValues = (values) => {
        if (type === 'job') {
            return {
                ...values,
                'type': type,
                'job': jobTitle.current.value,
                'location': document.getElementById('location').value, //Is document work on SSR?
                'skills': chips?.concat(document.getElementById('skills').value.split(",")),
            }
        }
        else {
            return {
                ...values,
                'type': type,
                'job': jobTitle.current.value,
                'skills': chips?.concat(document.getElementById('skills').value.split(",")),
            }
        }
    }

    //Form Submission Handling
    const onSubmit = async (values, event) => {

        //Empty Job title case handling
        if(!jobTitle.current.value){
            setJtError(true)
            setCheckedClass('form-group error')
        }
        else{
            const data = addValues(values);

            if(type === 'job') {
                history.push({
                    search: `?job_title=${data?.job}&minexp=${data?.experience}&loc=${data?.location}&skill=${data?.skills.join()}`
                });
            }
            else{
                history.push({
                    search: `?job_title=${data?.job}&minexp=${data?.experience}&department=${data?.department}&skill=${data?.skills.join()}`
                });
            }
        }
    }

    //Skills Append and Remove function
    function handleAppend(data, id) {
        setChips([...chips, data])
    }

    function handleDelete(value) {
        setChips(chips.filter(function (chip) {
            return chip !== value
        }));
    }

    //Data Append Handling
    const appendData = async (e, refr) => {
        if(refr){
            refr.current.value = e.target.textContent
            if(refr.current.id === 'job'){
                setShowResults(false)
                var data = await relatedSearch(jobTitle.current.value)
                setSkillSet(data?.slice(0, 10))
            }
            else{
                handleSkillsClick()
                setSkillResults([])
                setShowSkillResults(false)
            }
        }
    }

    //Return result format
    const getMenuItems = (data, refr, noOfItems = 6) => {
        return (
            <>
                {data?.slice(0, noOfItems)?.map((result, idx) => (
                    <div key={idx} onClick={e => appendData(e, refr)}>
                        <span>{result?.pdesc?.replace(/\w\S*/g, (w) => (w.replace(/^\w/, (c) => c.toUpperCase())))}</span>
                    </div>
                ))}
            </>
        )
    }

    useEffect(() => {
        // Make sure we have a value (user has entered something in input)
        if(debounceSkillSearch) {
            userSkillSearch(debounceSkillSearch).then(results => {
                setSkillResults(results?.data);
            });
        }
        else if (debouncedSearchTerm) {
            userSearch(debouncedSearchTerm).then(results => {
                setResults(results?.data);
            });
        } 
        else {
            setResults([]);
            setSkillResults([]);
        }
    }, [debouncedSearchTerm, debounceSkillSearch]);

    return (
        <section className="container-fluid mt-30n mb-0">
            <div className="row">
                <div className="container">
                    <div className="ui-main col">
                        <div className="ui-steps">
                            <Link className="completed" to={"#"}>1</Link>
                            <Link className="current" to={"#"}>2</Link>
                            <Link to={'#'}>3</Link>
                        </div>

                        <h2 className="heading3 mt-20">{type === 'job' ? 'Let’s get you to the right job' : type === 'pcareer' ? 'Get to next level with shine' : 'What do you have in mind'} </h2>
                        <div className="d-flex">
                            <div className="w-50">
                                <div className="find-job">
                                    <form className="mt-20" onSubmit={handleSubmit(onSubmit)}>

                                        <div className={checkedClass}>
                                            <input type="text" className="form-control" id="job" name="job" placeholder=" " ref={jobTitle} autoComplete="off"
                                                aria-required="true" aria-invalid="true" onChange={e => handleInput(e)} onFocus={() => setShowResults(true)} />
                                            <label htmlFor="">{ type === 'career' ? 'Preferred Role' : 'Current job title'}</label>
                                            { !!jtError ? <span className="error-msg">Job Title is Required</span> : ''}

                                            {showResults ?
                                                <div className="user-intent-search-result">
                                                    {results?.length ? getMenuItems(results, jobTitle) : null}
                                                </div> : null
                                            }
                                        </div>

                                        {/* <InputField attributes={UserIntentForm.job} register={register}
                                                errors={!!errors ? errors[UserIntentForm.job.name] : ''} /> */}

                                        {/*                                         
                                        <div className="form-group">        
                                                <select className="select" className="custom-select">
                                                    <option selected>Total experience </option>
                                                    <option value="+91">1 - 2</option>
                                                    <option value="+92">3 - 5</option>
                                                    <option value="+93">6+</option>
                                                </select>
                                        </div> */}

                                        <SelectIntentBox attributes={UserIntentForm.experience} register={register}
                                            errors={!!errors ? errors[UserIntentForm.experience.name] : ''} />

                                        {/* <div className="form-group">
                                            <input type="text" className="form-control" id="location" name="location" placeholder=" "
                                                aria-required="true" aria-invalid="true" />
                                            <label for="">Preferred location</label>
                                            <span class="error-msg">Required</span>
                                        </div> */}
                                        {type === 'job' ?
                                            <Autocomplete id={"location"} name={"location"} className={"form-control"} autoComplete={"off"}
                                                lableFor={"Preferred Location"} type={"text"} placeholder={" "}
                                                suggestions={IndianState}
                                            />
                                            :
                                            <SelectIntentBox attributes={UserIntentForm.department} register={register}
                                                errors={!!errors ? errors[UserIntentForm.department.name] : ''} />
                                        }

                                        {/* <InputField attributes={UserIntentForm.location} register={register}
                                                errors={!!errors ? errors[UserIntentForm.location.name] : ''} /> */}

                                        {/* <div className="form-group">
                                            <input type="text" className="form-control" id="skills" name="skills" placeholder=" "
                                                aria-required="true" aria-invalid="true" />
                                            <label for="">Your skills</label>
                                        </div> */}

                                        {/* <InputField attributes={UserIntentForm.skills} register={register}
                                            errors={!!errors ?errors[UserIntentForm.skills.name] : ''} /> */}


                                        {/* <MultiSelectBox attributes={UserIntentForm.skills} data={chips} register={register}
                                            errors={!!errors ? errors[UserIntentForm.skills.name] : ''} /> */}

                                        <div className={chips?.length ? "form-group-custom checked" : !!errors ? "form-group-custom error" : "form-group-custom"}>
                                            <label className="sticky-label" htmlFor="" style={!!errors ? { top: '1rem' } : { top: '-1rem' }}>Your skills</label>
                                            <div className="custom-textarea">
                                                {chips?.map((data, i) => {
                                                    return (
                                                        <label className="label-added" onClick={() => handleDelete(data)} for="">{data}</label>
                                                    )
                                                })
                                                }
                                                <span className="d-flex align-items-center mt-10">
                                                    <input type="text" className="form-control custom-input" name="skills" placeholder="Keyword Research" id="skills" autoComplete="off" ref={skillsKey} onChange={ e => suggestSkills(e) } onFocus={() => setShowSkillResults(true)} />
                                                    <button className="custom-btn" type="button" onClick={ handleSkillsClick }><figure className="icon-search-arrow"></figure></button>
                                                </span>
                                            </div>
                                            {   
                                                showSkillResults ?
                                                    <div className="user-intent-search-result">
                                                        {skillResults?.length ? getMenuItems(skillResults, skillsKey) : null}
                                                    </div> : null
                                            }
                                        </div>

                                        <div className="form-group-custom">
                                            {skillSet?.filter(item => !chips?.includes(item))?.map((skill, indx) => {
                                                return (
                                                    <label className="label-add" onClick={() => handleAppend(skill, indx)} htmlFor="" key={indx}>{skill}</label>
                                                )
                                            })
                                            }
                                        </div>


                                        <button type="submit" className="btn btn-inline btn-primary submit-btn mt-30" role="button" data-toggle="modal"
                                            data-target="#thankyouModal" type='submit'>{type === 'job' ? 'View Jobs' : 'View Courses'}</button>
                                    </form>
                                </div>
                            </div>
                            <figure className="find-job-bg">
                                <img src="/media/images/desktop/find-right-job.png" className="img-fluid" alt="Let’s get you to the right job" />
                            </figure>
                        </div>

                    </div>
                </div>
            </div>
        </section>
    )
}

export default FindJob;