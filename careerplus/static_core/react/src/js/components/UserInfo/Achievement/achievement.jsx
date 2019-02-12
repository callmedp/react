import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';

export class Achievement extends React.Component {
    constructor(props) {
        super(props);
        this.handleAddAchievement.bind(this);

    }

    handleAddAchievement(invalid, achievements, achievementValues, reset, userId) {
        if (invalid) return;
        let achievementList = achievements || [];
        achievementList.push({
            ...achievementValues,
            user: userId
        });
        this.props.addAchievement({achievements: achievementList});
        reset();

    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, achievements, achievementValues, invalid, userId} = this.props;
        return (
            <div className="container pr">
                <header className="login-page-bg">
                    <div className="login-bg-txt">
                        <figure className="login-icon1"></figure>
                        <strong>1 Lacs+</strong>
                        Satisfied users
                    </div>
                    <div className="login-bg-txt">
                        <figure className="login-icon2"></figure>
                        <strong>300+</strong>
                        Courses
                    </div>
                    <div className="login-bg-txt">
                        <figure className="login-icon3"></figure>
                        <strong>500+</strong>
                        Professional resumes delivered
                    </div>
                </header>

                <div className="register login-signup-box">
                    <h1 className="modal-title">Add Your Awards</h1>

                    <form onSubmit={handleSubmit}>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field type="text" name="title" component={renderField} validate={required}
                                       label="Title"/>
                            </div>
                        </div>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field type="date" name="date" component={datePicker} validate={required}
                                       label="Date"/>
                            </div>
                        </div>
                        <div className={'Text-spacing'}>
                            <div>
                                <Field type="text" name="summary" component={renderTextArea} validate={required}
                                       label="Summary"/>
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
                                    this.handleAddAchievement.bind(this, invalid, achievements, achievementValues, reset, userId)
                                }>
                                    Add
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
                        !!(achievements && achievements.length) &&
                        <div className={'Project-list'}>
                            <span className={'Project-heading'}>Achievements:</span>
                            {
                                (achievements || []).map(achievement => (
                                    <button>{achievement['title']}</button>
                                ))
                            }
                        </div>
                    }
                </div>
            </div>
        );
    }
}


export const AchievementForm = reduxForm({
    form: 'achievementForm',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/reference'
        })
    }
})(Achievement);


const mapStateToProps = (state) => {
    return {
        achievementValues: state.form && state.form.achievementForm && state.form.achievementForm.values || {},
        achievements: state.userInfoReducer.achievements,
        userId: state.userInfoReducer.id,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userAchievement) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserAchievement({userAchievement, resolve, reject}))
        }),
        "addAchievement": (achievement) => {
            return dispatch(actions.addAchievement(achievement))
        }
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(AchievementForm);

