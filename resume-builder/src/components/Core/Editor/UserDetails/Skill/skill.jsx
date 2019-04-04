import React, {Component} from 'react';
import './skill.scss'
import {Field, reduxForm} from "redux-form"
import * as actions from "../../../../../store/skill/actions";
import {connect} from "react-redux";
import {renderField, renderSelect} from "../../../../FormHandler/formFieldRenderer";
import moment from "moment";


class Skill extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    componentDidMount() {
        this.props.fetchUserSkill();
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=language')
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize, skill} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-skills1"></i></span>
                    <h2>Skills</h2>
                    <span className="icon-edit icon-education__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <h3 className="add-section-heading">{skill.name}</h3>
                                <div className="addon-buttons mr-10">
                                    <span className="icon-delete mr-15"></span>
                                    <span className="icon-ascend mr-5"></span>
                                    <span className="icon-descend"></span>
                                </div>
                            </div>
                            <div className="flex-container">
                                <fieldset className="width-half">
                                    <label>Skill name</label>
                                    <Field component={renderField} type={"text"} name="name"/>
                                </fieldset>

                                <fieldset className="width-half">
                                    <label>Skill rating (out of 10)</label>
                                    <span className="styled-select">
				        			<Field name="proficiency"
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
                                           ]}/>
			        			</span>
                                </fieldset>
                            </div>

                        </section>


                    </section>

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
    enableReinitialize: true
})(Skill);


const mapStateToProps = (state) => {
    return {
        initialValues: state.skill,
        skill: state.skill
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userSkill) => {
            const {proficiency} = userSkill
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
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
