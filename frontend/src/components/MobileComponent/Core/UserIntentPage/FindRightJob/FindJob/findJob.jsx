import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './findJob.scss';
import { useForm } from 'react-hook-form';
// import { useDispatch } from 'react-redux';
import { SelectExperienceBox, MultiSelectBox } from 'formHandler/mobileFormHandler/formFields';
import UserIntentForm from 'formHandler/mobileFormHandler/formData/userIntent';
import Autocomplete from 'formHandler/mobileFormHandler/AutoComplete';
// import { fetchFindRightJobsData } from 'store/UserIntentPage/actions';
import { IndianState } from 'utils/constants';

// Debouncing
import useDebounce from 'utils/searchUtils/debouce';
import { userSearch, relatedSearch } from 'utils/searchUtils/searchFunctions';

const FindJob = (props) => {
    const { history, type } = props;
    // const dispatch = useDispatch();
    const [chips, setChips] = useState([]);
    const [skillSet, setSkillSet] = useState([])
    const { register, handleSubmit, errors } = useForm();
    const jobTitle = useRef();
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const [showResults, setShowResults] = useState(false);
    const debouncedSearchTerm = useDebounce(searchTerm, 500);
    const [checkedClass, setCheckedClass] = useState('form-group')

    const addValues = (values) => {
        return {
            ...values,
            'type': type,
            'job': jobTitle.current.value,
            'location': document.getElementById('location').value, //Is document work on SSR?
            'skills': chips.length > 0 ? chips?.concat(document.getElementById('skills').value.split(",")) : [],
            'page': 1
        }
    }

    function handleAppend(data, id) {
        setChips([...chips, data])
        delete skillSet[id];
    }

    const appendData = async (e) => {
        jobTitle.current.value = e.target.textContent
        setShowResults(false)
        var data = await relatedSearch(jobTitle.current.value)
        setSkillSet(data?.data?.related_skill?.slice(0, 10))
    }

    const handleInput = (e) => {
        setSearchTerm(e.target.value);
    }

    function handleDelete(value) {
        setChips(chips.filter(function (chip) {
            return chip !== value
        }))
    }

    const getMenuItems = (data, noOfItems = 6) => {
        return (
            <>
                {data?.slice(0, noOfItems)?.map(result => (
                    <div key={result?.pid} onClick={e => appendData(e)}>
                        <span>{result?.pdesc?.replace(/\w\S*/g, (w) => (w.replace(/^\w/, (c) => c.toUpperCase())))}</span>
                    </div>
                ))}
            </>
        )
    }

    useEffect(() => {
        // Make sure we have a value (user has entered something in input)
        if (debouncedSearchTerm) {
            userSearch(debouncedSearchTerm).then(results => {
                setResults(results?.data);
            });
        } else {
            setResults([]);
        }
    }, [debouncedSearchTerm]);

    const onSubmit = async (values, event) => {
        const data = addValues(values);
        history.push({
            search: `?job_title=${data?.job}&minexp=${data?.experience}&loc=${data?.location}&skill=${data?.skills}`
        });
    }

    return (
        <section className="m-container mt-0 mb-0 pl-0 pr-0">
            <div className="m-ui-main col">
                <div className="d-flex align-items-center">
                    <div className="m-ui-steps">
                        <Link className="m-completed" to={"#"}>1</Link>
                        <Link className="m-current" to={"#"}>2</Link>
                        <Link>3</Link>
                    </div>
                    <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                </div>
                <h2 className="m-heading3 mt-20">{type === 'job' ? 'Let’s get you to the right job' : type === 'pcareer' ? 'Get to next level with shine' : 'What do you have in mind'}</h2>

                <div className="m-find-job">
                    <form className="mt-20" onSubmit={handleSubmit(onSubmit)}>
                        <div className={checkedClass}>
                            <input type="text" className="form-control" id="job" name="job" required="required" placeholder=" " ref={jobTitle} autoComplete="off"
                                aria-required="true" aria-invalid="true" onChange={e => handleInput(e)} onFocus={() => setShowResults(true)} />
                            <label for="">Current job title</label>

                            {showResults ?
                                <div className="user-intent-search-result">
                                    {results?.length ? getMenuItems(results) : null}
                                </div> : null
                            }
                        </div>

                        <SelectExperienceBox attributes={UserIntentForm.experience} register={register}
                            errors={!!errors ? errors[UserIntentForm.experience.name] : ''} />

                        <Autocomplete id={"location"} name={"location"} className={"form-control"} autoComplete={"off"}
                            lableFor={"Preferred Location"} type={"text"} placeholder={" "}
                            suggestions={IndianState}
                        />

                        <MultiSelectBox attributes={UserIntentForm.skills} data={chips} register={register}
                            errors={!!errors ? errors[UserIntentForm.skills.name] : ''} />

                        <div className="form-group-custom">
                            {skillSet?.filter(item => !chips?.includes(item))?.map((skill, indx) => {
                                return (
                                    <label className="label-add" onClick={() => handleAppend(skill, indx)} for="">{skill}</label>
                                )
                            })}
                        </div>

                        <button type="submit" className="btn btn-inline btn-primary submit-btn mt-30" role="button" data-toggle="modal" data-target="#thankyouModal">{type === 'job' ? 'View jobs' : 'View courses'}</button>
                    </form>
                </div>
            </div>
        </section>
    )
}

export default FindJob;