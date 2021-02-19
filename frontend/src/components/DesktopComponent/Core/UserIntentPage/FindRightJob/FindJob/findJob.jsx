import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import './findJob.scss';
import { useForm } from 'react-hook-form';
import { InputField, SelectExperienceBox, MultiSelectBox } from 'formHandler/desktopFormHandler/formFields';
import UserIntentForm from 'formHandler/desktopFormHandler/formData/userIntent';
import { fetchedUserIntentData } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';
import useDebounce from 'utils/searchUtils/debouce';
import { userSearch } from 'utils/searchUtils/searchFunctions';
import { IndianState } from 'utils/constants';

const FindJob = (props) => {
    const [chips, setChips] = useState([]);
    const { register, handleSubmit, errors } = useForm();
    const dispatch = useDispatch();
    const textInput = useRef();
    const { history, type } = props;
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const [showResults, setShowResults] = useState(false);
    const debouncedSearchTerm = useDebounce(searchTerm, 700);

    const addValues = (values) =>{
        return {
            ...values,
            'type': type,
        }
    }

    const onSubmit = async (values, event) => {
        const data = addValues(values)
        await new Promise((resolve) => dispatch(fetchedUserIntentData({data, resolve})));
        history.push({
            search: `?job=${values.job}&experience=${values.experience}&location=${values.location}&skills=${values.skills}`
          })
          
    }

    function handleAppend(data, id) {
        // UserIntentForm.skills.children.push(data);
        // console.log(UserIntentForm.skills.children)
        setChips([...chips, data])

    }

    const skill_data = [
        {
            name: 'Advanced Accounting', id: 1
        },
        {
            name: 'Risk Mangement', id: 2
        },
        {
            name: 'GST', id: 3
        },
        {
            name: 'Data Science', id: 4
        }
    ]
    const appendData = (e) => {
        textInput.current.value = e.target.textContent
        setShowResults(false)
    }

    const getMenuItems = (data, noOfItems=6) => {
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
                setResults(results);
            });
        } else {
            setResults([]);
        }
    },[debouncedSearchTerm]);

    return (
        <section className="container-fluid mt-30n mb-0">
            <div className="row">
                <div className="container">
                    <div className="ui-main col">
                        <div className="ui-steps">
                            <Link className="completed" to={"#"}>1</Link>
                            <Link className="current" to={"#"}>2</Link>
                            <Link>3</Link>
                        </div>

                        <h2 className="heading3 mt-20">{ type === 'job' ? 'Let’s get you to the right job' : type === 'pcareer' ? 'Get to next level with shine' : 'What do you have in mind' } </h2>
                        <div className="d-flex">
                            <div className="w-50">
                                <div className="find-job">
                                    <form className="mt-20" onSubmit={handleSubmit(onSubmit)}>

                                        <div className="form-group">
                                            <input type="text" className="form-control" id="job" name="job" placeholder=" " ref={textInput} autoComplete="off"
                                                aria-required="true" aria-invalid="true" onChange={e => setSearchTerm(e.target.value)} onFocus={()=>setShowResults(true)} />
                                            <label for="">Current job title</label>

                                            {showResults ?
                                                <div className="user-intent-search-result">
                                                    { results?.length ? getMenuItems(results) : null }
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
                                        
                                        <SelectExperienceBox attributes={UserIntentForm.experience} register={register}
                                                  errors={!!errors ? errors[UserIntentForm.experience.name] : '' } />

                                        {/* <div className="form-group">
                                            <input type="text" className="form-control" id="location" name="location" placeholder=" "
                                                aria-required="true" aria-invalid="true" />
                                            <label for="">Preferred location</label>
                                            <span class="error-msg">Required</span>
                                        </div> */}

                                        <InputField attributes={UserIntentForm.location} register={register}
                                                errors={!!errors ? errors[UserIntentForm.location.name] : ''} />

                                        {/* <div className="form-group">
                                            <input type="text" className="form-control" id="skills" name="skills" placeholder=" "
                                                aria-required="true" aria-invalid="true" />
                                            <label for="">Your skills</label>
                                        </div> */}

                                        {/* <InputField attributes={UserIntentForm.skills} register={register}
                                            errors={!!errors ?errors[UserIntentForm.skills.name] : ''} /> */}

                                        
                                        <MultiSelectBox attributes={UserIntentForm.skills} data={chips} register={register}
                                            errors={!!errors ? errors[UserIntentForm.skills.name] : ''} />

                                        <div className="form-group-custom">
                                            {skill_data?.map((skill, indx) => {
                                                return (
                                                    <label className="label-add" onClick={() => handleAppend(skill.name, indx)} for="">{skill.name}</label>
                                                )
                                            })
                                            }
                                        </div>
                                        
                                        
                                        <button type="submit" className="btn btn-inline btn-primary submit-btn mt-30" role="button" data-toggle="modal"
                                        data-target="#thankyouModal">{ type === 'job' ? 'View jobs' : 'View courses' }</button>
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