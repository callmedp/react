import React, {Component} from 'react';
import Header from '../../Common/Header/header.jsx';
import Footer from '../../Common/Footer/footer.jsx';
import {connect} from "react-redux";
import './home.scss'
import * as actions from "../../../store/landingPage/actions";
import Banner from './Banner/banner.jsx';
import ResumeSlider from './ResumeSlider/resumeSlider.jsx';
import Testimonial from './Testimonial/testimonial.jsx';

class Home extends Component {
    
    constructor(props) {
        super(props);
    }
    
    render() {
        return (
            <div className="home">
                <Header />
                <Banner/>

                <section className="info">
                    <ul className="info__items">
                        <li className="icon--expertise"><strong>10 years</strong> of expertise in resume building</li>
                        <li className="icon--build">Build your resume in a minute by importing your <strong>Shine profile</strong></li>
                        <li className="icon--download"><strong>Download</strong> your customised resume anytime</li>
                        <li className="icon--custom"><strong>Highly customizable</strong> resume  </li>
                        <li className="icon--power">Power to get you <strong>hired 33% faster</strong></li>
                    </ul>
                </section>

                <section className="section professional">
                    <div className="text-center">
                        <h2 className="section__head">Professional advantage</h2>
                        <p  className="section__subHead">Resume builder advantages which will make your career brighter</p>
                    </div>

                    <ul className="professional__items">
                        <li className="professional__item">
                            <span>
                                <i className="sprite icon--resume"></i>
                            </span>
                            A resume layout that stands out 
                        </li>
                        
                        <li className="professional__item">
                            <span>
                                <i className="sprite icon--create"></i>
                            </span>
                            Create a great first impression to recruiters  
                        </li>
                        
                        <li className="professional__item">
                            <span>
                                <i className="sprite icon--increase"></i>
                            </span>
                            Increased recruiter views on your profile 
                        </li>
                        
                        <li className="professional__item">
                            <span>
                                <i className="sprite icon--application"></i>
                            </span>
                            Application Tracking Software (ATS) Friendly 
                        </li>
                    </ul>
                </section>

                <section className="section how-works grey-bg">
                    <div className="text-center">
                        <h2 className="section__head">How it works</h2>
                        <p  className="section__subHead">Just 3 steps to create your perfect resume</p>
                    </div>

                    <div className="white-box mt-30">
                        <ul className="how-works__items">
                            <li className="how-works__item">
                                <span className="sprite icon--choose-resume mr-20">
                                    <i className="how-works--count">1</i>
                                </span>
                                <p>Choose your resume <br/>template</p>
                            </li>
                            
                            <li className="how-works__item justify-content-between">
                                <p>Verify your profile <br/>imported from Shine</p>
                                <span className="sprite icon--choose-verify">
                                    <i className="how-works--count">2</i>
                                </span>
                            </li>

                            <li className="how-works__item">
                                <span className="sprite icon--choose-download mr-20">
                                    <i className="how-works--count">3</i>
                                </span>
                                <p>Download your <br/>customised Resume</p>
                            </li>
                        </ul>
                    </div>
                </section>

                <ResumeSlider/>

                <section className="section pt-30 pb-30">
                    <div className="text-center">
                        <h2 className="section__head">Resume builder features</h2>
                        <p  className="section__subHead">Customise the resume as per your needs</p>
                    </div>

                    <div className="mt-20 resume-builder">
                        <ul className="resume-builder__items">
                            <li className="resume-builder__item"><i className="sprite icon--switch"></i>Switch template</li>

                            <li className="resume-builder__item"><i className="sprite icon--editText"></i>Edit text</li>

                            <li className="resume-builder__item"><i className="sprite icon--theme"></i>Theme change</li>

                            <li className="resume-builder__item"><i className="sprite icon--move"></i>Move sections</li>

                            <li className="resume-builder__item"><i className="sprite icon--upload"></i>Upload image</li>

                            <li className="resume-builder__item"><i className="sprite icon--preview"></i>Preview resume</li>
                        </ul>
                    </div>
                </section>
                <Testimonial/>

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


                <section className="section shine-learning mt-30">
                    <div className="text-center">
                        <div className="shine-learning--logo"></div>
                        <p  className="section__subHead">Shine Learning is India’s largest professional courses and career skills portal. Launched by Shine.com, Shine Learning has a vision to up-skill the Indian talent pool to adapt to the changing job market.</p>
                    </div>

                    <ul className="shine-learning__items">
                        <li className="shine-learning__item">Explore courses</li>
                        <li className="shine-learning__item">Job assistance</li>
                        <li className="shine-learning__item">Free rescources</li>
                        <li className="shine-learning__item">Talent economy</li>
                    </ul>
                </section>

                <section className="section mt-30">
                    <div className="text-center">
                        <h2 className="section__head">Reach out to us</h2>
                        <p  className="section__subHead">Feel free to share your feedback with us</p>
                    </div>

                    <div className="white-box mt-30 relative">
                        <ul className="line-form p-0 mt-10">
                            <li className="line-form__group">
                                <input type="text" id="name" className="line-form__input" placeholder="Full name" />
                                <label htmlFor="name" className="line-form__label">Full name</label>
                            </li>

                            <li>
                                <ul className="d-flex line-form__mobile">
                                    <li className="line-form__group code">
                                        <select class="line-form__select" id="skillRating">
                                            <option>+91</option>
                                            <option>+92</option>
                                            <option>+93</option>
                                        </select>
                                    </li>

                                    <li className="line-form__group number">
                                        <input type="text" id="name" className="line-form__input" placeholder="Mobile" />
                                        <label htmlFor="name" className="line-form__label">Mobile</label>
                                    </li>
                                </ul>
                            </li>

                            <li className="line-form__group">
                                <input type="text" id="name" className="line-form__input" placeholder="Message" />
                                <label htmlFor="name" className="line-form__label">Message</label>
                            </li>

                            <li className="d-flex justify-content-center">
                                <button className="btn btn__round btn__primary">Submit</button>
                            </li>
                        </ul>
                    </div>
                </section>
                <Footer/>
            </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {}
};

const mapDispatchToProps = (dispatch) => {
    return {
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);