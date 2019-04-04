import React, {Component} from 'react';
import './skill.scss'
import {Field, reduxForm} from "redux-form"
import * as actions from "../../../../../store/skill/actions";
import {connect} from "react-redux";
import {renderField} from "../../../../FormHandler/formFieldRenderer.jsx";


class Skill extends Component {

    componentDidMount() {
        this.props.fetchUserSkill();
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-skills1"></i></span>
                    <h2>Skills</h2>
                    <span className="icon-edit icon-education__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>

                <section className="right-sidebar-scroll">
                    <section className="info-section">
                        <div className="flex-container">
                            <h3 className="add-section-heading">Skill1</h3>
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
				        			<select selected>
				        				<option></option>
				        				<option>1</option>
				        				<option>2</option>
				        				<option>3</option>
				        			</select>	
			        			</span>
                            </fieldset>
                        </div>

                    </section>


                </section>

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10">Preview</button>
                    <button className="orange-button">Save & Continue</button>
                </div>
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
        initialValues: state.skill
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserSkill": () => {
            return dispatch(actions.fetchUserSkill())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
