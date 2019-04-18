import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../.../../../../../../store/award/actions";
import {connect} from "react-redux";
import {required} from "../../../../../FormHandler/formValidations"
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";

class Award extends Component {

    constructor(props){
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteAward = this.deleteAward.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
    }

    componentDidMount() {
        this.props.fetchUserAward()
    }

    async handleSubmit(values) {
        //console.log(this.props)
        await this.props.bulkUpdateUserAward(values.list);
        this.props.history.push('/resume-builder/edit/?type=course')
    }

    handleAddition(fields, error) {
        
        fields.push({
            "candidate_id": '',
            "id": '',
            "title": '',
            "date": '',
            "summary": '',
            order: fields.length
        })
    }

    deleteAward(index, fields, event) {
        event.stopPropagation();
        const award = fields.get(index);
        console.log(award)
        fields.remove(index);
        if (award && award.id) {
            this.props.removeAward(award.id)
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
        const {handleSubmit, award} = this.props;
        const renderAwards = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Award</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" onClick={this.handleAddition.bind(this, fields, error)}
                            type={'button'} className="btn btn__round btn--outline">+ Add new</button>
                    </div>

                    {fields.map((member, index) => {
                    return(
                        <React.Fragment key={index}>
                            <div className="subHeading pb-0">
                                <h2>{fields.get(index).title || 'Award'}</h2>
                                <ul className="subHeading__control">
                                    <li className="subHeading__delete">
                                        <span className="sprite icon--delete" role="button"
                                            onClick={(event) => this.deleteAward(index, fields, event)}></span>
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
                                    <label className="form__label" htmlFor="title">Title</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--education-grey"></i>
                                        </span>
                                    </div>
                                        <Field component={renderField} type={"text"} name={`${member}.title`}
                                            className="form__input" />
                                    </div>
                                </li>
                            
                                <li className="form__group">
                                    <label className="form__label" htmlFor="date">Date</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--date"></i>
                                            </span>
                                        </div>
                                        <Field component={datepicker} type={"date"} className={'form__input'}
                                            name={`${member}.date`}/>
                                    </div>
                                </li>
        
                                <li className="form__group">
                                    <label className="form__label" htmlFor="summary">Summary</label>
                                    <div className="input-group">
                                        <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--date"></i>
                                            </span>
                                        </div>
                                        <Field component={renderTextArea} type={"textarea"} className={'form__input'}
                                            className="form__input" name={`${member}.summary`}/>
                                    </div>
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
                    <FieldArray name="list" component={renderAwards}/>
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
                    date: (date && moment(date).format('YYYY-MM-DD')) || '',
                }
            };
            console.log(userAward)
            //return "yes"
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserAward({userAward, resolve, reject}));
            })
        },
        "fetchUserAward": () => {
            return dispatch(actions.fetchUserAward())
        },
        "removeAward": (awardId) => {
            console.log("Award iD   "+awardId)
            return dispatch(actions.deleteAward(awardId))
        },
        "bulkUpdateUserAward": (listItems) => {
            listItems = (listItems || []).map(userAward => {
                const {date} = userAward;
                if (!userAward['id']) delete userAward['id'];
                userAward = {
                    ...userAward,
                    ...{
                        date: (date && moment(date).format('YYYY-MM-DD')) || '',
                    }
                };
                return userAward;
            })
            console.log(listItems)
            return dispatch(actions.bulkUpdateUserAward({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(AwardForm);