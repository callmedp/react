import React, {Component} from 'react';
import './experience.scss'
import {renderField, renderTextArea, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {Field, reduxForm, FieldArray} from 'redux-form';
import * as actions from '../../../../../../store/experience/actions';
import {connect} from "react-redux";
import moment from 'moment';
import {required} from "../../../../../FormHandler/formValidations"

class Experience extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteExperience = this.deleteExperience.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);

    }
    componentDidMount() {
        this.props.fetchUserExperience()
    }

    async handleSubmit(values) {
        const {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        if(currentLinkPos > listOfLinks.length){
            currentLinkPos = 0
        }
        await this.props.bulkUpdateUserExperience(values.list);
        this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
    }

    handleAddition(fields, error) {
        
        fields.push({
            "candidate_id": '',
            "id": '',
            "job_profile": '',
            "company_name": '',
            "start_date": '',
            "end_date": '',
            "is_working": false,
            "job_location": '',
            "work_description": '',
            order: fields.length
        })
    }

    deleteExperience(index, fields, event) {
        event.stopPropagation();
        const experience = fields.get(index);
        fields.remove(index);
        if (experience && experience.id) {
            this.props.removeExperience(experience.id)
        }
    }

    changeOrderingUp(index,fields,event){
        event.stopPropagation();
        console.log("Clicked Up")
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index - 1)
        fields.insert(index - 1, prevItem)
        fields.swap(index, index - 1)
    }

    changeOrderingDown(index,fields,event){
        event.stopPropagation();
        console.log("Clicked Down")
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index+1)
        fields.insert(index + 1, nextItem)
        fields.swap(index, index + 1);
    }

    render() {
        const {handleSubmit, experience} = this.props;
        const renderExperiences = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Experience</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button"
                        onClick={this.handleAddition.bind(this, fields, error)}
                        type={'button'} className="btn btn__round btn--outline">+ Add new</button>
                    </div>
                    {fields.map((member, index) => {
                        return (
                        <React.Fragment key={index}>
                            <div className="subHeading pb-0">
                                <h2>{fields.get(index).company_name || 'Experience'}</h2>
                                <ul className="subHeading__control">
                                    <li className="subHeading__delete">
                                        <span className="sprite icon--delete"
                                        onClick={(event) => this.deleteExperience(index, fields, event)}
                                        role="button"></span>
                                    </li>
                                    {index == 0 ? '':
                                        <li className="subHeading__btn"
                                            onClick={(event) => this.changeOrderingUp(index, fields, event)}>
                                            <i className="sprite icon--upArrow"></i>
                                        </li>
                                    }
                                    {index == fields.length-1 ? '':
                                        <li className="subHeading__btn"
                                            onClick={(event) => this.changeOrderingDown(index, fields, event)}>
                                            <i className="sprite icon--downArrow"></i>
                                        </li>
                                    }
                                </ul>
                            </div>

                            <ul className="form pb-0">
                                <li className="form__group">
                                    <label className="form__label" htmlFor="job_profile">Designation</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--designation"></i>
                                            </span>
                                        </div>
                                        <Field component={renderField} type={"text"} 
                                        name={`${member}.job_profile`} className="form__input"  />
                                    </div>
                                </li>

                                <li className="form__group">
                                    <label className="form__label" htmlFor="company_name">Company name</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--company"></i>
                                            </span>
                                        </div>
                                        <Field component={renderField} type={"text"} 
                                        name={`${member}.company_name`} className="form__input"/>
                                    </div>
                                </li>

                                <li className="form__group">
                                    <label className="form__label" htmlFor="start_date">Date from</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--date"></i>
                                            </span>
                                        </div>
                                        <Field component={datepicker} type={"date"} 
                                        className="form__input" name={`${member}.start_date`}/>
                                    </div>
                                </li>

                                <li className="form__group">
                                    <label className="form__label" htmlFor="end_date">Date to</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--date"></i>
                                            </span>
                                        </div>
                                        <Field component={datepicker} type={"date"} 
                                        className="form__input" name={`${member}.end_date`}/>
                                    </div>
                                </li>

                                <li className="form__radio-group d-flex justify-content-end fs-14">
                                    <Field type="radio" name={`${member}.is_working`}component="input" 
                                        className="form__radio-input" value={`${member}.is_working`}/>
                                    <label className="form__radio-label" htmlFor="is_working">
                                        <span className="form__radio-button"></span>
                                        Till today
                                    </label>
                                </li>

                                <li className="form__group">
                                    <label className="form__label" htmlFor="job_location">Job Location</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--company"></i>
                                            </span>
                                        </div>
                                        <Field component={renderField} type={"text"} 
                                        name={`${member}.job_location`} className="form__input"/>
                                    </div>
                                </li>

                                <li className="form__group">
                                    <label className="form__label" htmlFor="work_description">Description</label>
                                    <Field component={renderTextArea} type={"textarea"} name={`${member}.work_description`}
                                        className="form__input h-300" rows="5" 
                                    />
                                </li>

                            </ul>
                        </React.Fragment>
                        )
                    })}
                    
                </div>

            )
        }
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" component={renderExperiences}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline">Preview</button>
                                <button className="btn btn__round btn__primary" type={'submit'}>Save &amp; Continue</button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}

export const ExperienceForm = reduxForm({
    form: 'experience',
    enableReinitialize: true
})(Experience);


const mapStateToProps = (state) => {
    return {
        initialValues: state.experience,
        experience: state.experience
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userExperience) => {
            const {start_date, end_date} = userExperience;
            userExperience = {
                ...userExperience,
                ...{
                    start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                    end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || ''
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserExperience({userExperience, resolve, reject}));
            })
        },
        "fetchUserExperience": () => {
            return dispatch(actions.fetchUserExperience())
        },
        "removeExperience": (experienceId) => {
            return dispatch(actions.deleteExperience(experienceId))
        },

        "bulkUpdateUserExperience": (listItems) => {
            listItems = (listItems || []).map(userExperience => {
                const {start_date, end_date} = userExperience;
                if (!userExperience['id']) delete userExperience['id'];
                userExperience = {
                    ...userExperience,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || ''
                    }
                };
                return userExperience;
            });
            return dispatch(actions.bulkUpdateUserExperience({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ExperienceForm);
