import React, { Component } from 'react';
import Header from '../../../Common/Header/header.jsx';
import './buy.scss';
import * as action from '../../../../store/buy/actions';
import { fetchThumbNailImages, fetchSelectedTemplateImage } from '../../../../store/template/actions/index'
import { fetchPersonalInfo } from '../../../../store/personalInfo/actions/index'
import { showGenerateResumeModal, hideGenerateResumeModal } from '../../../../store/ui/actions/index'
import { connect } from "react-redux";
import { siteDomain } from "../../../../Utils/domains";
import Slider from "react-slick";
import Loader from '../../../Common/Loader/loader.jsx';
import BuyTemplateModal from '../../../Common/BuyTemplateModal/buyTemplateModal.jsx';
import { eventClicked } from '../../../../store/googleAnalytics/actions/index'
import { loginCandidate } from "../../../../store/landingPage/actions";
import { apiError } from '../../../../Utils/apiError.js';
import AlertModal from '../../../Common/AlertModal/alertModal';
import {isTrackingInfoAvailable, getTrackingInfo,} from '../../../../Utils/common';
import { trackUser } from '../../../../store/tracking/actions/index'

class Buy extends Component {

    constructor(props) {
        super(props);

        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.state = {
            'checked': 'product1',
            'modal_status': false,
            'template_id': '',
            'resumeDownloadCount': -1,
            'freeDownloadButtonDisable': false,
        }
        this.closeModalStatus = this.closeModalStatus.bind(this);
        this.openModal = this.openModal.bind(this);
        this.editTemplate = this.editTemplate.bind(this);
        this.freeResumeRequest = this.freeResumeRequest.bind(this);
        this.pollingUserInfo = this.pollingUserInfo.bind(this);
        this.downloadRequestedResume = this.downloadRequestedResume.bind(this);
        this.timerFunction = this.timerFunction.bind(this);
        this.sendTrackingInfo = this.sendTrackingInfo.bind(this);
    }


    redirectToCart() {

       
        this.props.eventClicked({
            'action': 'PayNow',
            'label': 'Click'
        })
        if (!this.props.productIds[0])
            return;
        let product;


        if (this.state.checked === 'product1') {
            product = this.props.productIds[0]
        } else {
            product = this.props.productIds[1]
        }
        const data = {
            "prod_id": product.id,
            "cart_type": 'cart'
        }
        this.sendTrackingInfo('enroll_now',1,product.id)
        this.props.addToCart(data);
    }

    closeModalStatus() {
        this.setState({ modal_status: false })
    }

    async openModal(index) {
        await this.props.fetchSelectedTemplateImage(index + 1)
        this.setState({ modal_status: true, template_id: index + 1 })
    }

    async componentDidMount() {
        // check if the userexperinece is greater or equal to 4 years. (7 is the pid for 4 years (mapping done here))

        if (parseInt(localStorage.getItem('userExperience') || 0) >= 7) {
            if (typeof document !== 'undefined' && document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) {
                document.getElementsByClassName('chat-bot')[0].style.display = 'none';
            }
        }
        else {
            if (typeof document !== 'undefined' && document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) {
                document.getElementsByClassName('chat-bot')[0].style.display = 'block';
            }
        }

        const { getProductIds, fetchThumbNailImages, fetchUserInfo } = this.props
        if (!localStorage.getItem('candidateId')) {
            await this.props.loginCandidate()
        }
        // get userInfo from LocalStorage
        if (localStorage.getItem('email')) window['email'] = localStorage.getItem('email')
        else window['email'] = ''
        if (localStorage.getItem('mobile')) window['mobile'] = localStorage.getItem('mobile')
        else window['mobile'] = ''
        if (localStorage.getItem('name')) window['name'] = localStorage.getItem('name')
        else window['name'] = ''

        getProductIds();
       // fetchThumbNailImages();
        fetchUserInfo();
    }

    componentDidUpdate(prevProps) {
        if (this.props.userInfo !== prevProps.userInfo) {
            if (this.state.resumeDownloadCount >= 0 && (this.state.resumeDownloadCount < this.props.userInfo.resume_creation_count)) {
                clearInterval(this.state.timerId)
                this.downloadRequestedResume();
            }
        }
    }

    async downloadRequestedResume() {
        this.sendTrackingInfo('download_requested_resume',1)
        const { hideGenerateResumeModal } = this.props
        const candidateId = localStorage.getItem('candidateId')
        const selectedTemplate = localStorage.getItem('selected_template', 1)
        const url = `${siteDomain}/api/v1/resume/candidate/${candidateId}/free-resume/template/${selectedTemplate}/`
        const link = document.createElement('a');
        link.href = url;
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
        hideGenerateResumeModal()
        this.setState({ 'freeDownloadButtonDisable': false })
    }

    async freeResumeRequest() {
        this.sendTrackingInfo('free_resume_request',1);
        const { requestFreeResume, showGenerateResumeModal,
            userInfo: { resume_creation_count }, } = this.props

        this.setState({ 'resumeDownloadCount': resume_creation_count, 'freeDownloadButtonDisable': true }, async () => {
            await requestFreeResume()
            showGenerateResumeModal()
            this.pollingUserInfo()
        })
    }

    pollingUserInfo() {
        const timer = setInterval(this.timerFunction, 2000);
        const startTime = new Date().getTime();
        this.setState({ 'timerId': timer, 'pollingStartTIme': startTime })
    }

    timerFunction() {
        const { fetchUserInfo } = this.props
        const { timerId, pollingStartTIme } = this.state
        if (new Date().getTime() - pollingStartTIme > 30000) {  // max limit 10*3 seconds
            clearInterval(timerId)
            this.setState({ 'freeDownloadButtonDisable': false })
            hideGenerateResumeModal()
            apiError()
        }
        fetchUserInfo(true);
    }

    handleOnChange(checkedProduct) {
        if (checkedProduct === 'product1') {
            this.setState({
                'checked': 'product1'
            })
        } else {
            this.setState({
                'checked': 'product2'
            })
        }
    }

    editTemplate() {
        this.sendTrackingInfo('buy_edit_tempate',1);
        const { eventClicked, history } = this.props;
        eventClicked({
            'action': 'EditTemplate',
            'label': 'Click'
        })
        history.push(`/resume-builder/edit/?type=profile`)
    }

    sendTrackingInfo(action, position, productId="") {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId} = getTrackingInfo();
            const {userTrack} = this.props;
            userTrack({ trackingId, productTrackingMappingId, productId, action, position });
        }
    }

    render() {
        const settings = {
            dots: false,
            infinite: true,
            speed: 500,
            slidesToShow: 2,
        };
        const { ui: { mainloader, generateResumeModal }, template: { thumbnailImages, templateImage }, productIds, history,
            userInfo: { free_resume_downloads, resume_creation_count } } = this.props
        const template = localStorage.getItem('selected_template') || 1;
        const { checked, modal_status, freeDownloadButtonDisable } = this.state
        const price1 = productIds[0] ? productIds[0].inr_price : 999, discount1 = productIds[0] ? productIds[0].discount : 50,
            heading1 = productIds[0] ? productIds[0].heading : "14 DAYS PLAN",
            fakePrice1 = productIds[0] ? productIds[0].fake_inr_price : 99;
        const price2 = productIds[1] ? productIds[1].inr_price : 1248,
            discount2 = productIds[1] ? productIds[1].discount : 50,
            heading2 = productIds[1] ? productIds[1].heading : "YEARLY PLAN",
            fakePrice2 = productIds[1] ? productIds[1].fake_inr_price : 1999;
        const free_download_count = free_resume_downloads - resume_creation_count
        return (

            <div className="buy-container">
                <Header page={"buy"} history={history} />
                {mainloader ? <Loader /> : ""}
                {modal_status ? <BuyTemplateModal modal_status={modal_status}
                    closeModalStatus={this.closeModalStatus}
                    templateImage={templateImage} /> : ''}
                <AlertModal modal_status={generateResumeModal} generateResumeModal={generateResumeModal} />
                <div className="pay-now">
                    <div className="pay-now__price">
                        <span className="fs-12 pay-now__price--pay">You pay</span>
                        <span
                            className="fs-26 color-333 semi-bold">Rs. {checked === 'product1' ? price1 : price2}/-</span>
                    </div>

                    <button className="btn btn__round btn__primary fs-"
                        onClick={this.redirectToCart.bind(this)}>Pay Now
                    </button>
                </div>


                <div className="buy">
                    <div className="d-flex mb-30">
                        <div className="mr-auto">
                            <p className="fs-20 color-333"> Your customised <br></br>resume is ready </p>
                            <button class="btn btn--sm btn__round btn--outline mt-10" onClick={this.editTemplate}>Edit template</button>
                        </div>


                        <div className="position-relative">
                            <span className="buy__item--image">
                                {thumbnailImages.length === 5 ?
                                    <img src={`data:image/png;base64, ${thumbnailImages[template - 1]}`}
                                        alt="Resume" /> :
                                    <img
                                        src={`${this.staticUrl}react/assets/images/mobile/small-resume-${template}.jpg`}
                                        alt="Custom resume" />
                                }
                            </span>
                            <a className="sprite icon--zoom2" onClick={() => {
                                this.openModal(parseInt(template - 1))
                            }}></a>
                        </div>
                    </div>

                    <div className="buy__wrap mt-15">
                        <div className="buy__item">
                            <div className="buy__item--left w-100">
                                <input className="buy__item--input form__radio-input" type="radio" id="your-resume"
                                    name="product-1"
                                    checked={checked === 'product1' ? true : false}
                                    onChange={this.handleOnChange.bind(this, 'product1')}></input>
                                <label className="buy__item--label form__radio-label" htmlFor="your-resume">
                                    <span className="form__radio-button"></span>
                                    <span className="text-uppercase d-block color-333 bold">{heading1}</span>
                                    <span className="d-flex align-items-center">
                                        <strong className="mr-10">Rs. {price1}/-</strong>
                                        <span className="line-through fs-16 color-999 font-weight-light">Rs. {fakePrice1}</span>
                                    </span>
                                    <span className="fs-14">Save upto {discount1}%</span>
                                </label>
                            </div>
                        </div>

                        <div className="buy__item buy__recommended">
                            <div className="buy__recommended--tag">Recommended</div>
                            <div className="buy__item--left w-100">
                                <input className="buy__item--input form__radio-input" type="radio" id="all-resumes"
                                    name="product2"
                                    checked={checked === 'product2' ? true : false}
                                    onChange={this.handleOnChange.bind(this, 'product2')}>
                                </input>

                                <label className="buy__item--label form__radio-label" htmlFor="all-resumes">
                                    <span className="form__radio-button"></span>
                                    <span className="text-uppercase d-block color-333 bold">{heading2}</span>
                                    <span className="d-flex align-items-center">
                                        <strong className="mr-10">Rs. {price2}/-</strong>
                                        <span className="line-through fs-16 color-999 font-weight-light">Rs. {fakePrice2}</span>
                                    </span>
                                    <span className="fs-14">Save upto {discount2}%</span>
                                </label>
                            </div>
                        </div>

                        <div className="buy__item buy__recommended buy__youGet pt-15">
                            <p className="buy__youGet--head">You will get</p>
                            <ul className="buy__youGet__list mt-10">
                                <li><span></span>Unlimited Downloads</li>
                                <li><span></span>All Resume Templates</li>
                                <li><span></span>100% access to all features</li>
                                <li><span></span>Auto-upgrade of new features</li>
                            </ul>
                        </div>
                    </div>

                    {free_resume_downloads ?
                        <div class="buy__wrap mt-15">
                            <div className="buy__item buy__trial">
                                <div className="buy__recommended--tag">Trial offer</div>
                                <div className="buy_item--left">
                                    {free_download_count > 0 ? ` ${free_download_count} free download for 1st time users.` :
                                        "Free one time download for all 1st time users"}
                                </div>
                                <div className="buy_item--right">
                                    <button class="btn btn__round btn--outline" onClick={this.freeResumeRequest}
                                        disabled={freeDownloadButtonDisable} >Download</button>
                                </div>
                            </div>
                        </div> : ''
                    }
                </div>
            </div>

        )
    }
}

const mapStateToProps = (state) => {
    return {
        productIds: state.productIds,
        ui: state.ui,
        template: state.template,
        userInfo: state.personalInfo,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        'fetchUserInfo': (noUiLoader) => {
            return dispatch(fetchPersonalInfo({ noUiLoader }))
        },
        'getProductIds': () => {
            return dispatch(action.getProductIds())
        },
        'fetchThumbNailImages': () => {
            return dispatch(fetchThumbNailImages())
        },
        'fetchSelectedTemplateImage': (template_id) => {
            return new Promise((resolve, reject) => {
                return dispatch(fetchSelectedTemplateImage({ template_id, resolve, reject }))
            })
        },
        'addToCart': (data) => {
            return new Promise((resolve, reject) => {
                dispatch(action.addToCart({ data, resolve, reject }));
            })
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        },
        "loginCandidate": (token) => {
            return new Promise((resolve, reject) => {
                dispatch(loginCandidate({ info: { alt: token }, resolve, reject, isTokenAvail: false }))
            })
        },
        "requestFreeResume": () => {
            return new Promise((resolve, reject) => {
                dispatch(action.requestFreeResume({ resolve, reject }))
            })
        },
        'showGenerateResumeModal': () => {
            return dispatch(showGenerateResumeModal())
        },
        'hideGenerateResumeModal': () => {
            return dispatch(hideGenerateResumeModal())
        },
        "userTrack" : ( data ) => dispatch(trackUser(data)),
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Buy);