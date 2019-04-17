import React ,{Component} from 'react';
import Header from '../../../Common/Header/header.jsx';
import './preview.scss';

export default class Preview extends Component {
    render(){
        return(
            <div className="preview">
               <Header />

               <div className="preview__resume">
                    <img src="/media/static/react/assets/images/mobile/resume.jpg" alt="Resume"/>
               </div>

               <div className="preview__bottom-btns">
                    <span className="btn btn__round btn--outline">Customize template</span>
                    <span className="btn btn__round btn__primary">Get your resume</span>
               </div>

               <div className="filter">
                    <div className="filter__overlay"></div>
                    <div className="filter__wrap">
                        
                        <div className="filter__accordion">
                            <h2 className="filter__wrap--heading">Customize template</h2>

                            <div className="filter__accordion__card filter__accordion--active">
                                <div className="filter__accordion__card__heading">
                                    <div className="filter__accordion__card__heading--left">
                                        <i className="sprite icon--theme mr-10"></i>
                                        <span>Change theme</span>
                                    </div>

                                    <div className="filter__accordion__card__heading--right">
                                        <i className="sprite icon--plus icon--minus"></i>
                                    </div>
                                </div>

                                <div className="filter__accordion__card--content">  
                                    <ul className="resume-color-theme">
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="green" value="green" />
                                            <label htmlFor="green" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--green"></span>
                                            </label>
                                        </li>

                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="blue" value="blue" />
                                            <label htmlFor="blue" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--blue"></span>
                                            </label>
                                        </li>
                                        
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="red" value="red"/>
                                            <label htmlFor="red" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--red"></span>
                                            </label>
                                        </li>
                                        
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="black" value="black" />
                                            <label htmlFor="black" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--black"></span>
                                            </label>
                                        </li>
                                        
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="brown" value="brown"/>
                                            <label htmlFor="brown" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--brown"></span>
                                            </label>
                                        </li>
                                        
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="violet" value="violet" />
                                            <label htmlFor="violet" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--violet"></span>
                                            </label>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div className="filter__accordion__card">
                                <div className="filter__accordion__card__heading">
                                    <div className="filter__accordion__card__heading--left">
                                        <i className="sprite icon--font mr-10"></i>
                                        <span>Font size</span>
                                    </div>

                                    <div className="filter__accordion__card__heading--right">
                                        <i className="sprite icon--plus"></i>
                                    </div>
                                </div>

                                <div className="filter__accordion__card--content">
                                    <div className="font-filter">
                                        <h3>Section Heading</h3>
                                        <div className="font-filter__slide-bar">
                                            <span className="font-filter__dot"></span>
                                            <span className="font-filter--small mt-10 fs-12">S</span>
                                            <span className="font-filter--medium mt-10 fs-12">M</span>
                                            <span className="font-filter--large mt-10 fs-12">L</span>
                                        </div>

                                    </div>
                                </div>
                            </div>

                            <div className="filter__accordion__card mt-20">
                                <div className="filter__accordion__card__heading">
                                    <div className="filter__accordion__card__heading--left">
                                        <i className="sprite icon--reorder mr-10"></i>
                                        <span>Reorder section</span>
                                    </div>

                                    <div className="filter__accordion__card__heading--right">
                                        <i className="sprite icon--plus"></i>
                                    </div>
                                </div>

                                <div className="filter__accordion__card--content">
                                    <div className="reorder">
                                        <ul className="reorder__items">
                                            <li className="reorder__item reorder--select">
                                                <span className="reorder__title">Personal Info</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">Summary</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">Experience</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">Education</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">Skills</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">Language</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">Awards</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">Courses</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">Projects</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                            
                                            <li className="reorder__item">
                                                <span className="reorder__title">References</span>
                                                <div className="reorder__nav">
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--upArrow"></i>
                                                    </span>
                                                    <span className="reorder__nav--item">
                                                        <i className="sprite icon--downArrow"></i>
                                                    </span>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="filter__apply-btn">
                            <span className="btn">Cancel</span>
                            <span className="btn btn__round btn--outline">Apply</span>
                        </div>
                    </div>
                </div>
            </div>

            
        )
    }

}