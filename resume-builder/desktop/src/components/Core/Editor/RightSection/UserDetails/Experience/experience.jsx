import React, {Component} from 'react';
import './experience.scss'
import {renderField, renderTextArea, datepicker} from '../../../../../FormHandler/formFieldRenderer.jsx'
import {Field, reduxForm, FieldArray} from 'redux-form';
import * as actions from '../../../../../../store/experience/actions/index';
import {connect} from "react-redux";
import moment from 'moment';
import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';

import validate from '../../../../../FormHandler/validations/experience/validate'


const ExperienceRenderer = ({
                                fields,
                                loader,
                                meta: {touched, error, submitFailed},
                                deleteExperience,
                                handleAddition,
                                handleSubmit,
                                handleAccordionState,
                                handleAccordionClick,
                                changeOrderingUp,
                                changeOrderingDown,
                                openedAccordion,
                                editHeading,
                                saveTitle,
                                isEditable,
                                entityName
                            }) => {
    let elem = null;

    return (
        <div>
            <section className="head-section">
                <span className="icon-box"><i className="icon-experience1"/></span>
                <h2 ref={(value) => {
                    elem = value
                }} onKeyUp={(event) => saveTitle(event)}
                    contenteditable={isEditable ? "true" : "false"}>{entityName}</h2>
                <span onClick={() => editHeading(elem)}
                      className={!!(!isEditable) ? "icon-edit icon-experience__cursor" : ''}/>

                <button
                    onClick={handleSubmit((values) => {
                        handleAddition(fields, error)
                    })}
                    type={'button'}
                    className="add-button add-button__right">Add new
                </button>

            </section>


            <section className="right-sidebar-scroll">
                <ul>
                    <Accordion onChange={(value) => handleAccordionClick(value, fields, error)}
                               allowZeroExpanded={true}
                               preExpanded={[openedAccordion]}>
                        {
                            fields.map((member, index) => {
                                return (
                                    <li key={index}>
                                        <section className="info-section">
                                            <AccordionItem uuid={index}>
                                                <AccordionItemHeading>
                                                    <AccordionItemButton>
                                                        <div className="flex-container">
                                                            <h3 className="add-section-heading">{fields.get(index).company_name || 'Experience'}</h3>
                                                            <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => deleteExperience(index, fields, event)}
                                                                    className="icon-delete mr-15"/>
                                                                {index !== 0 &&
                                                                <span
                                                                    onClick={(event) => changeOrderingUp(index, fields, event)}
                                                                    className="icon-ascend mr-5"/>
                                                                }
                                                                {
                                                                    index !== fields.length - 1 &&
                                                                    < span
                                                                        onClick={(event) => changeOrderingDown(index, fields, event)}
                                                                        className="icon-descend"/>
                                                                }
                                                            </div>
                                                        </div>
                                                    </AccordionItemButton>
                                                </AccordionItemHeading>
                                                <AccordionItemPanel>
                                                    <div className="flex-container">
                                                        <fieldset className="error">
                                                            <label>Designation</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-designation"/>
                                                                </div>
                                                                <Field component={renderField}
                                                                       type={"text"}
                                                                       name={`${member}.job_profile`}/>
                                                            </div>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Company Name</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-company"/>
                                                                </div>
                                                                <Field component={renderField}
                                                                       type={"text"}
                                                                       name={`${member}.company_name`}/>
                                                            </div>
                                                        </fieldset>
                                                    </div>
                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Date from</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-date"/>
                                                                </div>
                                                                <Field component={datepicker}
                                                                       type={"date"}
                                                                       className={'input-control'}
                                                                       name={`${member}.start_date`}/>
                                                            </div>
                                                        </fieldset>
                                                        <fieldset>
                                                            <label>Date to</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-date"/>
                                                                </div>
                                                                <Field component={datepicker}
                                                                       type={"date"}
                                                                       name={`${member}.end_date`}
                                                                       className={'input-control'}/>
                                                            </div>
                                                            <span className="till-today">
									                                    <Field type="checkbox"
                                                                               name={`${member}.is_working`}
                                                                               component="input"
                                                                               checked={`${member}.is_working` === 'true' ? true : false}/>
								                                	Till Today
							                                    	</span>
                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Job Location</label>
                                                            <div className="input-group">
                                                                <div className="input-group--input-group-icon">
                                                                    <span className="icon-address"/>
                                                                </div>
                                                                <Field component={renderField} type={"text"}
                                                                       name={`${member}.job_location`}
                                                                       className={"input-control"}/>
                                                            </div>
                                                        </fieldset>
                                                    </div>

                                                    <div className="flex-container">
                                                        <fieldset>
                                                            <label>Description</label>
                                                            <Field component={renderTextArea} rows={"3"}
                                                                   type={"text"}
                                                                   name={`${member}.work_description`}/>
                                                        </fieldset>
                                                    </div>

                                                </AccordionItemPanel>
                                            </AccordionItem>
                                        </section>
                                    </li>
                                )
                            })
                        }
                    </Accordion>
                </ul>
            </section>

        </div>
    )

}

class Experience extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteExperience = this.deleteExperience.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,
        }
    }

    componentDidMount() {
        this.props.fetchUserExperience()
    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.onSubmit(list[list.length - 1]);
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }

    }


    changeOrderingDown(index, fields, event) {
        event.stopPropagation()
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.swap(index, index + 1);
        this.props.handleSwap([currentItem, nextItem]);
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.swap(index, index - 1)
        this.props.handleSwap([currentItem, prevItem])

    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        if (listLength) this.handleAccordionState(listLength, fields);
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


    handleAccordionState(val, fields) {
        const {currentAccordion} = this.state;

        if (currentAccordion !== '') {
            this.props.onSubmit(fields.get(currentAccordion))
        }

        this.setState((state) => ({
            previousAccordion: state.currentAccordion,
            openedAccordion: val,
            currentAccordion: val
        }))
    }

    handleAccordionClick(value, fields) {
        const val = value.length > 0 ? value[0] : '';
        this.handleAccordionState(val, fields)
    }

    render() {
        const {handleSubmit, ui: {loader}, isEditable,
            editHeading, saveTitle, entityName, nextEntity,handlePreview} = this.props;

        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray name={"list"}
                            loader={loader}
                            handleSubmit={handleSubmit}
                            handleAccordionClick={this.handleAccordionClick}
                            handleAccordionState={this.handleAccordionState}
                            handleAddition={this.handleAddition}
                            deleteExperience={this.deleteExperience}
                            changeOrderingUp={this.changeOrderingUp}
                            changeOrderingDown={this.changeOrderingDown}
                            openedAccordion={this.state.openedAccordion}
                            component={ExperienceRenderer}
                            saveTitle={(event) => saveTitle(event, 2)}
                            editHeading={(value) => editHeading(value)}
                            isEditable={isEditable}
                            entityName={entityName}
                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" type="button" onClick={handlePreview}>Preview</button>
                    <button className="orange-button" type="submit">Save & Continue</button>
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

        "handleSwap": (listItems) => {
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
            return dispatch(actions.handleExperienceSwap({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ExperienceForm);
