import React, { Component } from 'react';
import './buy.scss';
import { Link } from 'react-router-dom';
import TopBar from '../../Editor/TopBar/topBar.jsx'
import Header from '../../../Common/Header/header.jsx'
import Footer from '../../../Common/Footer/footer.jsx'
import * as action from '../../../../store/buy/actions'
import {
    showModal, hideModal, updateUi, showSelectTemplateModal, hideSelectTemplateModal,
    hideGenerateResumeModal, showGenerateResumeModal
} from "../../../../store/ui/actions"
import { connect } from "react-redux";
import TemplateModal from '../../../Modal/tempateModal'
import Slider from "react-slick";
import moment from "moment"
import { fetchPersonalInfo, updatePersonalInfo, getComponentTitle } from '../../../../store/personalInfo/actions/index'
import SelectTemplateModal from '../../../Modal/selectTemplateModal';
import LoaderPage from '../../../Loader/loaderPage';
import { siteDomain } from '../../../../Utils/domains'
import {
    displaySelectedTemplate,
    fetchDefaultCustomization,
    fetchSelectedTemplateImage,
    fetchThumbNailImages
} from "../../../../store/template/actions";
import { eventClicked } from '../../../../store/googleAnalytics/actions/index'
import { loginCandidate } from "../../../../store/landingPage/actions";
import { Toast } from '../../../../services/ErrorToast';
import propTypes from 'prop-types';


export class Buy extends Component {
    static propTypes = {
        fetchSelectedTemplateImage: propTypes.func,
        showModal: propTypes.func,
        eventClicked: propTypes.func,
        showSelectTemplateModal: propTypes.func,
        userInfo: propTypes.shape({
            active_subscription: propTypes.bool,
            candidate_id: propTypes.string,
            date_of_birth: propTypes.string,
            email: propTypes.string,
            entity_preference_data: propTypes.array,
            extra_info: propTypes.string,
            extracurricular: propTypes.array,
            first_name: propTypes.string,
            free_resume_downloads: propTypes.number,
            gender: propTypes.object,
            id: propTypes.number,
            image: propTypes.string,
            interest_list: propTypes.array,
            last_name: propTypes.string,
            location: propTypes.string,
            number: propTypes.string,
            selected_template: propTypes.string,
            order_data: propTypes.object,
            resume_creation_count: propTypes.number,
            resume_generated: propTypes.bool,
            upload_resume: propTypes.bool,
        }),
        hideGenerateResumeModal: propTypes.func,
        requestFreeResume: propTypes.func,
        showGenerateResumeModal: propTypes.func,
        fetchUserInfo: propTypes.func,
        productIds: propTypes.shape({
            ids: propTypes.array
        }),
        showLoader: propTypes.func,
        addToCart: propTypes.func,
        getProductIds: propTypes.func,
        template: propTypes.shape({
            color: propTypes.number,
            entity_id_count_mapping: propTypes.object,
            entity_position: propTypes.string,
            heading_font_size: propTypes.number,
            html: propTypes.string,
            modalTemplateImage: propTypes.string,
            template: propTypes.number,
            templateId: propTypes.number,
            templateImage: propTypes.string,
            templateToPreview: propTypes.string,
            text_font_size: propTypes.number,
            thumbnailImages: propTypes.array
        }),
        hideModal: propTypes.func,
        location: propTypes.shape({
            hash: propTypes.string,
            pathname: propTypes.string,
            search: propTypes.string,
            state: undefined
        }),
    }
    
    constructor(props) {
        super(props);
        this.state = {
            'checked': 'product1',
            'resumeDownloadCount': -1,
            'freeDownloadButtonDisable': false,
        }
        
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.showEnlargedTemplate = this.showEnlargedTemplate.bind(this);
        this.changeTemplate = this.changeTemplate.bind(this);
        this.freeResumeRequest = this.freeResumeRequest.bind(this);
        this.pollingUserInfo = this.pollingUserInfo.bind(this);
        this.downloadRequestedResume = this.downloadRequestedResume.bind(this);
        this.timerFunction = this.timerFunction.bind(this);
    }
    
    async showEnlargedTemplate(templateId) {
        await this.props.fetchSelectedTemplateImage(templateId, true);
        this.props.showModal()
    }
    
    changeTemplate() {
        const { eventClicked, showSelectTemplateModal } = this.props
        showSelectTemplateModal()
        eventClicked({
            'action': 'ChangeTemplate',
            'label': 'PaymentPage'
        })
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
        const { requestFreeResume, showGenerateResumeModal,
            userInfo: { resume_creation_count }, } = this.props
            this.setState({ 'resumeDownloadCount': resume_creation_count, 'freeDownloadButtonDisable': true }, async () => {
                await requestFreeResume()
                showGenerateResumeModal()
                this.pollingUserInfo()
            })
        }
        
        timerFunction() {
            const { fetchUserInfo, hideGenerateResumeModal } = this.props
            const { timerId, pollingStartTIme } = this.state
            if (new Date().getTime() - pollingStartTIme > 30000) {  // max limit 10*3 seconds
                clearInterval(timerId)
                hideGenerateResumeModal()
                this.setState({ 'freeDownloadButtonDisable': false })
                Toast.fire({
                    type: 'error',
                    title: 'Something Went Wrong'
                });
            }
            fetchUserInfo(true);
        }
        
        pollingUserInfo() {
            const timer = setInterval(this.timerFunction, 2000);
            const startTime = new Date().getTime();
            this.setState({ 'timerId': timer, 'pollingStartTIme': startTime })
        }
        
        async redirectToCart(checkedProduct) {
            this.props.eventClicked({
                'action': 'PayNow',
                'label': 'Click'
            })
            
            if (!this.props.productIds[0]) return;
            let product;
            this.props.showLoader();
            
            if (checkedProduct === 'product1') {
                product = this.props.productIds[0]
            } else {
                product = this.props.productIds[1]
            }
            const data = {
                "prod_id": product.id,
                "cart_type": 'cart',
            }
            await this.props.addToCart(data);
            window.location.href = `${siteDomain}/cart/payment-summary/`;
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
            
            if (!localStorage.getItem('candidateId')) {
                await loginCandidate()
            }
            
            // get userInfo from LocalStorage
            if (localStorage.getItem('email')) window['email'] = localStorage.getItem('email')
            else window['email'] = ''
            if (localStorage.getItem('mobile')) window['mobile'] = localStorage.getItem('mobile')
            else window['mobile'] = ''
            if (localStorage.getItem('name')) window['name'] = localStorage.getItem('name')
            else window['name'] = ''
            
            // this.props.fetchThumbNailImages();
            this.props.fetchSelectedTemplateImage(localStorage.getItem('selected_template') || 1);
            this.props.getProductIds();
            this.props.fetchUserInfo();
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
        
        static getActions() {
            return [getComponentTitle]
        }
        
        static async fetching({ dispatch }, params) {
            let actionList = Buy.getActions();
            const results = [];
            for (const [index, value] of actionList.entries()) {
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
            const settings = {
                infinite: true,
                speed: 500,
                slidesToShow: 3,
                slidesToScroll: 1,
            };
            const { userInfo: { first_name, last_name, number, email, selected_template,
                order_data, resume_creation_count, free_resume_downloads, resume_generated },
                ui: { loader, modal }, template: { templateImage, thumbnailImages, templateId, modalTemplateImage },
                productIds, eventClicked, hideModal } = this.props;
                const { userInfo } = this.props;
                const { checked, freeDownloadButtonDisable } = this.state;
                const price1 = productIds[0] ? productIds[0].inr_price : 999, discount1 = productIds[0] ? productIds[0].discount : 50,
                heading1 = productIds[0] ? productIds[0].heading : "14-DAYS PLAN",
                fakePrice1 = productIds[0] ? productIds[0].fake_inr_price : 99;
                const price2 = productIds[1] ? productIds[1].inr_price : 1248,
                discount2 = productIds[1] ? productIds[1].discount : 50,
                heading2 = productIds[1] ? productIds[1].heading : "YEARLY PLAN",
                fakePrice2 = productIds[1] ? productIds[1].fake_inr_price : 1999;
                
                const free_download_count = free_resume_downloads - resume_creation_count
                
                return (
                    /*
                    * @desc Top Bar component
                    * */
                    <div>
                    <Header userName={first_name}
                    lastName={last_name}
                    number={number}
                    email={email}
                    location={this.props.location}
                    />
                    <TemplateModal
                    hideModal={hideModal}
                    templateId={templateId}
                    modalTemplateImage={modalTemplateImage}
                    modal={modal}
                    page={'buy'} />
                    <SelectTemplateModal
                    {...this.props}
                    page={"buy"} />
                    {
                        !!(loader) &&
                        <LoaderPage />
                    }
                    <div className="page-container">
                    <TopBar
                    page={'buy'}
                    userInfo={{ selected_template, order_data, resume_generated }}
                    />
                    <section className={'flex-container mt-30'}>
                    
                    <section className="left-sidebar half-width pos-rel">
                    <span onClick={() => this.showEnlargedTemplate(selected_template)} className="zoom" />
                    <div className="right-sidebar-scroll-main">
                    {
                        !!(templateImage) ?
                        <img
                        src={`data:image/png;base64,${templateImage}`}
                        className="img-responsive" alt="" />
                        :
                        <img
                        src={`${this.staticUrl}react/assets/images/resume${selected_template || localStorage.getItem(('selected_template')) || 1}_preview.jpg`}
                        className="img-responsive" alt="" />
                    }
                    
                    </div>
                    
                    </section>
                    
                    <section className="right-sidebar right-sidebar-scroll-main">
                    <div className="choose-plan">
                    <h2 className="mt-10">Choose your plan</h2>
                    {/* <span
                    className="choose-plan-txt">Use resume builder for 12 months to<strong> create/edit</strong> unlimited resume.</span> */}
                    {free_resume_downloads ?
                        <ul>
                        <li className="bdr pos-rel free-trial">
                        <div>
                        <span className="free-trial--ribbon">
                        <span>TRIAL OFFER</span>
                        </span>
                        <span className="free-trial--text">
                        <p>
                        {free_download_count > 0
                            ? ` ${free_download_count} free download for 1st time users.`
                            : "You have exhausted the limit. Please buy resume builder with unlimited downloads to keep using resume builder for an year"}
                            </p>
                            </span>
                            {free_download_count > 0 ?
                                <span className="free-trial--download-button">
                                <button onClick={this.freeResumeRequest} disabled={freeDownloadButtonDisable}>Download</button>
                                </span> : ''
                            }
                            </div>
                            </li>
                            </ul> : ''
                        }
                        <ul>
                        <li>
                        <div className="flex-container">
                        {/* <span className="choose-plann--child">
                        <input type="radio" name="product1"
                        checked={this.state.checked === 'product1' ? true : false}
                        onChange={this.handleOnChange.bind(this, 'product1')} />
                    </span> */}
                    <span className="choose-plan--price">
                    <p>{heading1}</p>
                    Rs. <strong>{price1}/-</strong>
                    <strike className="ml-10">Rs. {fakePrice1}</strike>
                    <span className="choose-plan--off mt-10 db">Save up to {discount1}%</span>
                    </span>
                    <button
                    className="choose-plan--btn-rt orange-button ml-auto"
                    onClick={this.redirectToCart.bind(this, 'product1')}>Pay now
                    </button>
                    </div>
                    </li>
                    <li className="bdr pos-rel">
                    <div className="flex-container">
                    <span className="choose-plan--ribbon">Recommended</span>
                    {/* <span className="choose-plann--child">
                    <input type="radio" name="product2"
                    checked={this.state.checked === 'product2' ? true : false}
                    onChange={this.handleOnChange.bind(this, 'product2')} />
                </span> */}
                <span className="choose-plan--price">
                <p>{heading2}</p>
                <span>Rs.</span> <strong>  {price2}
                /-</strong>
                <strike className="ml-10">Rs. {fakePrice2}</strike>
                <span className="choose-plan--off mt-10 db">Save up to {discount2}%</span>
                </span>
                <button
                className="choose-plan--btn-rt orange-button ml-auto mt-20"
                onClick={this.redirectToCart.bind(this, 'product2')}>Pay now
                </button>
                </div>
                </li>
                <li className="bdr">
                <ul className="choose-plan--planlist">
                <li>Unlimited Downloads</li>
                <li>100% access to all features</li>
                <li>All Resume Templates</li>
                <li>Auto-upgrade of new features</li>
                </ul>
                </li>
                
                {/* <li className="bdr pos-rel">
                <Slider {...settings}>
                
                {
                    [1, 2, 3, 4, 5].map((el, key) => (
                        <div className="carousel-box--slide__content" key={key}>
                        <div onClick={() => this.showEnlargedTemplate(el)}
                        className="triangle-topright">
                        <span></span>
                        </div>
                        {
                            !!(thumbnailImages && thumbnailImages.length) ?
                            <img
                            src={`data:image/png;base64,${thumbnailImages[key]}`}
                            className="img-responsive" alt="" />
                            // <img
                            //     src={`${this.staticUrl}react/assets/images/resume-thumb-${selected_template || el}.jpg`}
                            //     className="img-responsive" alt=""/>
                            :
                            <img
                            src={`${this.staticUrl}react/assets/images/resume-thumb-${selected_template || el}.jpg`}
                            className="img-responsive" alt="" />
                        }
                        </div>
                        ))
                    }
                    </Slider>
                </li> */}
                </ul>
                {/* <div className="">
                <div className="choose-plan--pay-price">
                You pay
                <span>Rs. <strong>{checked === 'product1' ? price1 : price2}/-</strong></span>
                </div>
                <button
                className="choose-plan--orange-button-change orange-button items-right pull-right mt-10"
                onClick={this.redirectToCart.bind(this)}>Pay now
                </button>
            </div> */}
            </div>
            </section>
            
            </section>
            
            <div className="bottom-links">
            {
                <React.Fragment>
                <a onClick={this.changeTemplate}>Change template</a> |
                </React.Fragment>
            }
            <Link to={'/resume-builder/edit'}
            onClick={() => {
                eventClicked({
                    'action': 'EditTemplate',
                    'label': 'Click'
                })
            }}>Edit template</Link>
            </div>
            </div>
            <Footer />
            
            </div>
            )
        }
        
    }
    
    const mapStateToProps = (state) => {
        return {
            productIds: state.productIds,
            ui: state.ui,
            userInfo: state.personalInfo,
            template: state.template
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
            'addToCart': (data) => {
                return new Promise((resolve, reject) => {
                    dispatch(action.addToCart({ data, resolve, reject }));
                })
            },
            'showModal': () => {
                return dispatch(showModal())
            },
            'hideModal': () => {
                return dispatch(hideModal())
            },
            'showGenerateResumeModal': () => {
                return dispatch(showGenerateResumeModal())
            },
            'hideGenerateResumeModal': () => {
                return dispatch(hideGenerateResumeModal())
            },
            'showSelectTemplateModal': () => {
                return dispatch(showSelectTemplateModal())
            },
            'hideSelectTemplateModal': () => {
                return dispatch(hideSelectTemplateModal())
            },
            "updateSelectedTemplate": (personalDetails) => {
                const { gender, date_of_birth, extracurricular } = personalDetails;
                personalDetails = {
                    ...personalDetails,
                    ...{
                        'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                        'gender': (gender && gender['value']) || '',
                        'extracurricular': extracurricular instanceof Array ?
                        (extracurricular || []).map(el => el.value).join(',') : extracurricular
                    }
                }
                return new Promise((resolve, reject) => {
                    dispatch(updatePersonalInfo({ personalDetails, resolve, reject }));
                })
            },
            'displaySelectedTemplate': (templateId) => {
                return dispatch(displaySelectedTemplate(templateId))
            },
            'fetchThumbNailImages': () => {
                return dispatch(fetchThumbNailImages())
            },
            'fetchSelectedTemplateImage': (templateId, isModal) => {
                
                return new Promise((resolve, reject) => {
                    return dispatch(fetchSelectedTemplateImage({ templateId, isModal, resolve, reject }))
                })
            },
            "fetchDefaultCustomization": (templateId) => {
                return new Promise((resolve, reject) => {
                    return dispatch(fetchDefaultCustomization({ templateId, resolve, reject }))
                })
            },
            'eventClicked': (data) => {
                return dispatch(eventClicked(data))
            },
            
            "loginCandidate": (token = '') => {
                return new Promise((resolve, reject) => {
                    dispatch(loginCandidate({ info: { alt: '' }, resolve, reject, isTokenAvail: false }))
                })
            },
            "requestFreeResume": () => {
                return new Promise((resolve, reject) => {
                    dispatch(action.requestFreeResume({ resolve, reject }))
                })
            },
            "showLoader": () => {
                return dispatch(updateUi({ loader: true }))
            }
        }
    };
    
    export default connect(mapStateToProps, mapDispatchToProps)(Buy);