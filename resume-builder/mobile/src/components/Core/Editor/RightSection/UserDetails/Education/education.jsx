import React, {Component} from 'react';
import {Field, reduxForm} from "redux-form";
import {renderField, renderTextArea, renderSelect, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {required} from "../../../../../FormHandler/formValidations"
import * as actions from "../../../../../../store/education/actions";
import {connect} from "react-redux";
import moment from "moment";

class Education extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteEducation = this.deleteEducation.bind(this);
    }

    async handleSubmit(values) {
        await this.props.bulkUpdateUserEducation(values.list);
        this.props.history.push('/resume-builder/edit/?type=skill')
    }

    componentDidMount() {
        this.props.fetchUserEducation()
    }

    handleAddition(fields, error, event) {
        event.stopPropagation();
        fields.push({
            "candidate_id": '',
            "id": '',
            "specialization": '',
            "institution_name": '',
            "course_type": '',
            "start_date": '',
            "percentage_cgpa": '',
            "end_date": '',
            "is_pursuing": false,
            order: fields.length
        })
    }

    deleteEducation(index, fields, event) {
        event.stopPropagation();
        const education = fields.get(index);
        fields.remove(index);
        if (education && education.id) {
            this.props.removeEducation(education.id)
        }
    }

    render() {
        const {handleSubmit, education} = this.props;
        const renderEducation = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Education</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline"
                            onClick={(event) => this.handleAddition(fields, error, event)}
                            type={'button'}>+ Add new</button>
                    </div>
                    {fields.map((member, index) => {
                        return(
                            <React.Fragment key={index}>
                                <div className="subHeading pb-0">
                                    <h2>{education.specialization}</h2>
                                    <ul className="subHeading__control">
                                        <li className="subHeading__delete">
                                            <span className="sprite icon--delete" 
                                            onClick={(event) => this.deleteEducation(index, fields, event)}
                                            role="button"></span>
                                        </li>
                                        <li className="subHeading__btn">
                                            <i className="sprite icon--upArrow"></i>
                                        </li>
                                        <li className="subHeading__btn">
                                            <i className="sprite icon--downArrow"></i>
                                        </li>
                                    </ul>
                                </div>

                                <ul className="form pb-0">
                                    <li className="form__group">
                                        <label className="form__label" htmlFor="institution_name">Institution Name </label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                                <span className="input-group__text">
                                                    <i className="sprite icon--education-grey"></i>
                                                </span>
                                            </div>
                                            <Field component={renderField} type={"text"} name={`${member}.institution_name`}
                                            className="form__input"/>
                                        </div>
                                    </li>

                                    <li className="form__group">
                                        <label className="form__label" htmlFor="specialization">Specialization</label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                                <span className="input-group__text">
                                                    <i className="sprite icon--date"></i>
                                                </span>
                                            </div>
                                            <Field component={renderField} type={"text"}
                                            name={`${member}.specialization`} className="form__input"/>
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
                                            name={`${member}.start_date`} className="form__input"/>
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
                                            name={`${member}.end_date`} className="form__input"/>
                                        </div>
                                    </li>

                                    <li className="form__radio-group d-flex justify-content-end fs-14">
                                        <input class="form__radio-input" type="radio" name={`${member}.is_pursuing`}
                                            checked={`${member}.is_pursuing` === 'true' ? true : false}  />
                                        <label class="form__radio-label" htmlFor="tillToday">
                                            <span className="form__radio-button"></span>
                                            Till today
                                    </label>
                                    </li>

                                    <li className="form__group">
                                        <label className="form__label" htmlFor="course_type">Course Type</label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                                <span className="input-group__text">
                                                    <i className="sprite icon--date"></i>
                                                </span>
                                            </div>
                                            <Field component={renderSelect} type={"text"}
                                                name={`${member}.course_type`}
                                                options={[
                                                    {value: 'FT', label: 'FULL TIME'},
                                                    {value: 'PT', label: 'PART TIME'},
                                                ]}
                                                className="form__input"  id="course_type" 
                                                aria-label="course_type"/>
                                        </div>
                                    </li>

                                    <li className="form__group">
                                        <label className="form__label" htmlFor="percentage_cgpa">Percentage/CGPA</label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                                <span className="input-group__text">
                                                    <i className="sprite icon--date"></i>
                                                </span>
                                            </div>
                                            <Field component={renderField} type={"text"} 
                                            name={`${member}.percentage_cgpa`} className="form__input"/>
                                        </div>
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
                    <FieldArray name={'list'} component={renderEducation}/> 
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

export const EducationForm = reduxForm({
    form: 'education',
    enableReinitialize: true
})(Education);


const mapStateToProps = (state) => {
    return {
        initialValues: state.education,
        education: state.education
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userEducation) => {
            const {start_date, end_date, course_type} = userEducation;

            userEducation = {
                ...userEducation,
                ...{
                    start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                    end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                    course_type: course_type && course_type.value
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserEducation({userEducation, resolve, reject}));
            })
        },
        "fetchUserEducation": () => {
            return dispatch(actions.fetchUserEducation())
        },
        "removeEducation": (educationId) => {
            return dispatch(actions.deleteEducation(educationId))
        },

        "bulkUpdateUserEducation": (listItems) => {
            listItems = (listItems || []).map(userEducation => {
                    const {start_date, end_date, course_type} = userEducation;
                    if (!userEducation['id']) delete userEducation['id'];
                    userEducation = {
                        ...userEducation,
                        ...{
                            start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                            end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                            course_type: course_type && course_type.value
                        }
                    };
                    return userEducation;
                }
            );
            return dispatch(actions.bulkUpdateUserEducation({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
