import React, {Component} from 'react';
import {renderField, renderTextArea, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {Field, reduxForm, FieldArray} from 'redux-form';
import * as actions from '../../../../../../store/experience/actions/index';
import {connect} from "react-redux";
import moment from 'moment';
import {ExperienceRenderer} from "./experienceRenderer";
import validate from '../../../../../FormHandler/validations/experience/validate'
import {scroller, Events, animateScroll as scroll} from "react-scroll/modules";


class Experience extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteExperience = this.deleteExperience.bind(this);
        this.tillTodayDisable = this.tillTodayDisable.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false,
            till_today: [],

        };
        this.props.currentForm('experience');

    }

    componentDidMount() {
        this.props.fetchUserExperience()
        let till_today = []
        for (let i of this.props.initialValues.list) {
            till_today.push(i.is_working)
        }
        this.setState({till_today})


        Events.scrollEvent.register('begin', function () {
            console.log("begin");
        });

        Events.scrollEvent.register('end', function () {
            console.log("end");
        });
    }

    componentDidUpdate(prevProps) {
        if (this.props.initialValues.list !== prevProps.initialValues.list) {
            let till_today = []
            for (let i of this.props.initialValues.list) {
                till_today.push(i.is_working)
            }
            this.setState({till_today})
        }
    }


    componentWillUnmount() {
        Events.scrollEvent.remove('begin');
        Events.scrollEvent.remove('end');
        let {formData: {experience: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit) this.props.bulkUpdateOrCreate(values && values['list'])

    }

    tillTodayDisable(index, checked, e) {
        e.stopPropagation();
        let {till_today} = this.state;
        till_today[parseInt(index)] = checked
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

    handleAddition(fields, error) {
        const listLength = fields.length;

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
            order: listLength
        })

        scroll.scrollTo(500)
    }

    deleteExperience(index, fields, event) {
        event.stopPropagation();
        const experience = fields.get(index);
        fields.remove(index);
        if (experience && experience.id) {
            this.props.removeExperience(experience.id)
        }
    }


    handleAccordionClick(value, fields) {
        this.setState({active: value})
    }

    render() {
        const {
            handleSubmit, ui: {loader}, isEditable,
            editHeading, saveTitle, entityName, nextEntity, handlePreview,
            changeOrderingDown, changeOrderingUp

        } = this.props;
        const {till_today} = this.state;

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name={"list"}
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAddition={this.handleAddition}
                            deleteExperience={this.deleteExperience}
                            changeOrderingUp={changeOrderingUp}
                            changeOrderingDown={changeOrderingDown}
                            component={ExperienceRenderer}
                            saveTitle={(event) => saveTitle(event, 2)}
                            editHeading={(value) => editHeading(value)}
                            isEditable={isEditable}
                            entityName={entityName}
                            expanded={this.state.active}
                            till_today={till_today}
                            tillTodayDisable={this.tillTodayDisable}
                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" type="button" onClick={handlePreview}>Preview</button>
                    <button className="orange-button"
                            type="submit">{!nextEntity ? "Download" : 'Save and Continue'}</button>
                </div>
            </form>
        )
    }
}

export const ExperienceForm = reduxForm({
    form: 'experience',
    enableReinitialize: true,
    validate
})(Experience);


const mapStateToProps = (state) => {
    return {
        initialValues: state.experience,
        ui: state.ui,
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

        "bulkUpdateOrCreate": (listItems) => {
            listItems = (listItems || []).map((userExperience, index) => {
                const {start_date, end_date} = userExperience;
                if (!userExperience['id']) delete userExperience['id'];
                userExperience = {
                    ...userExperience,
                    ...{
                        start_date: (start_date && moment(start_date).format('YYYY-MM-DD')) || '',
                        end_date: (end_date && moment(end_date).format('YYYY-MM-DD')) || '',
                        order: index

                    }
                };
                return userExperience;
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserExperience({list: listItems, resolve, reject}))
            })

        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ExperienceForm);
