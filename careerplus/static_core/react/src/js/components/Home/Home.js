import React from 'react';
import PropTypes from 'prop-types';
import {Field, reduxForm} from 'redux-form';

class Home extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {handleSubmit, pristine, reset, submitting} = this.props;
        return (
            <div className={'App-header'}>
                <form onSubmit={handleSubmit}>
                    <div className={'Text-spacing'}>
                        <label>
                            First Name:
                        </label>
                        <div>
                            <Field type="text" name="firstName" component="input" placeholder="First Name"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <label>
                            Last Name:
                        </label>
                        <div>
                            <Field type="text" name="lastName" component="input" placeholder="Lasst Name"/>
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <label>
                            Email:
                        </label>
                        <div>
                            <Field
                                name="email"
                                component="input"
                                type="email"
                                placeholder="Email"
                            />
                        </div>
                    </div>
                    <div className={'Text-spacing'}>
                        <label>
                            Number:
                        </label>
                        <div>
                            <Field
                                name="number"
                                component="input"
                                type="text"
                                placeholder="Contact Number"
                            />
                        </div>
                    </div>

                    <button type="submit" disabled={pristine || submitting}>
                        Submit
                    </button>
                </form>
            </div>
        );
    }
}

Home.propTypes = {
    pinCode: PropTypes.number
}

export default reduxForm({
    form: 'user_info'
})(Home);