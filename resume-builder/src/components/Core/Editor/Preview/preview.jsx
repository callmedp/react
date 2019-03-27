import React ,{Component} from 'react';
import Header from '../../../Common/Header/header';
import './preview.scss';

export default class Preview extends Component {
    render(){
        return(
            <div className="preview">
               <Header />

               <div className="preview__resume">
                    <img src="/images/resume.jpg" alt="Resume"/>
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

                            <div className="filter__accordion__card">
                                <div className="filter__accordion__card__heading">
                                    <div className="filter__accordion__card__heading--left">
                                        <i className="sprite icon--theme mr-10"></i>
                                        <span>Change theme</span>
                                    </div>

                                    <div className="filter__accordion__card__heading--right">
                                        <i className="sprite icon--plus"></i>
                                    </div>
                                </div>

                                <div className="filter__accordion__card--content">
                                    
                                    <ul className="resume-color-theme">
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="green" value="green" />
                                            <label for="green" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--green"></span>
                                            </label>
                                        </li>

                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="blue" value="blue" />
                                            <label for="blue" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--blue"></span>
                                            </label>
                                        </li>
                                        
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="red" value="red"/>
                                            <label for="red" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--red"></span>
                                            </label>
                                        </li>
                                        
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="black" value="black" />
                                            <label for="black" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--black"></span>
                                            </label>
                                        </li>
                                        
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="brown" value="brown"/>
                                            <label for="brown" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--brown"></span>
                                            </label>
                                        </li>
                                        
                                        <li className="resume-color-theme__item">
                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="violet" value="violet" />
                                            <label for="violet" className="resume-color-theme__item__label">
                                                <span className="resume-color-theme__item__theme resume-color-theme__item--violet"></span>
                                            </label>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div className="filter__accordion__card filter__accordion--active">
                                <div className="filter__accordion__card__heading">
                                    <div className="filter__accordion__card__heading--left">
                                        <i className="sprite icon--font mr-10"></i>
                                        <span>Font size</span>
                                    </div>

                                    <div className="filter__accordion__card__heading--right">
                                        <i className="sprite icon--plus icon--minus"></i>
                                    </div>
                                </div>

                                <div className="filter__accordion__card--content">
                                    <div className="font-filter">

                                    </div>
                                </div>
                            </div>


                            
                            <div className="filter__accordion__card">
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
                                    Reorder section
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