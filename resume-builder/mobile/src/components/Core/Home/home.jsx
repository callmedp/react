import React, { Component } from 'react';
import Header from '../../Common/Header/header.jsx';
import Footer from '../../Common/Footer/footer.jsx';
import { connect } from "react-redux";
import './home.scss'
import { getCandidateId, loginCandidate, feedbackSubmit, getComponentTitle } from "../../../store/landingPage/actions/index.js";
import Banner from './Banner/banner.jsx';
import ResumeSlider from './ResumeSlider/resumeSlider.jsx';
import Testimonial from './Testimonial/testimonial.jsx';
import queryString from "query-string";
import { scroller } from 'react-scroll';
import Loader from '../../Common/Loader/loader.jsx';
import { eventClicked } from '../../../store/googleAnalytics/actions/index'
class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'token': ''
        }
        if (document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) {
            document.getElementsByClassName('chat-bot')[0].style.display = 'none';
        }
        const values = queryString.parse(this.props.location.search);
        this.scrollTo = this.scrollTo.bind(this);
        const token = (values && values.token) || '';
        this.state.token = token;
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
    }

    async componentDidMount() {
        if (this.state.token) {
            await this.props.loginCandidate(this.state.token);
        }
    }

    scrollTo(elem, action, label) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -50
        });
        this.props.eventClicked({
            action,
            label
        })
    }

    static getActions() {
        return [loginCandidate, getComponentTitle]
    }

    static async fetching({ dispatch }, params) {
        const actionList = Home.getActions()
        const results = [];
        for (const [index, value] of actionList.entries()) {
            if (index == 0 && !(params && params.alt)) {
                continue;
            }
            results[index] = await new Promise((resolve, reject) => dispatch(value({
                info: params,
                resolve,
                reject,
                isTokenAvail: true
            })))
        }
        return results;
    }


    render() {
        const { ui: { mainloader }, userInfo: { first_name }, eventClicked } = this.props;
        return (
            <div className="home">
                <Header eventClicked={eventClicked} />
                <Banner userName={first_name} eventClicked={eventClicked} />
                {
                    !!(mainloader)
                    && <Loader />
                }


                <section className="section professional">
                    <div className="text-center">
                        <h2 className="section__head">Resume builder advantages</h2>
                        <p className="section__subHead">Resume builder advantages which will make your career
                            brighter</p>
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
                        <p className="section__subHead">Just 3 steps to create your perfect resume</p>
                    </div>

                    <div className="white-box mt-30">
                        <ul className="how-works__items">
                            <li className="how-works__item">
                                <span className="sprite icon--choose-resume mr-20">
                                    <i className="how-works--count">1</i>
                                </span>
                                <p>Choose your resume <br />template</p>
                            </li>

                            <li className="how-works__item justify-content-between">
                                <p>Verify your profile <br />imported from Shine</p>
                                <span className="sprite icon--choose-verify">
                                    <i className="how-works--count">2</i>
                                </span>
                            </li>

                            <li className="how-works__item">
                                <span className="sprite icon--choose-download mr-20">
                                    <i className="how-works--count">3</i>
                                </span>
                                <p>Start impressing employers with new resume</p>
                            </li>
                        </ul>
                    </div>
                </section>

                <ResumeSlider showtext={true} eventClicked={eventClicked} />

                <section className="section pt-30 pb-30">
                    <div className="text-center">
                        <h2 className="section__head">Resume builder features</h2>
                        <p className="section__subHead">Customise the resume as per your needs</p>
                    </div>

                    <div className="mt-20 resume-builder">
                        <ul className="resume-builder__items">
                            <li className="resume-builder__item"><i className="sprite icon--switch"></i>Expert
                                assistance
                            </li>

                            <li className="resume-builder__item"><i className="sprite icon--import"></i>Import data from
                                Shine
                            </li>

                            <li className="resume-builder__item"><i className="sprite icon--update"></i>Update resume
                                back to Shine
                            </li>

                            <li className="resume-builder__item"><i className="sprite icon--custom-resume"></i>Customize
                                your resume
                            </li>

                            <li className="resume-builder__item"><i className="sprite icon--reorder-home"></i>Reorder
                                resume sections
                            </li>

                            <li className="resume-builder__item"><i className="sprite icon--display-home"></i>Display
                                your photo
                            </li>
                        </ul>
                    </div>

                    <div className="text-center mt-30">
                        <a className="btn btn__shadow btn__round btn__primary"
                            onClick={() => this.scrollTo('templates', 'BuildResume', 'Features')}>Build your resume</a>
                    </div>

                </section>
                <section className="section pt-30 pb-30">
                    <div className="text-center">
                        <h2 className="section__head">Next generation ready resume</h2>
                        <p className="section__subHead">Difference between shine resume and others</p>
                    </div>

                    <div className="mt-20 resume-builder">
                        <img src={`${this.staticUrl}react/assets/images/mobile/nextgen-resume.jpg`} alt=""
                            className="img-fluid" />
                    </div>
                </section>
                <Testimonial />
                <section className="section shine-learning mt-30 mb-40">
                    <div className="text-center">
                        <div className="shine-learning--logo"></div>
                        <p className="section__subHead">Shine Learning is India’s largest professional courses and
                            career skills portal. Launched by Shine.com, Shine Learning has a vision to up-skill the
                            Indian talent pool to adapt to the changing job market.</p>
                    </div>

                    <ul className="shine-learning__items">
                        <li className="shine-learning__item">Explore courses</li>
                        <li className="shine-learning__item">Job assistance</li>
                        <li className="shine-learning__item">Free rescources</li>
                        <li className="shine-learning__item">Talent economy</li>
                    </ul>
                </section>


                <Footer />
            </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        ui: state.ui,
        userInfo: state.personalInfo,

    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "getCandidateId": () => {
            return dispatch(getCandidateId())
        },
        "loginCandidate": (token) => {
            return new Promise((resolve, reject) => {
                dispatch(loginCandidate({ info: { alt: token }, resolve, reject, isTokenAvail: true }))
            })
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);