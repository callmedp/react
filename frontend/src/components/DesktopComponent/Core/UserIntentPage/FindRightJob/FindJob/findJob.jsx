import React from 'react';
import { Link } from 'react-router-dom';
import './findJob.scss';
import { useForm } from 'react-hook-form';
import { InputField, SelectExperienceBox } from 'formHandler/desktopFormHandler/formFields';
import UserIntentForm from 'formHandler/desktopFormHandler/formData/userIntent';
import { fetchedUserIntentData } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';

const FindJob = (props) => {

    const { register, handleSubmit, errors } = useForm();
    const dispatch = useDispatch();
    const { history, type } = props;

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

                        <h2 className="heading3 mt-20">Let’s get you to the right job</h2>
                        <div className="d-flex">
                            <div className="w-50">
                                <div className="find-job">
                                    <form className="mt-20" onSubmit={handleSubmit(onSubmit)}>

                                        {/* <div className="form-group">
                                            <input type="text" className="form-control" id="job" name="job" placeholder=" "
                                                aria-required="true" aria-invalid="true" />
                                            <label for="">Current job title</label>
                                        </div> */}
                                        
                                        <InputField attributes={UserIntentForm.job} register={register}
                                                errors={!!errors ? errors[UserIntentForm.job.name] : ''} />
                                        
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

                                        <InputField attributes={UserIntentForm.skills} register={register}
                                            errors={!!errors ?errors[UserIntentForm.skills.name] : ''} />
                                        
                                        <button type="submit" className="btn btn-inline btn-primary submit-btn mt-30" role="button" data-toggle="modal"
                                        data-target="#thankyouModal">View jobs</button>
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