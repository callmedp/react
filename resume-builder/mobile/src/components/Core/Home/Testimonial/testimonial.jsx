import React, {Component} from 'react';
import './testimonial.scss'

export default class Testimonial extends Component {
    constructor(props) {
        super(props)
    }


    render() {
        return (
            <section className="section grey-bg">
                    <div className="text-center">
                        <h2 className="section__head">Success stories</h2>
                        <p  className="section__subHead">What are our customers saying about our
                        <br/>resume builder</p>
                    </div>

                    <div className="success-stories mt-20">
                        <ul className="success-stories__items">
                            <li className="success-stories__item white-box pt-30 pb-30">
                                <div className="success-stories__infoWrap">
                                    <div className="success-stories__userInfo">
                                        <span className="success-stories__user">
                                            <img src="/media/static/react/assets/images/mobile/user-1.jpg" alt="" />
                                        </span>

                                        <div className="success-stories__nameInfo">
                                            <h3>Sumit Sharma</h3>
                                            <p>Project Manager, Sapient</p>
                                        </div>
                                    </div>

                                    <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</p>
                                </div>
                            </li>
                            
                            <li className="success-stories__item white-box pt-30 pb-30">
                                <div className="success-stories__infoWrap">
                                    <div className="success-stories__userInfo">
                                        <span className="success-stories__user">
                                            <img src="/media/static/react/assets/images/mobile/user-2.jpg" alt="" />
                                        </span>

                                        <div className="success-stories__nameInfo">
                                            <h3>Rakesh Kumar</h3>
                                            <p>Project Manager, Sapient</p>
                                        </div>
                                    </div>

                                    <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</p>
                                </div>
                            </li>
                            
                            <li className="success-stories__item white-box pt-30 pb-30">
                                <div className="success-stories__infoWrap">
                                    <div className="success-stories__userInfo">
                                        <span className="success-stories__user">
                                            <img src="/media/static/react/assets/images/mobile/user-3.jpg" alt="" />
                                        </span>

                                        <div className="success-stories__nameInfo">
                                            <h3>Vihaan Kumar</h3>
                                            <p>Project Manager, Sapient</p>
                                        </div>
                                    </div>

                                    <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</p>
                                </div>
                            </li>
                            
                            <li className="success-stories__item white-box pt-30 pb-30">
                                <div className="success-stories__infoWrap">
                                    <div className="success-stories__userInfo">
                                        <span className="success-stories__user">
                                            <img src="/media/static/react/assets/images/mobile/user-4.jpg" alt="" />
                                        </span>

                                        <div className="success-stories__nameInfo">
                                            <h3>Reyansh Kumar</h3>
                                            <p>Project Manager, Sapient</p>
                                        </div>
                                    </div>

                                    <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</p>
                                </div>
                            </li>
                            
                            <li className="success-stories__item white-box pt-30 pb-30">
                                <div className="success-stories__infoWrap">
                                    <div className="success-stories__userInfo">
                                        <span className="success-stories__user">
                                            <img src="/media/static/react/assets/images/mobile/user-5.jpg" alt="" />
                                        </span>

                                        <div className="success-stories__nameInfo">
                                            <h3>Muhammad Akmal</h3>
                                            <p>Project Manager, Sapient</p>
                                        </div>
                                    </div>

                                    <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </section>

        )
    }

}
