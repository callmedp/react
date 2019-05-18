import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/education/actions";
import {connect} from "react-redux";
import moment from "moment";
import {EducationRenderer} from "./educationRenderer";
import validate from '../../../../../FormHandler/validations/education/validate';
import {scroller} from "react-scroll/modules";


class Education extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteEducation = this.deleteEducation.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false,
            till_today: [],
        }
        this.props.currentForm('education');

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
        let {formData: {education: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit) this.props.bulkUpdateOrCreate(values && values['list'])
    }

    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let {till_today} = this.state
        till_today[parseInt(index)] = checked
    }

    componentDidMount() {
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.is_pursuing)
        }
        this.setState({till_today})
        this.props.fetchUserEducation()
    }

    componentDidUpdate(prevProps) {
        if (this.props.initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of this.props.initialValues.list) {
                till_today.push(i.is_pursuing)
            }
            this.setState({till_today})
        }
    }


    handleAddition(fields, error, event) {
        const listLength = fields.length;
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
            order: listLength
        })

        scroller.scrollTo(`education${fields.length -1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 350,
            containerId:'education'
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

    handleAccordionClick(value, fields) {
        this.setState({active: value})
    }

    render() {
        const {
            handleSubmit, ui: {loader}, saveTitle, isEditable,
            editHeading, entityName, nextEntity, handlePreview, changeOrderingUp
            , changeOrderingDown
        } = this.props;
        const {till_today} = this.state

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name={'list'}
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAddition={this.handleAddition}
                            deleteEducation={this.deleteEducation}
                            changeOrderingUp={changeOrderingUp}
                            changeOrderingDown={changeOrderingDown}
                            component={EducationRenderer}
                            saveTitle={(event) => saveTitle(event, 1)}
                            editHeading={(value) => editHeading(value)}
                            isEditable={isEditable}
                            entityName={entityName}
                            expanded={this.state.active}
                            till_today={till_today}
                            tillTodayDisable={this.tillTodayDisable}
                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" onClick={handlePreview}>Preview</button>
                    <button className="orange-button"
                            type={'submit'}>{!nextEntity ? "Download" : 'Save and Continue'}</button>
                </div>

            </form>
        )
    }
}


export const EducationForm = reduxForm({
    form: 'education',
    enableReinitialize: true,
    validate
})(Education);


const mapStateToProps = (state) => {
    return {
        initialValues: state.education,
        ui: state.ui,
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

        "bulkUpdateOrCreate": (listItems) => {
            console.log('---education list--', listItems);
            listItems = (listItems || []).map((userEducation, index) => {
                    const {start_date, end_date, course_type} = userEducation;
                    if (!userEducation['id']) delete userEducation['id'];
                    userEducation = {
                        ...userEducation,
                        ...{
                            start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                            end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                            course_type: course_type && course_type.value,
                            order: index
                        }
                    };
                    return userEducation;
                }
            );
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserEducation({list: listItems, resolve, reject}))
            })

        },

    }

};

export default connect(mapStateToProps, mapDispatchToProps)(EducationForm);
