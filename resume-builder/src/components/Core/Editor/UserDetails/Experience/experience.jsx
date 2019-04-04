import React, {Component} from 'react';
import './experience.scss'


export default class Experience extends Component {
    render() {
        return (
            <div className="buildResume">
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Experience</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline">+ Add new</button>
                    </div>

                    <div className="subHeading pb-0">
                        <h2>Experience 1</h2>
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
                            <label className="form__label" for="designation">Designation</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                <span className="input-group__text">
                                    <i className="sprite icon--designation"></i>
                                </span>
                                </div>
                                <input type="text" name="designation" className="form__input" placeholder="Visual Designer" aria-label="designation" id="school" />
                            </div>
                        </li>
                        
                        <li className="form__group">
                            <label className="form__label" for="company">Company name</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                <span className="input-group__text">
                                    <i className="sprite icon--company"></i>
                                </span>
                                </div>
                                <input type="text" name="company" className="form__input" placeholder="Sapient" aria-label="company" id="school" />
                            </div>
                        </li>
                        
                        <li className="form__group">
                            <label className="form__label" for="dateFrom">Date from</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                <span className="input-group__text">
                                    <i className="sprite icon--date"></i>
                                </span>
                                </div>
                                <input type="text" name="dateFrom" className="form__input" placeholder="" aria-label="dateFrom" id="dateFrom" />
                            </div>
                        </li>
                        
                        <li className="form__group">
                            <label className="form__label" for="dateTo">Date to</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                <span className="input-group__text">
                                    <i className="sprite icon--date"></i>
                                </span>
                                </div>
                                <input type="text" name="dateTo" className="form__input" placeholder="" aria-label="dateTo" id="dateTo" />
                            </div>
                        </li>
                        
                        
                        <li className="form__group">
                            <label className="form__label" for="description">Description</label>
                            <textarea rows="3" cols="30" name="description" className="form__input" aria-label="description" id="description" ></textarea>
                        </li>

                        <li className="form__radio-group d-flex justify-content-end fs-14">
                            <input class="form__radio-input" type="radio" name="tillToday" id="tillToday" value="option2" />
                            <label class="form__radio-label" for="tillToday">
                                <span className="form__radio-button"></span>
                                Till today
                            </label>
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
                </div>
            </div>
        )
    }
}