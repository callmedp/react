import React, {Component} from 'react';

export default class course extends Component {
    render () {
        return (
            <div className="buildResume">
                <div className="buildResume__wrap">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Courses</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline">+ Add new</button>
                    </div>

                    <div className="subHeading pb-0">
                        <h2>Courses 1</h2>
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
                            <label className="form__label" for="course">Course name</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                <span className="input-group__text">
                                    <i className="sprite icon--course-grey"></i>
                                </span>
                                </div>
                                <input type="text" name="course" className="form__input" placeholder="" aria-label="course" id="course" />
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