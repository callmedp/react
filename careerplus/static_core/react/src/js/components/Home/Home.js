import React from 'react';
import PropTypes from 'prop-types';
import {Field, reduxForm} from 'redux-form';
import {renderField, required, phoneNumber} from '../../fieldLevelValidationForm';

class Home extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {handleSubmit, pristine, reset, submitting} = this.props;
        return (
            <div className={'Authentication-page'}>
                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="firstName" component={renderField} validate={required}
                                   label="First Name:"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field type="text" name="lastName" component={renderField} validate={required}
                                   label="Last Name:"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field
                                name="email"
                                component={renderField}
                                validate={required}
                                type="email"
                                label="Email:"
                            />
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <div>
                            <Field
                                name="number"
                                component={renderField}
                                validate={[required, phoneNumber]}
                                type="text"
                                label="Contact Number:"
                            />
                        </div>
                    </div>
                    <div className={'Button-parent'}>
                        <button className={'Submit-button'} type="submit" disabled={pristine || submitting}>
                            Submit
                        </button>
                    </div>
                </form>
            </div>
        );
    }
}

Home.propTypes = {};

export default reduxForm({
    form: 'user_info'
})(Home);