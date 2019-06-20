import React, {Component} from 'react';
import Header from '../../Common/Header/header.jsx';
import Footer from '../../Common/Footer/footer.jsx';
import {connect} from "react-redux";
import './home.scss'
import * as actions from "../../../store/landingPage/actions";
import Banner from './Banner/banner.jsx';
import ResumeSlider from './ResumeSlider/resumeSlider.jsx';
import Testimonial from './Testimonial/testimonial.jsx';
import queryString from "query-string";
import {Events, animateScroll as scroll, scrollSpy, scroller} from 'react-scroll'
import Loader from '../../Common/Loader/loader.jsx';

class Home extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            'token': ''
        }
        const values = queryString.parse(this.props.location.search);
        this.scrollTo = this.scrollTo.bind(this);
        const token = (values && values.token) || '';
        this.state.token = token;
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
    }
    componentDidMount() {
        this.props.loginCandidate(this.state.token);
    }

    scrollTo(elem) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -50
        })
    }
    
    render() {
        const {ui:{mainloader}} = this.props;
        return (
            <div className="home">
                <Header />
                <Banner/>
                {mainloader ? <Loader/> :""}
                

                <section className="section professional">
                    <div className="text-center">
                        <h2 className="section__head">Resume builder advantages</h2>
                        <p  className="section__subHead">Resume builder advantages which will make your career brighter</p>
                    </div>

                    <ul className="professional__items">
                        <li className="professional__item">
                            <span>
                                <i className="sprite icon--resume"></i>
                            </span>
                            Visually Striking Resume
                        </li>
                        
                        <li className="professional__item">
                            <span>
                                <i className="sprite icon--create"></i>
                            </span>
                            Unlimited Downloads of your customised resume  
                        </li>
                        
                        <li className="professional__item">
                            <span>
                                <i className="sprite icon--increase"></i>
                            </span>
                            Get higher Recruiter Views of your resume 
                        </li>
                        
                        <li className="professional__item">
                            <span>
                                <i className="sprite icon--application"></i>
                            </span>
                            Get your CV past screening software
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

                <ResumeSlider showtext={true}/>

                <section className="section pt-30 pb-30">
                    <div className="text-center">
                        <h2 className="section__head">Resume builder features</h2>
                        <p  className="section__subHead">Customise the resume as per your needs</p>
                    </div>

                    <div className="mt-20 resume-builder">
                        <ul className="resume-builder__items">
                            <li className="resume-builder__item"><i className="sprite icon--switch"></i>Expert assistance</li>

                            <li className="resume-builder__item"><i className="sprite icon--import"></i>Import data from Shine</li>

                            <li className="resume-builder__item"><i className="sprite icon--update"></i>Update resume back to Shine</li>

                            <li className="resume-builder__item"><i className="sprite icon--custom-resume"></i>Customize your resume</li>

                            <li className="resume-builder__item"><i className="sprite icon--reorder-home"></i>Reorder resume sections</li>

                            <li className="resume-builder__item"><i className="sprite icon--display-home"></i>Display your photo</li>
                        </ul>
                    </div>

                    <div className="text-center mt-30">
                        <a className="btn btn__shadow btn__round btn__primary" onClick={() => this.scrollTo('templates')}>Build your resume</a>
                    </div>
               
                    </section>
                <section className="section pt-30 pb-30">
                    <div className="text-center">
                        <h2 className="section__head">Next generation ready resume</h2>
                        <p  className="section__subHead">Difference between shine resume and others</p>
                    </div>

                    <div className="mt-20 resume-builder">
                        <img src={`${this.staticUrl}react/assets/images/mobile/nextgen-resume.jpg`} alt=""
                     className="img-fluid"/>
                    </div>
                </section>
                <Testimonial/>
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

                <section className="section mt-30 grey-bg">
                    <div className="text-center">
                        <h2 className="section__head">Reach out to us</h2>
                        <p  className="section__subHead">Feel free to share your feedback with us</p>
                    </div>

                    <div className="white-box mt-30 mb-30 relative">
                        <ul className="line-form p-0 mt-10">
                            <li className="line-form__group">
                                <input type="text" id="name" className="line-form__input" placeholder="Full name" />
                                <label htmlFor="name" className="line-form__label">Full name</label>
                            </li>

                            <li>
                                <ul className="d-flex line-form__mobile">
                                    <li className="line-form__group code">
                                        <select className="line-form__select" id="skillRating">
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
                                <button className="btn btn__medium btn__round btn__primary">Submit</button>
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
    return {
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "getCandidateId": () => {
            return dispatch(actions.getCandidateId())
        },
        "loginCandidate": (token) => {
            return dispatch(actions.loginCandidate({alt: token}))
        }

    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);