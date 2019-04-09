import React, {Component} from 'react';
import './language.scss'
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../../store/language/actions";
import {connect} from "react-redux";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";


class Language extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
    }


    componentDidMount() {
        this.props.fetchUserLanguage();
    }


    async handleSubmit(values) {
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=award')
    }


    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize, language} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-languages1"></i></span>
                    <h2>Languages</h2>
                    <span className="icon-edit icon-language__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <h3 className="add-section-heading">{language.name}</h3>
                                <div className="addon-buttons mr-10">
                                    <span className="icon-delete mr-15"></span>
                                    <span className="icon-ascend mr-5"></span>
                                    <span className="icon-descend"></span>
                                </div>
                            </div>
                            <div className="flex-container">
                                <fieldset className="width-half">
                                    <label>Language name</label>
                                    <Field component={renderField} type={"text"} name="name"/>
                                </fieldset>

                                <fieldset className="width-half">
                                    <label>Language rating (out of 10)</label>
				        			<Field name="proficiency"
                                           component={renderSelect}
                                           isMulti={false}
                                           options={[
                                               {value: 1, label: '1'},
                                               {value: 2, label: '2'},
                                               {value: 3, label: '3'},
                                               {value: 4, label: '4'},
                                               {value: 5, label: '5'},
                                               {value: 6, label: '6'},
                                               {value: 7, label: '7'},
                                               {value: 8, label: '8'},
                                               {value: 9, label: '9'},
                                               {value: 10, label: '10'}
                                           ]}/>
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


export const LanguageForm = reduxForm({
    form: 'Language',
    enableReinitialize: true
})(Language);


const mapStateToProps = (state) => {
    return {
        initialValues: state.language,
        language: state.language
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userLanguage) => {
            const {proficiency} = userLanguage;
            userLanguage = {
                ...userLanguage,
                ...{
                    proficiency: proficiency && proficiency.value || 5
                }
            }
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserLanguage({userLanguage, resolve, reject}));
            })
        },
        "fetchUserLanguage": () => {
            return dispatch(actions.fetchUserLanguage())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
