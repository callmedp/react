import React, {Component} from 'react';
import Header from '../../../Common/Header/header.jsx';
import './buy.scss';
import BuyModal from '../Buy/BuyModal.jsx';


export default class buy extends Component {

    render() {
        return(
            
            <div className="buy-container">
                <Header />
                <BuyModal 
                BuyOption={''}
                />
                <div className="pay-now">
                    <div className="pay-now__price">
                        <span className="fs-14 pay-now__price--pay">You pay</span>
                        <span className="fs-26 color-333 semi-bold">Rs. 999/-</span>
                    </div>

                    <button className="btn btn__round btn__primary fs-">Pay Now</button>
                </div>

                <div className="buy">
                    <div className="buy__wrap">
                        <div className="buy__item">
                            <div className="buy__item--left form__radio-group">
                                <input className="buy__item--input form__radio-input" type="radio" id="your-resume" name="custom-resume"></input>
                                <label  className="buy__item--label form__radio-label" for="your-resume">
                                    <span className="form__radio-button"></span>
                                    Buy your <br />customised resume
                                    <strong>Rs. 999/-</strong>
                                </label>
                            </div>
                            <div className="buy__item--right">
                                <span className="buy__item--image">
                                    <img src="/media/static/react/assets/images/mobile/resume4.png" alt="Resume"/>
                                </span>
                                <a href="#" className="fs-12 mt-5">Edit</a>
                            </div>
                        </div>
                        
                        
                        <div className="buy__item buy__recommended">
                            <div className="buy__recommended--tag">Recommended</div>
                            <div className="buy__item--left form__radio-group">
                                <input className="buy__item--input form__radio-input" type="radio" id="all-resumes" name="custom-resume"></input>
                                <label  className="buy__item--label form__radio-label" for="all-resumes">
                                    <span className="form__radio-button"></span>
                                    Buy all 6 customised resumes
                                    <div className="buy__item--price">
                                        <span className="fs-22 color-333 semi-bold">Rs. 1249/-</span>
                                        <span className="fs-14 line-through">Rs. 3499</span>
                                        <span className="fs-14 bold">63% off</span>
                                    </div>
                                </label>
                            </div>
                            <div className="buy__item--right">
                                <div className="buy__item--right__sliderWrap mt-20">
                                    <div className="buy__item--right__sliderWrap__controls">
                                        <span className="buy__item--right__sliderWrap__controls--next">
                                            <i className="sprite icon--control"></i>
                                        </span>
                                        <span className="buy__item--right__sliderWrap__controls--prev hide">
                                            <i className="sprite icon--control"></i>
                                        </span>
                                    </div>
                                    <ul className="buy__recommended__items">
                                        <li className="buy__recommended__item" onClick={this.openModal}>
                                            <span className="buy__recommended__image">
                                                <span className="sprite icon--zoom"></span>
                                                <img src="/media/static/react/assets/images/mobile/resume-1.png" alt="Custom resume" />
                                            </span>
                                        </li>
                                        
                                        <li className="buy__recommended__item">
                                            <span className="buy__recommended__image">
                                                <span className="sprite icon--zoom"></span>
                                                <img src="/media/static/react/assets/images/mobile/resume-2.png" alt="Custom resume" />
                                            </span>
                                        </li>
                                       
                                        <li className="buy__recommended__item">
                                            <span className="buy__recommended__image">
                                                <span className="sprite icon--zoom"></span>
                                                <img src="/media/static/react/assets/images/mobile/resume-2.png" alt="Custom resume" />
                                            </span>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                

                
            </div>

        )
    }
}