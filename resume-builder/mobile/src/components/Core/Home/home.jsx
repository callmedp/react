import React, { Component } from 'react';
import Header from '../../Common/Header/header.jsx';
import Footer from '../../Common/Footer/footer.jsx';
import { connect } from "react-redux";
import './home.scss'
import { getCandidateId, loginCandidate, feedbackSubmit, getComponentTitle, getCandidateShineDetails, checkSessionAvaialability } from "../../../store/landingPage/actions/index.js";
import Banner from './Banner/banner.jsx';
import ResumeSlider from './ResumeSlider/resumeSlider.jsx';
import Testimonial from './Testimonial/testimonial.jsx';
import queryString from "query-string";
import { scroller } from 'react-scroll';
import Loader from '../../Common/Loader/loader.jsx';
import { eventClicked } from '../../../store/googleAnalytics/actions/index'
import { showLoginModal, hideLoginModal } from '../../../store/ui/actions/index'
import LoginModal from '../../Common/LoginModal/loginModal.jsx'
import { trackUser } from '../../../store/tracking/actions/index'
import { isTrackingInfoAvailable, getTrackingInfo, storeTrackingInfo, updateProductAvailability} from '../../../Utils/common';

class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'token': '',
            'login': ''
        }

        const values = queryString.parse(this.props.location.search);
        this.scrollTo = this.scrollTo.bind(this);
        const token = (values && values.token) || '', login = (values && values.login) || '';
        this.state.token = token;
        this.state.login = login;
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.handleLoginSuccess = this.handleLoginSuccess.bind(this);
        this.sendTrackingInfo = this.sendTrackingInfo.bind(this);
        this.handleBuildYourResumeClick = this.handleBuildYourResumeClick.bind(this);
        this.handleExitTracking = this.handleExitTracking.bind(this);
    }


    sendTrackingInfo(action, position) {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId, productId } = getTrackingInfo();
            const {userTrack} = this.props;
            userTrack({ trackingId, productTrackingMappingId, productId, action, position });
        }
    }

    async componentDidMount() {

        const query = new URLSearchParams(this.props.location.search);
        const trackingId = query.get('t_id')
        
        if(trackingId !== null){
            const productTrackingMappingId = '11'
            storeTrackingInfo(trackingId, productTrackingMappingId, '')
            this.sendTrackingInfo('enter_home_page',1);
        }

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
                    // redirect back from where it comes
                    const { state } = this.props.location;
                    if (state && state.from) {
                        this.props.history.push(state.from);
                    }
                }
                catch (e) {
                    console.log(e.message);
                }

            }
            else {
                await this.props.showLoginModal()
                // const { state } = this.props.location;
                // if (state && state.from) {
                //     this.props.history.push(state.from);
                // }
            }
        }
        const values = queryString.parse(this.props.location.search);
        const template = (values && values.template) || '';

        if (template === "false") {
            this.scrollTo('templates', -15, 'Templates', 'Header')
        }

    }

    handleBuildYourResumeClick(){
        this.scrollTo('templates', 'BuildResume', 'Features');
        this.sendTrackingInfo('home_page_build_your_resume',1);
    }

    handleExitTracking(){
        this.sendTrackingInfo('exit_home_page',1);
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
        return [getComponentTitle]
    }

    static async fetching({ dispatch }, params) {
        const actionList = Home.getActions()
        const results = [];
        for (const [index, value] of actionList.entries()) {
            // if (index == 0 && !(params && params.alt)) {
            //     continue;
            // }
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
                <Banner 
                userName={first_name} 
                eventClicked={eventClicked} 
                sendTrackingInfo = {this.sendTrackingInfo}  />
                {
                    !!(mainloader)
                    && <Loader />
                }
                <LoginModal  {...this.props} handleLoginSuccess={this.handleLoginSuccess} />

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

                <ResumeSlider showtext={true} eventClicked={eventClicked} {...this.props} sendTrackingInfo ={this.sendTrackingInfo}/>

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
                        <a className="btn btn__shadow btn__round btn__primary" alt="Build Your Resume"
                            onClick={this.handleBuildYourResumeClick}>Build your resume</a>
                    </div>

                </section>
                <section className="section pt-30 pb-30">
                    <div className="text-center">
                        <h2 className="section__head">Next generation ready resume</h2>
                        <p className="section__subHead">Difference between shine resume and others</p>
                    </div>

                    <div className="mt-20 resume-builder">
                        <img src={`${this.staticUrl}react/assets/images/mobile/nextgen-resume.jpg`} alt="Resume Template"
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
                        <li className="shine-learning__item">
                            <a className="shine-learning__anchortag" href="https://learning.shine.com/" onClick={this.handleExitTracking}>Explore courses</a></li>
                        <li className="shine-learning__item shine-learning__anchortag"><a className="shine-learning__anchortag" href="https://learning.shine.com/services/resume-writing/63/" onClick={this.handleExitTracking}>Job assistance</a></li>
                        <li className="shine-learning__item shine-learning__anchortag"><a className = "shine-learning__anchortag" href="https://learning.shine.com/cms/resume-format/1/" onClick={this.handleExitTracking}>Free rescources</a></li>
                        <li className="shine-learning__item shine-learning__anchortag"><a className ="shine-learning__anchortag" href="https://learning.shine.com/talenteconomy/" onClick={this.handleExitTracking}>Talent economy</a></li>
                    </ul>
                </section>


                <Footer 
                sendTrackingInfo = {this.sendTrackingInfo}/>
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
        "loginCandidate": (payload, history, isTokenAvail) => {
            return new Promise((resolve, reject) => {
                dispatch(loginCandidate({ info: payload, resolve, reject, history, isTokenAvail: isTokenAvail }))
            })
        },
        "getCandidateShineDetails": () => {
            return new Promise((resolve, reject) => {
                return dispatch(getCandidateShineDetails({ resolve, reject }))
            })
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        },
        'showLoginModal': () => {
            return dispatch(showLoginModal())
        },
        'hideLoginModal': () => {
            return dispatch(hideLoginModal())
        },
        'checkSessionAvaialability': () => {
            return new Promise((resolve, reject) => {
                return dispatch(checkSessionAvaialability({ resolve, reject }))
            })
        },
        "userTrack" : (data) => dispatch(trackUser(data)),
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);