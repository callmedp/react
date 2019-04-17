import React, {Component} from 'react';
import './language.scss'
import {Field, reduxForm, FieldArray, arrayPush} from "redux-form";
import * as actions from "../../../../../../store/language/actions";
import {connect} from "react-redux";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {required} from "../../../../../FormHandler/formValidations"

class Language extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteLanguage = this.deleteLanguage.bind(this);
    }

    componentDidMount() {
        this.props.fetchUserLanguage();
    }


    async handleSubmit(values) {
        await this.props.bulkUpdateUserLanguage(values.list);
        this.props.history.push('/resume-builder/edit/?type=award')
    }

    handleAddition(fields, error) {

        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": {
                value: 5, 'label': '5'
            },
            order: fields.length
        })
    }

    deleteLanguage(index, fields, event) {
        event.stopPropagation();
        const language = fields.get(index);
        fields.remove(index);
        if (language && language.id) {
            this.props.removeLanguage(language.id)
        }
    }


    render() {
        const {handleSubmit, language} = this.props;
        const renderMembers = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                
                <div className="buildResume__wrap pb-0">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Language</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline"
                        onClick={this.handleAddition.bind(this, fields, error)}
                        type={'button'} >+ Add new</button>
                    </div>
                    {fields.map((member, index) => {
                        return (
                            <React.Fragment>
                                <div className="subHeading pb-0">
                                    <h2>{language.name}</h2>
                                    <ul className="subHeading__control">
                                        <li className="subHeading__delete">
                                            <span className="sprite icon--delete" 
                                             onClick={(event) => this.deleteLanguage(index, fields, event)}
                                             role="button"></span>
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
                                        <label className="form__label" htmlFor="name">Language name</label>
                                        <Field component={renderField} type={"text"} 
                                        name={`${member}.name`} className="form__input"/>
                                    </li>
                                    
                                    <li className="form__group">
                                        <label className="form__label" htmlFor="proficiency">Skill rating (out of 10)</label>
                                        <Field name={`${member}.proficiency`}
                                                    component={renderSelect}
                                                    className="form__select"
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
                                                    ]}
                                                   />
                                    </li>
                                </ul>

                            </React.Fragment>
                    )})}
                </div>
            
            )
        }
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" component={renderMembers}/>
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
        "removeLanguage": (languageId) => {
            return dispatch(actions.deleteLanguage(languageId))
        },

        "bulkUpdateUserLanguage": (listItems) => {
            listItems = (listItems || []).map(item => {
                const {proficiency} = item;
                if (!item['id']) delete item['id'];
                item = {
                    ...item,
                    ...{
                        proficiency: (proficiency && proficiency.value) || 5

                    }
                }
                return item;
            })
            return dispatch(actions.bulkUpdateUserLanguage({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
