import React, { Component } from 'react';
import './home.scss'
import { getCandidateId, loginCandidate, feedbackSubmit, getComponentTitle, getCandidateShineDetails, checkSessionAvaialability } from "../../../store/landingPage/actions";
import { connect } from "react-redux";
import Banner from "./Banner/banner.jsx";
import ResumeSlider from "./ResumeSlider/resumeSlider.jsx";
import Testimonial from "./Testimonial/testimonial.jsx";
import Footer from "../../Common/Footer/footer.jsx";
import Header from "../../Common/Header/header.jsx";
import LoaderPage from '../../Loader/loaderPage.jsx'
import { scroller } from 'react-scroll';
import queryString from "query-string";
import LoginModal from "../../Modal/loginModal";
import { hideModal, showModal, showLoginModal, hideLoginModal } from "../../../store/ui/actions";
import { displaySelectedTemplate } from '../../../store/template/actions';
import { eventClicked } from '../../../store/googleAnalytics/actions/index';
import {
    Redirect
} from 'react-router-dom'

class Home extends Component {
    constructor(props) {

        super(props);
        this.scrollTo = this.scrollTo.bind(this);
        this.addclass = this.addclass.bind(this);
        this.state = {
            'scrolled': false,
            'token': '',
            'login': ''
        }
        const values = queryString.parse(this.props.location.search);
        const token = (values && values.token) || '', login = (values && values.login) || '';

        this.state.token = token;
        this.state.login = login;
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.handleLoginSuccess = this.handleLoginSuccess.bind(this);
    }


    scrollTo(elem, action, label) {
        scroller.scrollTo(elem, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: -10
        });
        this.props.eventClicked({
            action,
            label
        })
    }

    addclass() {
        let scrollpos = window.scrollY;
        if (scrollpos > 60) {
            this.setState({
                'scrolled': true
            })
        } else {
            this.setState({
                'scrolled': false
            })
        }
    }


    handleLoginSuccess() {
        const { history, location } = this.props;
        const pathFrom = location.state && location.state.from || '';

        if (pathFrom) {
            history.push(pathFrom);
        }
        else {
            history.push('/resume-builder/edit/?type=profile')
        }
    }
    async componentDidMount() {

        if (typeof document !== 'undefined' && document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) {
            document.getElementsByClassName('chat-bot')[0].style.display = 'none';
        }

        if (this.state.token) {
            await this.props.loginCandidate({ alt: this.state.token }, this.props.history, true);
        }
        if (this.state.login === 'false') {
            const isSessionAvailable = await this.props.checkSessionAvaialability();
            if (isSessionAvailable) {
                try {
                    await this.props.getCandidateShineDetails()
                    const { state } = this.props.location;
                    if (state && state.from) {
                        this.props.history.push(state.from);
                    }
                }
                catch (e) {
                    console.log(e.message);
                }
                // redirect back from where it comes

            }
            else {
                await this.props.showLoginModal()
                // const { state } = this.props.location;
                // if (state && state.from) {
                //     this.props.history.push(state.from);
                // }
            }
        }

    }

    static getActions() {
        return [getComponentTitle]
    }

    static async fetching({ dispatch }, params) {
        let actionList = Home.getActions();
        const results = []
        for (const [index, value] of actionList.entries()) {
            try {
                results[index] = await new Promise((resolve, reject) => dispatch(value({
                    info: params,
                    resolve,
                    reject,
                    isTokenAvail: true
                })))
            }
            catch (e) {
                console.log('New error - ', e);
            }
        }
        return results;
    }

    render() {
        const { ui: { loader, loginModal }, userInfo, userInfo: { first_name, number, email }, feedback, eventClicked, loginCandidate, hideLoginModal } = this.props;

        return (
            <div className="nav-fixed">
                {
                    !!(loader) &&
                    <LoaderPage />
                }
                <Header
                    userName={first_name}
                    number={number}
                    email={email}
                    page={'home'}
                    eventClicked={eventClicked}
                    feedback={feedback}
                    getclass={this.state.scrolled ? 'color-change' : ''}
                    location={this.props.location} />
                <Banner
                    userName={first_name}
                    eventClicked={eventClicked} />
                <LoginModal
                    handleLoginSuccess={this.handleLoginSuccess}
                    loginCandidate={loginCandidate}
                    hideLoginModal={hideLoginModal}
                    loginModal={loginModal}
                    history={this.props.history}
                />
                <section className="section-container">
                    <h2>Resume builder advantages</h2>
                    <strong className="section-container--sub-head">Resume builder advantages which will make your
                        career brighter</strong>
                    <ul className="advantages mt-30">
                        <li className="advantages--list">
                            <div className="advantages--image">
                                <span className="icon-advantage1"></span>
                            </div>
                            <div className="advantages--content">
                                <strong>Visually Striking Resume</strong>
                                <p>Our resume layout optimizer makes sure all your
                                    content is aligned and organized so your resume looks
                                    like a work of art.</p>
                            </div>
                        </li>
                        <li className="advantages--list">
                            <div className="advantages--image">
                                <span className="icon-advantage2"></span>
                            </div>
                            <div className="advantages--content">
                                <strong>Unlimited Downloads</strong>
                                <p>Our Resume Builder subscription gives you the
                                    flexibility to edit and download your resume unlimited time</p>
                            </div>
                        </li>
                        <li className="advantages--list">
                            <div className="advantages--image">
                                <span className="icon-advantage3"></span>
                            </div>
                            <div className="advantages--content">
                                <strong>Higher Recruiter Views</strong>
                                <p>Each job has on average of 500 applicants with 95% of resume never read. Our resume
                                    builder increases the chances of your resume getting read.</p>
                            </div>
                        </li>
                        <li className="advantages--list">
                            <div className="advantages--image">
                                <span className="icon-advantage4"></span>
                            </div>
                            <div className="advantages--content">
                                <strong>Get your CV past screening software</strong>
                                <p>Most of the resume filtering is done by machine. So, it becomes very important to
                                    design your CV as per the ATS</p>
                            </div>
                        </li>
                    </ul>
                </section>

                <section id="works" className="section-container grey-bg">
                    <h2>How it works</h2>
                    <strong className="section-container--sub-head">Just 3 steps to create your perfect resume</strong>
                    <ul className="works mt-70">
                        <li className="works--list">
                            <div className="works--image">
                                <i>1</i>
                                <span className="icon-works1"></span>
                            </div>
                            <div className="works--content">
                                <h3>Choose your resume template</h3>
                                <p>Our professional resume templates are designed strictly following all industry
                                    guidelines and best practices employers are looking for.</p>
                            </div>
                        </li>
                        <li className="works--list">
                            <div className="works--image">
                                <i>2</i>
                                <span className="icon-works2"></span>
                            </div>
                            <div className="works--content">
                                <h3>Verify your profile imported from Shine</h3>
                                <p>We import your Shine Profile to create your resume automatically. You may edit the
                                    details, if required</p>
                            </div>
                        </li>
                        <li className="works--list">
                            <div className="works--image">
                                <i>3</i>
                                <span className="icon-works3"></span>
                            </div>
                            <div className="works--content">
                                <h3>Start impressing employers</h3>
                                <p>Download your awesome resume from you email and land the job you are looking for,
                                    effortlessly.</p>
                            </div>
                        </li>
                    </ul>
                </section>

                <ResumeSlider
                    {...this.props}
                    page={'home'}
                />

                <section className="section-container">
                    <h2>Resume builder features</h2>
                    <strong className="section-container--sub-head">Customise the resume as per your needs</strong>
                    <ul className="features mt-30">
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features1"></span>
                            </div>
                            <div className="features--content">
                                <strong>Expert assistance</strong>
                                <p>Get professional summary and job profile recommendation</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features2"></span>
                            </div>
                            <div className="features--content">
                                <strong>Import data from Shine</strong>
                                <p>You can import all data from your shine profile to your resume</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features3"></span>
                            </div>
                            <div className="features--content">
                                <strong>Update resume back to Shine</strong>
                                <p>You can update your resume on your shine profile</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features4"></span>
                            </div>
                            <div className="features--content">
                                <strong>Customize your resume</strong>
                                <p>Customize your resume with professional font, colors and templates</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features5"></span>
                            </div>
                            <div className="features--content">
                                <strong>Reorder sections</strong>
                                <p>All sections on resume can be reorder anywhere where you want</p>
                            </div>
                        </li>
                        <li className="features--list">
                            <div className="features--image">
                                <span className="icon-features6"></span>
                            </div>
                            <div className="features--content">
                                <strong>Display your photo</strong>
                                <p>Display your photo in your resume for more views</p>
                            </div>
                        </li>
                    </ul>

                    <button className="orange-button"
                        onClick={() => this.scrollTo('templates', 'BuildResume', 'Features')}>Build your resume
                    </button>

                </section>

                <section className="section-container">
                    <h2>Next generation ready resume</h2>
                    <strong className="section-container--sub-head">Difference between shine resume and others</strong>

                    <div>
                        <img className="img-responsive" alt={"Next generation ready resume"}
                            src={`${this.staticUrl}react/assets/images/nextgen-resume.jpg`} />
                    </div>

                </section>

                <Testimonial />

                <section className="section-container flex-container text-center">
                    <div className="shinelearning">
                        <span className="icon-shinelearning"></span>
                        <p>Shine Learning is India’s largest professional courses and career skills portal. Launched by
                            Shine.com, Shine Learning has a vision to up-skill the Indian talent pool to adapt to the
                            changing job market.</p>
                        <ul>
                            <li><a href="https://learning.shine.com/" className="hyper-link-urls" >Explore courses</a></li>
                            <li> <a href="https://learning.shine.com/services/resume-writing/63/" className="hyper-link-urls">Job assistance</a></li>
                            <li>  <a href="https://learning.shine.com/cms/resume-format/1/" className="hyper-link-urls" >Free rescources</a></li>
                            <li><a href="https://learning.shine.com/talenteconomy/" className="hyper-link-urls">Talent economy</a></li>
                        </ul>
                    </div>
                </section>

                <Footer />
            </div>
        )
    }
}


const mapStateToProps = (state) => {
    return {
        userInfo: state.personalInfo,
        ui: state.ui,
        template: state.template,
        analytics: state.analytics
    }
};


const mapDispatchToProps = (dispatch) => {
    return {
        "getCandidateId": () => {
            return dispatch(getCandidateId())
        },
        "loginCandidate": (payload, history, isTokenAvail) => {
            return new Promise((resolve, reject) => {
                return dispatch(loginCandidate({ info: payload, resolve, reject, history, isTokenAvail: isTokenAvail }))
            })
        },
        "getCandidateShineDetails": () => {
            return new Promise((resolve, reject) => {
                return dispatch(getCandidateShineDetails({ resolve, reject }))
            })
        },
        'showModal': () => {
            return dispatch(showModal())
        },
        'hideModal': () => {
            return dispatch(hideModal())
        },
        'showLoginModal': () => {
            return dispatch(showLoginModal())
        },
        'hideLoginModal': () => {
            return dispatch(hideLoginModal())
        },
        'displaySelectedTemplate': (templateId) => {
            return dispatch(displaySelectedTemplate(templateId))
        },
        'feedback': (values) => {
            return dispatch(feedbackSubmit(values))
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        },
        'checkSessionAvaialability': () => {
            return new Promise((resolve, reject) => {
                return dispatch(checkSessionAvaialability({ resolve, reject }))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);
