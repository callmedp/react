import React, {Component} from 'react';
import './award.scss'
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../store/award/actions";
import {connect} from "react-redux";
import {required} from "../../../../FormHandler/formValidations"
import {datepicker, renderField, renderTextArea} from "../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";


class Award extends Component {
    componentDidMount() {
        this.props.fetchUserAward()
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=course')
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, award, enableReinitialize} = this.props;
        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-awards1"></i></span>
                    <h2>Awards</h2>
                    <span className="icon-edit icon-awards__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <h3 className="add-section-heading">{award.title}</h3>
                                <div className="addon-buttons mr-10">
                                    <span className="icon-delete mr-15"></span>
                                    <span className="icon-ascend mr-5"></span>
                                    <span className="icon-descend"></span>
                                </div>
                            </div>
                            <div className="flex-container">
                                <fieldset className="error">
                                    <label>Title</label>
                                    <Field component={renderField} type={"text"} name="title"
                                        validate={required} className="input-control"/>
                                </fieldset>
                                <fieldset>
                                    <label>Date</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-date"></span>
                                        </div>
                                        <Field component={datepicker} type={"date"} className={'input-control'}
                                            validate={required} name="date"/>
                                    </div>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Summary</label>
                                    <Field component={renderTextArea} type={"text"} name="summary"
                                           className="input-control"/>
                                </fieldset>
                            </div>

                        </section>


                    </section>

                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
                        <button className="orange-button" type={'submit'}>Save & Continue</button>
                    </div>
                </form>

            </div>
        )
    }
}


export const AwardForm = reduxForm({
    form: 'award',
    enableReinitialize: true
})(Award);


const mapStateToProps = (state) => {
    return {
        initialValues: state.award,
        award: state.award
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userAward) => {
            const {date} = userAward;

            userAward = {
                ...userAward,
                ...{
                    date: date && moment(date).format('YYYY-MM-DD') || '',
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserAward({userAward, resolve, reject}));
            })
        },
        "fetchUserAward": () => {
            return dispatch(actions.fetchUserAward())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(AwardForm);
