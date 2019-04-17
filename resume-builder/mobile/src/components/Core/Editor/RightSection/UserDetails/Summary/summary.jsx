import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';

import {
    renderTextArea
} from "../../../../../FormHandler/formFieldRenderer.jsx";


class Summary extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        this.props.fetchPersonalInfo()

    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=experience')
    }

    render() {
        const {personalInfo: {extra_info}, handleSubmit} = this.props;
        return (
        <div className="buildResume">
            <div className="buildResume__wrap pb-0">
                <div className="buildResume__heading">
                    <h2>Summary</h2>
                    <i className="sprite icon--edit"></i>
                </div>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <ul className="form">
                    
                        <li className="form__group">
                            <label className="form__label" for="extra_info">Summary</label>
                            <Field component={renderTextArea} type={"textarea"} name="extra_info"
                                className="form__input h-300" value={extra_info}
                                aria-label="extra_info" id="extra_info"/>
                        </li>
                        

                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline">Preview</button>
                                <button className="btn btn__round btn__primary" type={'submit'}>Save &amp; Continue</button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
        </div>
        )
    }
}

export const SummaryForm = reduxForm({
    form: 'personalInfo',
    enableReinitialize: true
})(Summary);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo,
        personalInfo: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "onSubmit": (personalDetails) => {
            const {gender, date_of_birth, extracurricular} = personalDetails
            personalDetails = {
                ...personalDetails,
                ...{
                    'gender': gender && gender['value'] || '',
                    'extracurricular': (extracurricular || []).map(el => el.value).join(',')
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(actions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SummaryForm);
