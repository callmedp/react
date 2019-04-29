import React, {Component} from 'react';
import './summary.scss'
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';

import {
    renderTextArea
} from "../../../../../FormHandler/formFieldRenderer.jsx";
import Loader from "../../../../../Loader/loader.jsx";


class Summary extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.editHeading = this.editHeading.bind(this);
        this.saveTitle = this.saveTitle.bind(this);
        this.state = {
            'isEditable': false
        }
    }

    componentDidMount() {
        this.props.fetchPersonalInfo()

    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=experience')
    }

    shouldComponentUpdate(nextProps, nextState, nextContext) {
        console.log('----update----', nextProps);
        return true;
    }

    editHeading() {
        this.setState({
            'isEditable': true
        })
        setTimeout(() => {
            this.refs.summary.focus();
        }, 0)


    }

    saveTitle(event) {
        event.stopPropagation()
        if (event.keyCode === 13) {
            this.setState({
                'isEditable': false
            })
        }
    }

    render() {
        const {personalInfo: {extra_info}, ui: {loader}, handleSubmit} = this.props;
        const {isEditable} = this.state;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-summary1"/></span>
                    <h2 ref={"summary"} onKeyUp={(event) => this.saveTitle(event)}
                        contenteditable={!!(isEditable) ? "true" : "false"}>Summary</h2>
                    <span onClick={this.editHeading}
                          className={!!(!isEditable) ? "icon-edit icon-edit__cursor" : ''}/>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="right-sidebar-scroll p3p">
                        <div className="summary-box">
                            <h3>Summary</h3>
                            <Field component={renderTextArea} type={"textarea"} name="extra_info"
                                   className="summary-box--summary-txt" rows="10" value={extra_info}/>
                        </div>
                    </section>

                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-20">Preview</button>
                        <button className="orange-button" type={'submit'}>Save & Continue</button>
                    </div>
                </form>
            </div>
        )
    }
}


export const SummaryForm = reduxForm({
    form: 'summary',
    enableReinitialize: true
})(Summary);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo,
        personalInfo: state.personalInfo,
        ui: state.ui
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
