import React, {Component} from 'react';
import './reference.scss'
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import {connect} from "react-redux";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";


class Reference extends Component {
    constructor(props) {
        super(props)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values);
    }

    componentDidMount() {
        this.props.fetchUserReference()
    }

    render() {
        const { handleSubmit,reference} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-references1"></i></span>
                    <h2>References</h2>
                    <span className="icon-edit icon-references__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <h3 className="add-section-heading">{reference.reference_name}</h3>
                                <div className="addon-buttons mr-10">
                                    <span className="icon-delete mr-15"></span>
                                    <span className="icon-ascend mr-5"></span>
                                    <span className="icon-descend"></span>
                                </div>
                            </div>
                            <div className="flex-container">
                                <fieldset className="error">
                                    <label>Reference name</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-refrences-gr"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="reference_name"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Designation</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-designation"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="reference_designation" 
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset>
                                    <label>Description</label>
                                    <Field component={renderTextArea} type={"textarea"} name="about_candidate"/>
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


export const ReferenceForm = reduxForm({
    form: 'reference',
    enableReinitialize: true
})(Reference);


const mapStateToProps = (state) => {
    return {
        initialValues: state.reference,
        reference: state.reference
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userReference) => {
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserReference({userReference, resolve, reject}));
            })
        },
        "fetchUserReference": () => {
            return dispatch(actions.fetchUserReference())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
