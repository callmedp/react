import React, {Component} from 'react';
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import {connect} from "react-redux";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {required} from "../../../../../FormHandler/formValidations"
class References extends Component {
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
                                <label className="form__label" htmlFor="reference_name">Reference name</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--project-gray"></i>
                                    </span>
                                    </div>
                                    <Field component={renderField} validate={required} type={"text"} className="form__input"
                                        name="reference_name" aria-label="reference_name" id="actireference_namevity"/>
                                </div>
                            </li>
                            
                            <li className="form__group">
                                <label className="form__label" htmlFor="reference_designation">Designation</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--designation"></i>
                                    </span>
                                    </div>
                                    <Field component={renderField} validate={required} type={"text"} name="reference_designation"
                                        className="form__input" aria-label="reference_designation" id="reference_designation"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" htmlFor="about_candidate">Description</label>
                                <Field component={renderTextArea} rows="3" type={"textarea"} name="about_candidate"
                                    className="form__input" aria-label="about_candidate" id="about_candidate"/>
                            </li>
                            
                        </ul>

                        <ul className="form">
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


export const ReferenceForm = reduxForm({
    form: 'reference',
    enableReinitialize: true
})(References);


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
