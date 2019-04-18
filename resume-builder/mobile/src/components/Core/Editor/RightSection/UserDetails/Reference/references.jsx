import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import {connect} from "react-redux";
import {renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {required} from "../../../../../FormHandler/formValidations"
class References extends Component {
    constructor(props) {
        super(props)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteReference = this.deleteReference.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
    }

    async handleSubmit(values) {
        await this.props.bulkUpdateUserReference(values.list);
    }

    componentDidMount() {
        this.props.fetchUserReference()
    }

    handleAddition(fields, error) {
        
        fields.push({
            "candidate_id": '',
            "id": '',
            "reference_name": '',
            "reference_designation": '',
            "about_user": "",
            order: fields.length
        })
    }

    deleteReference(index, fields, event) {
        event.stopPropagation();
        const reference = fields.get(index);
        fields.remove(index);
        if (reference && reference.id) {
            this.props.removeReference(reference.id)
        }


    }

    changeOrderingUp(index,fields,event){
        event.stopPropagation();
        console.log("Clicked Up")
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index - 1)
        fields.insert(index - 1, prevItem)
        fields.swap(index, index - 1)
    }

    changeOrderingDown(index,fields,event){
        event.stopPropagation();
        console.log("Clicked Down")
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index+1)
        fields.insert(index + 1, nextItem)
        fields.swap(index, index + 1);
    }

    render () {
        const { handleSubmit,reference} = this.props;
        const renderReferences = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>References</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline"
                            onClick={this.handleAddition.bind(this, fields, error)}
                            type={'button'}>+ Add new</button>
                    </div>
                    {fields.map((member, index) => {
                        return (
                            <React.Fragment key={index}>
                                <div className="subHeading pb-0">
                                    <h2>{reference.reference_name}</h2>
                                    <ul className="subHeading__control">
                                        <li className="subHeading__delete">
                                            <span className="sprite icon--delete" role="button"
                                            onClick={(event) => this.deleteReference(index, fields, event)}></span>
                                        </li>
                                        {index == 0 ? '':
                                            <li className="subHeading__btn"
                                                onClick={(event) => this.changeOrderingUp(index, fields, event)}>
                                                <i className="sprite icon--upArrow"></i>
                                            </li>
                                        }
                                        {index == fields.length-1 ? '':
                                            <li className="subHeading__btn"
                                                onClick={(event) => this.changeOrderingDown(index, fields, event)}>
                                                <i className="sprite icon--downArrow"></i>
                                            </li>
                                        }
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
                                                name={`${member}.reference_name`}/>
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
                                            <Field component={renderField} validate={required} type={"text"} 
                                                name={`${member}.reference_designation`} className="form__input"/>
                                        </div>
                                    </li>

                                    <li className="form__group">
                                        <label className="form__label" htmlFor="about_candidate">Description</label>
                                        <Field component={renderTextArea} rows="3" type={"textarea"}
                                            className="form__input" name={`${member}.about_candidate`}/>
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
                    <FieldArray name={"list"} component={renderReferences}/>
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
        "removeReference": (referenceId) => {
            return dispatch(actions.deleteReference(referenceId))
        },

        "bulkUpdateUserReference": (listItems) => {
            listItems = (listItems || []).map(userReference => {
                if (!userReference['id']) delete userReference['id'];
                return userReference;
            })
            return dispatch(actions.bulkUpdateUserReference({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
