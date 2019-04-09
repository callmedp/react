import React, {Component} from 'react';
import './language.scss'


export default class Language extends Component {
    render() {
        return (
            <div className="buildResume">
                <div className="buildResume__wrap pb-0">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Language</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline">+ Add new</button>
                    </div>

                    <div className="subHeading pb-0">
                        <h2>Language 1</h2>
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
                            <label className="form__label" for="language">Language name</label>
                            <select class="form__select" id="language">
                                <option>English</option>
                                <option>Hindi</option>
                                <option>English</option>
                                <option>Hindi</option>
                                <option>English</option>
                                <option>Hindi</option>
                            </select>
                        </li>
                        
                        <li className="form__group">
                            <label className="form__label" for="skillRating">Skill rating (out of 10)</label>
                            <select class="form__select" id="skillRating">
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                                <option>4</option>
                                <option>5</option>
                            </select>
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