import React, {Component} from 'react';
import './reference.scss'
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../store/reference/actions";
import {connect} from "react-redux";
import {renderField, renderTextArea} from "../../../../FormHandler/formFieldRenderer";


class Reference extends Component {


    componentDidMount() {
        this.props.fetchUserReference()
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-references1"></i></span>
                    <h2>References</h2>
                    <span className="icon-edit icon-references__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>

                <section className="right-sidebar-scroll">
                    <section className="info-section">
                        <div className="flex-container">
                            <h3 className="add-section-heading">Reference 1</h3>
                            <div className="addon-buttons mr-10">
                                <span className="icon-delete mr-15"></span>
                                <span className="icon-ascend mr-5"></span>
                                <span className="icon-descend"></span>
                            </div>
                        </div>
                        <div className="flex-container">
                            <fieldset className="error">
                                <label>Reference name</label>
                                <Field component={renderField} type={"text"} name="reference_name"/>
                            </fieldset>
                            <fieldset>
                                <label>Reference company name</label>
                                <input type="text" name="" placeholder=""/>
                            </fieldset>
                            <fieldset>
                                <label>Designation</label>
                                <Field component={renderField} type={"text"} name="reference_designation"/>
                            </fieldset>
                        </div>

                        <div className="flex-container">
                            <fieldset>
                                <label>Description</label>
                                <Field component={renderTextArea} type={"textarea"} name="about_user"/>
                            </fieldset>
                        </div>

                    </section>


                </section>

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10">Preview</button>
                    <button className="orange-button">Save & Continue</button>
                </div>

            </div>
        )
    }
}


export const ReferenceForm = reduxForm({
    form: 'reference',
    enableReinitialize: true
})(Reference);


const mapStateToProps = (state) => {
    return {
        initialValues: state.reference
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserReference": () => {
            return dispatch(actions.fetchUserReference())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
