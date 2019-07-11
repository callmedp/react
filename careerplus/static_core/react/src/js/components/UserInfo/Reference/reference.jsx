import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';
import ChoosePlanModal from '../../Modal/ChoosePlan/choosePlanModal.jsx'

export class Reference extends React.Component {
    constructor(props) {
        super(props);
        const {userId, history} = props;
        if (!userId) history.push('/resume-builder/register');
        this.state = {
            'showModal': false
        }
    }


    handleAddReference(invalid, references, referenceValues, reset, userId) {
        if (invalid) return;
        let referenceList = references || [];
        referenceList.push({
            ...referenceValues,
            user: userId
        });
        this.props.addReference({references: referenceList});
        reset();

    }

    handleOpenModal() {
        this.setState({
            'showModal': true
        })
    }

    handleCloseModal() {
        this.setState({
            'showModal': false
        })
        const {history} = this.props;
        history.push({
            pathname: '/resume-builder/pricing'
        })

    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, references, referenceValues, invalid, userId} = this.props;
        return (
            <div className="register login-signup-box">
                <h1 className="modal-title">Add Your References</h1>

                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="reference_name" component={renderField} validate={required}
                                   label="Name Of Reference"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="reference_designation" component={renderField}
                                   validate={required}
                                   label="Designation Of Reference"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="about_user" component={renderTextArea}
                                   validate={required}
                                   label="About Reference"/>
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
                                this.handleAddReference.bind(this, invalid, references, referenceValues, reset, userId)
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
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} type="button" onClick={this.handleOpenModal.bind(this)}>
                                Download Resume
                            </button>
                        </div>
                    </div>
                </form>
                {error && <div className={'Api-error'}>
                    <span>{error}</span>
                </div>
                }
                {
                    !!(references && references.length) &&
                    <div className={'Project-list'}>
                        <span className={'Project-heading'}>References:</span>
                        {
                            (references || []).map(reference => (
                                <button>{reference['reference_name']}</button>
                            ))
                        }
                    </div>
                }
                <ChoosePlanModal showModal={this.state.showModal} closeModal={this.handleCloseModal.bind(this)}/>
            </div>
        );
    }
}


export const ReferenceForm = reduxForm({
    form: 'referenceForm',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push({
            pathname: '/resume-builder/pricing'
        })
        window.location.reload()
    }
})(Reference);


const mapStateToProps = (state) => {
    return {
        referenceValues: state.form && state.form.referenceForm && state.form.referenceForm.values || {},
        references: state.userInfoReducer.references,
        userId: state.userInfoReducer.id,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userReference) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserReference({userReference, resolve, reject}))
        }),
        "addReference": (reference) => {
            return dispatch(actions.addReference(reference))
        }
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);

