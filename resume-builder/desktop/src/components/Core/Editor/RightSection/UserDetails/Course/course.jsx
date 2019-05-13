import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/course/actions";
import {connect} from "react-redux";
import validate from "../../../../../FormHandler/validations/course/validate"
import moment from "moment";
import {CourseRenderer} from "./courseRenderer";

class Course extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteCourse = this.deleteCourse.bind(this);

        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false

        }
    }

    componentDidMount() {
        this.props.fetchUserCourse()
    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            this.setState({
                submit: true
            })
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }

    }


    componentWillUnmount() {
        let {formData: {course: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el).map(key => (!!el[key] ? error = true : false)))
        if (!error &&  !this.state.submit) this.props.bulkUpdateOrCreate(values && values['list'])

    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        fields.push({
            "candidate_id": '',
            "id": '',
            "name_of_certification": '',
            "year_of_certification": '',
            order: listLength
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

    handleAccordionClick(value) {
        this.setState({active: value})
    }

    render() {
        const {
            handleSubmit, ui: {loader}, editHeading, saveTitle, isEditable,
            entityName, nextEntity, handlePreview, changeOrderingUp, changeOrderingDown
        } = this.props;

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name={'list'}
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAddition={this.handleAddition}
                            deleteCourse={this.deleteCourse}
                            changeOrderingUp={changeOrderingUp}
                            changeOrderingDown={changeOrderingDown}
                            component={CourseRenderer}
                            saveTitle={(event) => saveTitle(event, 7)}
                            editHeading={(value) => editHeading(value)}
                            isEditable={isEditable}
                            entityName={entityName}
                            expanded={this.state.active}

                />
                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" type={'button'} onClick={handlePreview}>Preview</button>
                    <button className="orange-button" type={'submit'}>{!nextEntity ? "Download": 'Save and Continue'}</button>
                </div>
            </form>

        )
    }
}


export const
    CourseForm = reduxForm({
        form: 'course',
        enableReinitialize: true,
        validate
    })(Course);


const
    mapStateToProps = (state) => {
        return {
            initialValues: state.course,
            ui: state.ui
        }
    };

const
    mapDispatchToProps = (dispatch) => {
        return {
            "onSubmit": (userCourse) => {
                const {year_of_certification} = userCourse;
                userCourse = {
                    ...userCourse,
                    ...{
                        year_of_certification: (year_of_certification && moment(year_of_certification).format('YYYY')) || '',
                    }
                };
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

            "bulkUpdateOrCreate": (listItems) => {
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
                });
                return new Promise((resolve, reject) => {
                    return dispatch(actions.bulkUpdateOrCreateUserCourse({list: listItems, resolve, reject}))
                })

            },
        }
    };

export default connect(mapStateToProps, mapDispatchToProps)

(
    CourseForm
)
;
