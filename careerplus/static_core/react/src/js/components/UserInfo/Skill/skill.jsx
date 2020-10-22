import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';

export class Skill extends React.Component {
    constructor(props) {
        super(props);
        const {userId, history} = props;
        // if (!userId) history.push('/resume-builder/register');

    }

    handleAddSkill(invalid, skills, skillValues, reset, userId) {
        if (invalid) return;
        let skillList = skills || [];
        skillList.push({
            ...skillValues,
            user: userId
        });
        this.props.addSkill({skills: skillList});
        reset();
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, skills, skillValues, invalid, userId} = this.props;
        return (
            <div className="register login-signup-box">
                <h1 className="modal-title">Add My Skill</h1>

                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="name" component={renderField} validate={required}
                                   label="Skill Name"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="proficiency" component={renderField} validate={required}
                                   label="Skill Proficiency"/>
                        </div>
                    </div>

                    <div className={'Button-group'}>
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} type="button" onClick={() => {
                                this.props.history.goBack()
                            }}>
                                Back
                            </button>
                        </div>
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} type="button" onClick={
                                this.handleAddSkill.bind(this, invalid, skills, skillValues, reset, userId)
                            }>
                                Add
                            </button>
                        </div>
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} type="button">
                                Preview
                            </button>
                        </div>
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} type="submit" disabled={pristine || submitting}>
                                Next
                            </button>
                        </div>
                    </div>
                </form>
                {error && <div className={'Api-error'}>
                    <span>{error}</span>
                </div>
                }
                {
                    !!(skills && skills.length) &&
                    <div className={'Project-list'}>
                        <span className={'Project-heading'}>SKILLS:</span>
                        {
                            (skills || []).map(skill => (
                                <button>{skill['name']}</button>
                            ))
                        }
                    </div>
                }
            </div>
        );
    }
}


export const SkillForm = reduxForm({
    form: 'skillForm',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/experience'
        })
    }
})(Skill);


const mapStateToProps = (state) => {
    return {
        skillValues: state.form && state.form.skillForm && state.form.skillForm.values || {},
        skills: state.userInfoReducer.skills,
        userId: state.userInfoReducer.id,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userSkill) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserSkill({userSkill, resolve, reject}))
        }),
        "addSkill": (skill) => {
            return dispatch(actions.addSkill(skill))
        }
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);

