import React, {Component} from 'react';
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import {connect} from "react-redux";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {required} from "../../../../../FormHandler/formValidations"
export default class references extends Component {
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

    render () {
        const { handleSubmit,reference} = this.props;
        return (
            <div className="buildResume">
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>References</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline">+ Add new</button>
                    </div>
                    <form onSubmit={handleSubmit(this.handleSubmit)}>
                        <div className="subHeading pb-0">
                            <h2>{reference.reference_name}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className="sprite icon--delete" role="button"></span>
                                </li>
                                <li className="subHeading__btn">
                                    <i className="sprite icon--upArrow"></i>
                                </li>
                                <li className="subHeading__btn">
                                    <i className="sprite icon--downArrow"></i>
                                </li>
                            </ul>
                        </div>

                        <ul className="form pb-0">
                            <li className="form__group">
                                <label className="form__label" for="reference_name">Reference name</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--project-gray"></i>
                                    </span>
                                    </div>
                                    <Field component={renderField} validate={required} type={"text"} 
                                        name="reference_name" aria-label="reference_name" id="actireference_namevity"/>
                                </div>
                            </li>
                            
                            <li className="form__group">
                                <label className="form__label" for="activity">Reference company name</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--company"></i>
                                    </span>
                                    </div>
                                    <input type="text" name="activity" className="form__input" placeholder="" aria-label="activity" id="activity" />
                                </div>
                            </li>
                            
                            <li className="form__group">
                                <label className="form__label" for="designation">Designation</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--designation"></i>
                                    </span>
                                    </div>
                                    <input type="text" name="designation" className="form__input" placeholder="IT Project Manager" aria-label="designation" id="designation" />
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" for="description">Description</label>
                                <textarea rows="3" cols="30" name="description" className="form__input" aria-label="description" id="description" ></textarea>
                            </li>
                            
                        </ul>

                        <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline">Preview</button>
                                <button className="btn btn__round btn__primary">Save &amp; Continue</button>
                            </div>
                        </li>
                    </ul>
                    </form>
                </div>
            </div>
        )
    }
}