import React, {Component} from 'react';
import './skill.scss'
import {Field, reduxForm, FieldArray} from "redux-form"
import * as actions from "../../../../../../store/skill/actions";
import {connect} from "react-redux";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";

import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton
} from 'react-accessible-accordion';

import validate from '../../../../../FormHandler/validations/skillValidation.js'
import Loader from "../../../../../Loader/loader.jsx";


/*
styles
* */
import 'react-accessible-accordion/dist/fancy-example.css';

class Skill extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAccordionState = this.handleAccordionState.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteSkill = this.deleteSkill.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);

        this.state = {
            currentAccordion: 0,
            previousAccordion: 0,
            openedAccordion: 0,

        }
    }

    componentDidMount() {
        this.props.fetchUserSkill();
    }

    async handleSubmit(values) {
        const {list} = values;
        if (list.length) {
            await this.props.onSubmit(list[list.length - 1]);
            this.props.history.push('/resume-builder/edit/?type=language')
        }
    }

    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        console.log('donw pressed');
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.swap(index, index + 1);
        this.props.handleSwap([currentItem, nextItem])
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        console.log('up pressed');
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.swap(index, index - 1);
        this.props.handleSwap([currentItem, prevItem])

    }

    handleAddition(fields, error) {
        const listLength = fields.length;

        if (listLength) this.handleAccordionState(listLength, fields);
        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": {
                value: 5, 'label': '5'
            },
            order: listLength
        })

    }

    deleteSkill(index, fields, event) {
        event.stopPropagation();
        const skill = fields.get(index);
        fields.remove(index);
        if (skill && skill.id) {
            this.props.removeSkill(skill.id)
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
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize, skill, ui: {loader}} = this.props;

        const renderSkills = ({fields, loader, meta: {touched, error, submitFailed}}) => {
            return (

                <div>
                    {!!loader &&
                    <Loader/>
                    }
                    <section className="head-section">
                        <span className="icon-box"><i className="icon-skills1"/></span>
                        <h2>Skills</h2>
                        {/*<span className="icon-edit icon-education__cursor"></span>*/}
                        <button onClick={this.handleAddition.bind(this, fields, error)}
                                type={'button'}
                                className="add-button add-button__right">Add new
                        </button>
                    </section>
                    <section className="right-sidebar-scroll">
                        <ul>
                            <Accordion onChange={(value) => this.handleAccordionClick(value, fields, error)}
                                       allowZeroExpanded={true}
                                       preExpanded={[this.state.openedAccordion]}>
                                {fields.map((member, index) => {
                                    return (
                                        <li key={index}>
                                            <section className="info-section">
                                                <AccordionItem uuid={index}>
                                                    <AccordionItemHeading>
                                                        <AccordionItemButton>
                                                            <div className="flex-container">
                                                                <h3 className="add-section-heading">{fields.get(index).name || 'Skill'}</h3>
                                                                <div className="addon-buttons mr-10">
                                                                <span
                                                                    onClick={(event) => this.deleteSkill(index, fields, event)}
                                                                    className="icon-delete mr-15"/>
                                                                    {index !== 0 &&
                                                                    <span
                                                                        onClick={(event) => this.changeOrderingUp(index, fields, event)}
                                                                        className="icon-ascend mr-5"/>
                                                                    }
                                                                    {
                                                                        index !== fields.length - 1 &&
                                                                        < span
                                                                            onClick={(event) => this.changeOrderingDown(index, fields, event)}
                                                                            className="icon-descend"/>
                                                                    }
                                                                </div>
                                                            </div>
                                                        </AccordionItemButton>
                                                    </AccordionItemHeading>
                                                    <AccordionItemPanel>
                                                        <div className="flex-container">
                                                            <fieldset>
                                                                <label>Skill name</label>
                                                                <div className="input-group">
                                                                    <div className="input-group--input-group-icon">
                                                                        <span className="icon-skills-gr"></span>
                                                                    </div>
                                                                    <Field component={renderField}
                                                                           type={"text"} name={`${member}.name`}
                                                                           className={"input-control"}/>
                                                                </div>
                                                            </fieldset>

                                                            <fieldset className="custom">
                                                                <label>Skill rating (out of 10)</label>
                                                                <div className="input-group">
                                                                    <div className="input-group--input-group-icon">
                                                                        <span className="icon-blank"></span>
                                                                    </div>
                                                                    <Field name={`${member}.proficiency`}
                                                                           component={renderSelect}
                                                                           isMulti={false}
                                                                           options={[
                                                                               {value: 1, label: '1'},
                                                                               {value: 2, label: '2'},
                                                                               {value: 3, label: '3'},
                                                                               {value: 4, label: '4'},
                                                                               {value: 5, label: '5'},
                                                                               {value: 6, label: '6'},
                                                                               {value: 7, label: '7'},
                                                                               {value: 8, label: '8'},
                                                                               {value: 9, label: '9'},
                                                                               {value: 10, label: '10'}
                                                                           ]}
                                                                    />
                                                                </div>
                                                            </fieldset>
                                                            <Field component={'input'} name={`${member}.id`}
                                                                   type={'text'}
                                                                   hidden={true}/>

                                                        </div>

                                                    </AccordionItemPanel>
                                                </AccordionItem>
                                            </section>
                                        </li>
                                    )
                                })}
                            </Accordion>
                        </ul>
                    </section>
                </div>

            )
        }

        return (
            <div>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" loader={loader} component={renderSkills}/>
                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type={'submit'}>Save & Continue</button>
                    </div>
                </form>
            </div>
        )
    }
}


export const SkillForm = reduxForm({
    form: 'Skill',
    enableReinitialize: true,
    validate

})(Skill);


const mapStateToProps = (state) => {
    return {
        initialValues: state.skill,
        skill: state.skill,
        ui:state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userSkill) => {
            const {proficiency} = userSkill;
            userSkill = {
                ...userSkill,
                ...{
                    proficiency: proficiency && proficiency.value
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserSkill({userSkill, resolve, reject}));
            })
        },
        "fetchUserSkill": () => {
            return dispatch(actions.fetchUserSkill())
        },
        "removeSkill": (skillId) => {
            return dispatch(actions.deleteSkill(skillId))
        },
        "handleSwap": (listItems) => {
            listItems = (listItems || []).map(userSkill => {
                const {proficiency} = userSkill;
                if (!userSkill['id']) delete userSkill['id'];
                userSkill = {
                    ...userSkill,
                    ...{
                        proficiency: proficiency && proficiency.value
                    }
                };
                return userSkill;
            })
            return dispatch(actions.handleSkillSwap({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
