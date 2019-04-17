import React, {Component} from 'react';
import {Field, reduxForm} from "redux-form";
import * as actions from "../../.../../../../../../store/award/actions";
import {connect} from "react-redux";
import {required} from "../../../../../FormHandler/formValidations"
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";

class Award extends Component {

    constructor(props){
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        this.props.fetchUserAward()
    }

    async handleSubmit(values) {
        //console.log(this.props)
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=course')
    }

    render () {
        const {handleSubmit, award} = this.props;
        return (
            <div className="buildResume">
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Award</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline">+ Add new</button>
                    </div>
                    <form onSubmit={handleSubmit(this.handleSubmit)}>
                        <div className="subHeading pb-0">
                            <h2>{award.title}</h2>
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
                                <label className="form__label" for="title">Title</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--education-grey"></i>
                                    </span>
                                </div>
                                    <Field component={renderField} type={"text"} name="title"
                                         className="form__input" validate={required} aria-label="title" id="title"/>
                                </div>
                            </li>
                        
                            <li className="form__group">
                                <label className="form__label" for="date">Date</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={datepicker} type={"date"} className={'form__input'}
                                            validate={required} name="date" aria-label="date" id="date"/>
                                </div>
                            </li>

                            <li className="form__group">
                                <label className="form__label" for="summary">Summary</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                        <span className="input-group__text">
                                            <i className="sprite icon--date"></i>
                                        </span>
                                    </div>
                                    <Field component={renderTextArea} type={"textarea"} className={'form__input'}
                                        className="form__input" name="summary" aria-label="summary" id="summary"/>
                                </div>
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
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(AwardForm);