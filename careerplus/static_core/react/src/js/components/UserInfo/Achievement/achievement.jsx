import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';
import PreviewResumeModal from "../../Modal/PreviewResume/previewResumeModal.jsx";

export class Achievement extends React.Component {
    constructor(props) {
        super(props);
        const {userId, history} = props;
        this.state = {
            showModal: false,
            html: ''
        }
        // if (!userId) history.push('/resume-builder/register');

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

    async handleOpenModal() {

        let html = await this.props.showPreview()

        this.setState({
            'html': html
        })

        this.setState({
            'showModal': true
        })

    }

    handleCloseModal() {
        this.setState({
            'showModal': false
        })
    }


    render() {
        const {error, handleSubmit, pristine, reset, submitting, achievements, achievementValues, invalid, userId, showPreview} = this.props;
        return (
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
                            <button className={'Submit-button'} type="button" onClick={this.handleOpenModal.bind(this)}>
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
                <PreviewResumeModal showModal={this.state.showModal} html={this.state.html}
                                    closeModal={this.handleCloseModal.bind(this)}/>

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
        },
        "showPreview": () => new Promise((resolve, reject) => {
            return dispatch(actions.showResumePreview({resolve, reject}))
        })

    }

};

export default connect(mapStateToProps, mapDispatchToProps)(AchievementForm);

