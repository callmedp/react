import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/language/actions";
import {connect} from "react-redux";
import {LanguageRenderer} from "./languageRenderer";
import validate from '../../../../../FormHandler/validations/language/validate'
/*
styles
* */
import 'react-accessible-accordion/dist/fancy-example.css';

class Language extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteLanguage = this.deleteLanguage.bind(this);

        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false

        };
        this.props.currentForm('language');

    }


    componentWillUnmount() {
        let {formData: {Language: {values, syncErrors}}} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit) this.props.bulkUpdateOrCreate(values && values['list']);
    }

    componentDidMount() {
        this.props.fetchUserLanguage();
    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            this.setState({
                submit: true
            })
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }
    }

    async handleAddition(fields) {
        const listLength = fields.length;
        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": {
                value: 5, 'label': '5'
            },
            order: listLength
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

    handleAccordionClick(value) {
        this.setState({active: value})
    }


    render() {
        const {
            handleSubmit, ui: {loader}, isEditable,
            editHeading, saveTitle, entityName, nextEntity,
            handlePreview, changeOrderingUp, changeOrderingDown
        } = this.props;
        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray
                    name="list"
                    loader={loader}
                    handleSubmit={handleSubmit}
                    handleAccordionClick={this.handleAccordionClick}
                    handleAddition={this.handleAddition}
                    deleteLanguage={this.deleteLanguage}
                    changeOrderingUp={changeOrderingUp}
                    changeOrderingDown={changeOrderingDown}
                    component={LanguageRenderer}
                    saveTitle={(event) => saveTitle(event, 8)}
                    editHeading={(value) => editHeading(value)}
                    isEditable={isEditable}
                    entityName={entityName}
                    expanded={this.state.active}

                />

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10" type={'button'} onClick={handlePreview}>Preview</button>
                    <button className="orange-button"
                            type={'submit'}>{!nextEntity ? "Download" : 'Save and Continue'}</button>
                </div>
            </form>
        )
    }
}


export const LanguageForm = reduxForm({
    form: 'Language',
    enableReinitialize: true,
    validate,


})(Language);


const mapStateToProps = (state) => {
    return {
        initialValues: state.language,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userLanguage) => {
            const {proficiency} = userLanguage;
            userLanguage = {
                ...userLanguage,
                ...{
                    proficiency: (proficiency && proficiency.value) || 5
                }
            };
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

        "bulkUpdateOrCreate": (listItems) => {
            listItems = (listItems || []).map((item, index) => {
                const {proficiency} = item;
                if (!item['id']) delete item['id'];
                item = {
                    ...item,
                    ...{
                        proficiency: (proficiency && proficiency.value) || 5,
                        order: index

                    }
                };
                return item;
            })
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserLanguage({list: listItems, resolve, reject}))
            })

        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LanguageForm);
