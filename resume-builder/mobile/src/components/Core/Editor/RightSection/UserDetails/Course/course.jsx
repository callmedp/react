import React, {Component} from 'react';
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/course/actions";
import {connect} from "react-redux";
import {renderField, datepicker} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {required} from "../../../../../FormHandler/formValidations"
import moment from "moment";

class Course extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteCourse = this.deleteCourse.bind(this);
    }
    
    componentDidMount() {
        this.props.fetchUserCourse()
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=project')
    }
    
    handleAddition(fields, error) {

        fields.push({
            "candidate_id": '',
            "id": '',
            "name_of_certification": '',
            "year_of_certification": '',
            order: fields.length
        })
    }

    deleteCourse(index, fields, event) {
        event.stopPropagation();
        const course = fields.get(index);
        fields.remove(index);
        if (course && course.id) {
            this.props.removeCourse(course.id)
        }
    }

    render () {
        const {handleSubmit, course} = this.props;
        const renderCourse = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Courses</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline"
                        onClick={this.handleAddition.bind(this, fields, error)}
                        type={'button'}>+ Add new</button>
                    </div>
                    {fields.map((member, index) => {
                    return (
                        <React.Fragment>
                            <div className="subHeading pb-0">
                                <h2>{course.name_of_certification}</h2>
                                <ul className="subHeading__control">
                                    <li className="subHeading__delete">
                                        <span className="sprite icon--delete" 
                                        onClick={(event) => this.deleteCourse(index, fields, event)}
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
                                    <label className="form__label" htmlFor="name_of_certification">Course name</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--course-grey"></i>
                                            </span>
                                        </div>
                                        <Field component={renderField} validate={required} className="form__input"
                                            type={"text"} name={`${member}.name_of_certification`}/>
                                    </div>
                                </li>

                                <li className="form__group">
                                    <label className="form__label" htmlFor="year_of_certification">Completion Year</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--date"></i>
                                            </span>
                                        </div>
                                        <Field component={datepicker} validate={required} type={"date"} 
                                        name={`${member}.year_of_certification`} className="form__input" />
                                    </div>
                                </li>
                            </ul>
                        </React.Fragment>
                    )})}
                </div>

            )
        }
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
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

export const CourseForm = reduxForm({
    form: 'course',
    enableReinitialize: true
})(Course);


const mapStateToProps = (state) => {
    return {
        initialValues: state.course,
        course: state.course
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userCourse) => {
            const {year_of_certification} = userCourse;
            userCourse = {
                ...userCourse,
                ...{
                    year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                }
            };
            console.log(userCourse)
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserCourse({userCourse, resolve, reject}));
            })
        },
        "fetchUserCourse": () => {
            return dispatch(actions.fetchUserCourse())
        },
        "removeCourse": (courseId) => {
            return dispatch(actions.deleteCourse(courseId))
        },

        "handleSwap": (listItems) => {
            listItems = (listItems || []).map(userCourse => {
                const {year_of_certification} = userCourse;
                if (!userCourse['id']) delete userCourse['id'];
                userCourse = {
                    ...userCourse,
                    ...{
                        year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                    }
                };
                return userCourse;
            })
            return dispatch(actions.handleCourseSwap({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(CourseForm);
