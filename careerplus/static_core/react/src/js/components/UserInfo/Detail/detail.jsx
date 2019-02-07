import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import * as actions from '../../../store/userInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, datePicker, renderSelect, renderTextArea} from '../../../fieldLevelValidationForm';

export class Detail extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting} = this.props;
        return (
            <div className={'Authentication-page'}>
                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="date" name="date_of_birth" component={renderField} validate={required}
                                   label="Date Of Birth:"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="location" component={renderField} validate={required}
                                   label="Location :"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field
                                name="gender"
                                component={renderSelect}
                                validate={required}
                                label="Gender:"
                            >
                                <option></option>
                                <option name="Male" value="M">Male</option>
                                <option name="Female" value="F">Female</option>
                                <option name="Other" value="O">Other</option>

                            </Field>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field
                                name="extra_info"
                                component={renderTextArea}
                                type="text"
                                label="Extra Information:"
                            />
                        </div>
                    </div>
                    <div className={'Button-group'}>
                        <div className={'Button-parent'}>
                            <button className={'Submit-button'} onClick={() => {
                                this.props.history.goBack()
                            }}>
                                Back
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
            </div>
        );
    }
}


export const DetailForm = reduxForm({
    form: 'user_info',
    onSubmitSuccess: (result, dispatch, props) => {
        props.history.push('about')
    }
})(Detail);


const mapStateToProps = (state) => {
    return {}
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userDetails) => new Promise((resolve, reject) => {
            dispatch(actions.updateUserDetails({userDetails, resolve, reject}))
        })
    }

};

export default connect(mapStateToProps, mapDispatchToProps)(DetailForm);

