import React, {Component} from 'react';
import {datepicker, renderField, renderTextArea} from "../../../../../FormHandler/formFieldRenderer.jsx";
import {Field} from "redux-form";
export default class RenderAward extends Component {
    render(){
        const {fields, meta: {touched, error, submitFailed}} = this.props
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
                                        onBlur={() => {this.blurFunction.bind(this,error)}}   className="form__input" />
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
                {error && <li>{error}</li>}
            </div>
                
        )
    }
}