import React, {Component} from 'react';
import Header from '../../../Common/Header/header.jsx';
import './buy.scss';
import * as action from '../../../../store/buy/actions';
import {fetchThumbNailImages, fetchSelectedTemplateImage} from '../../../../store/template/actions/index'
import {connect} from "react-redux";
import {siteDomain} from "../../../../Utils/domains";
import Slider from "react-slick";
import Loader from '../../../Common/Loader/loader.jsx';
import BuyTemplateModal from '../../../Common/BuyTemplateModal/buyTemplateModal.jsx';
import {eventClicked} from '../../../../store/googleAnalytics/actions/index'
import {loginCandidate} from "../../../../store/landingPage/actions";


class Buy extends Component {

    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.state = {
            'checked': 'product1',
            'pay_button_clicked': false,
            'modal_status': false,
            'template_id': ''
        }
        this.closeModalStatus = this.closeModalStatus.bind(this);
        this.openModal = this.openModal.bind(this);
        this.editTemplate = this.editTemplate.bind(this);
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
        this.props.addToCart(data);
        this.setState({pay_button_clicked: true})
    }

    closeModalStatus() {
        this.setState({modal_status: false})
    }

    async openModal(index) {
        await this.props.fetchSelectedTemplateImage(index + 1)
        this.setState({modal_status: true, template_id: index + 1})
    }

    async componentDidMount() {
        if (!localStorage.getItem('candidateId')) {
            await loginCandidate()
        }
        this.props.getProductIds();
        this.props.fetchThumbNailImages();
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
        const {eventClicked, history} = this.props;
        eventClicked({
            'action': 'EditTemplate',
            'label': 'Click'
        })
        history.push(`/resume-builder/edit/?type=profile`)
    }

    render() {
        const settings = {
            dots: false,
            infinite: true,
            speed: 500,
            slidesToShow: 2,
        };
        const {ui: {mainloader}, template: {thumbnailImages, templateImage}, productIds, history} = this.props
        const template = localStorage.getItem('selected_template') || 1;
        const {checked, pay_button_clicked, modal_status} = this.state
        const price1 = productIds[0] ? productIds[0].inr_price : 999
        const discount1 = Math.floor(((1499 - price1) / 1499) * 100)
        const price2 = productIds[1] ? productIds[1].inr_price : 1248
        const discount2 = Math.floor(((1999 - price2) / 1999) * 100)
        return (

            <div className="buy-container">
                <Header page={"buy"} history={history}/>
                {mainloader ? <Loader/> : ""}
                {modal_status ? <BuyTemplateModal modal_status={modal_status}
                                                  closeModalStatus={this.closeModalStatus}
                                                  templateImage={templateImage}/> : ''}

                <div className="pay-now">
                    <div className="pay-now__price">
                        <span className="fs-12 pay-now__price--pay">You pay</span>
                        <span
                            className="fs-26 color-333 semi-bold">Rs. {checked === 'product1' ? price1 : price2}/-</span>
                    </div>

                    <button className="btn btn__round btn__primary fs-" disabled={pay_button_clicked}
                            onClick={this.redirectToCart.bind(this)}>Pay Now
                    </button>
                </div>


                <div className="buy">
                    <p className="buy--create">Use resume builder for 12 months
                        to<strong> create/edit</strong> unlimited resume.</p>
                    <div className="buy__wrap mt-15">
                        <div className="buy__item">
                            <div className="buy__item--left">
                                <input className="buy__item--input form__radio-input" type="radio" id="your-resume"
                                       name="product-1"
                                       checked={checked === 'product1' ? true : false}
                                       onChange={this.handleOnChange.bind(this, 'product1')}></input>
                                <label className="buy__item--label form__radio-label" htmlFor="your-resume">
                                    <span className="form__radio-button"></span>
                                    Buy your <br/>customised resume<br/>
                                    <strong>Rs. {price1}/-</strong>
                                    <span className="fs-14 line-through">Rs. 1499 </span>
                                    <span className="fs-14 bold">Flat {discount1}% off</span>
                                </label>
                            </div>
                            <div className="buy__item--right">
                                <span className="buy__item--image">
                                    {thumbnailImages.length === 5 ?
                                        <img src={`data:image/png;base64, ${thumbnailImages[template - 1]}`}
                                             alt="Resume"/> :
                                        <img
                                            src={`${this.staticUrl}react/assets/images/mobile/small-resume-${template}.jpg`}
                                            alt="Custom resume"/>
                                    }
                                </span>
                                <a className="fs-12 mt-5" onClick={this.editTemplate}>Edit</a>
                            </div>
                        </div>

                        <div className="buy__item buy__recommended">
                            <div className="buy__recommended--tag">Recommended</div>
                            <div className="buy__item--left form__radio-group">
                                <input className="buy__item--input form__radio-input" type="radio" id="all-resumes"
                                       name="product2"
                                       checked={checked === 'product2' ? true : false}
                                       onChange={this.handleOnChange.bind(this, 'product2')}></input>
                                <label className="buy__item--label form__radio-label" htmlFor="all-resumes">
                                    <span className="form__radio-button"></span>
                                    Buy all 5 customised resumes
                                    <div className="buy__item--price">
                                        <span className="fs-22 color-333 semi-bold">Rs. {price2}/-</span>
                                        <span className="fs-14 line-through">Rs. 1999</span>
                                        <span className="fs-14 bold">Flat {discount2}% off</span>
                                    </div>
                                </label>
                            </div>

                            <div className="buy__item--right">
                                <div className="buy__item--right__sliderWrap">
                                    <Slider {...settings}>
                                        {thumbnailImages.length === 5 ?
                                            thumbnailImages.map((el, index) => {
                                                return (
                                                    <div className="buy__recommended__item" key={index}>
                                                    <span className="buy__recommended__image">
                                                        <span className="sprite icon--zoom"
                                                              onClick={() => {
                                                                  this.openModal(index)
                                                              }}></span>
                                                        <img src={`data:image/png;base64, ${el}`} alt="Custom resume"/>
                                                    </span>
                                                    </div>
                                                )
                                            }) :
                                            [1, 2, 3, 4, 5].map((el, index) => {
                                                return (
                                                    <div className="buy__recommended__item" key={index}>
                                                    <span className="buy__recommended__image">
                                                        <img
                                                            src={`${this.staticUrl}react/assets/images/mobile/resumebig-${el}.jpg`}
                                                            alt="Custom resume"/>
                                                    </span>
                                                    </div>
                                                )

                                            })
                                        }
                                    </Slider>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>


            </div>

        )
    }
}

const mapStateToProps = (state) => {
    return {
        productIds: state.productIds,
        ui: state.ui,
        template: state.template
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        'getProductIds': () => {
            return dispatch(action.getProductIds())
        },
        'fetchThumbNailImages': () => {
            return dispatch(fetchThumbNailImages())
        },
        'fetchSelectedTemplateImage': (template_id) => {
            return new Promise((resolve, reject) => {
                return dispatch(fetchSelectedTemplateImage({template_id, resolve, reject}))
            })
        },
        'addToCart': (data) => {
            return new Promise((resolve, reject) => {
                dispatch(action.addToCart({data, resolve, reject}));
            })
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        },
        "loginCandidate": (token) => {
            return new Promise((resolve, reject) => {
                dispatch(loginCandidate({payload: {alt: token}, resolve, reject, isTokenAvail: false}))
            })
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Buy);