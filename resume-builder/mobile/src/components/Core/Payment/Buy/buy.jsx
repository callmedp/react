import React, {Component} from 'react';
import Header from '../../../Common/Header/header.jsx';
import './buy.scss';
import * as action from '../../../../store/buy/actions';
import {connect} from "react-redux";
import {siteDomain} from "../../../../Utils/domains";
import Slider from "react-slick";
import Loader from '../../../Common/Loader/loader.jsx';


class Buy extends Component {

    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.state = {
            'checked': 'product1',
            'pay_button_clicked': false
        }
    }


     redirectToCart() {
        // console.log("Here")

        if (!this.props.productIds[0])
            return;
        let product;
        if (this.state.checked === 'product1') {
            product = this.props.productIds[1]
        } else {
            product = this.props.productIds[0]
        }
        const data = {
            "prod_id": product.parent,
            "addons": [],
            "cart_type": 'cart',
            "cv_id": product.id,
            "req_options": [],
            'add_resume': true

        }
        this.props.addToCart(data);
        this.setState({pay_button_clicked:true})
    }

    componentDidMount() {
        this.props.getProductIds();
        ////console.log(this.props.productIds[0])

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

    render() {

        const settings = {
            dots: false,
            infinite: true,
            speed: 500,
            slidesToShow: 2,
          };
          const {loader:{mainloader}} = this.props
          const template = localStorage.getItem('template') || 1;
          const {checked,pay_button_clicked} = this.state
          
        return (

            <div className="buy-container">
                <Header/>
                {mainloader ? <Loader/> :""}

                <div className="pay-now">
                    <div className="pay-now__price">
                        <span className="fs-14 pay-now__price--pay">You pay</span>
                        <span
                            className="fs-26 color-333 semi-bold">Rs. {checked === 'product1' ? 999 : 1249}/-</span>
                    </div>

                    <button className="btn btn__round btn__primary fs-" disabled={pay_button_clicked}
                            onClick={this.redirectToCart.bind(this)}>Pay Now
                    </button>
                </div>

                <div className="buy">
                    <div className="buy__wrap">
                        <div className="buy__item">
                            <div className="buy__item--left form__radio-group">
                                <input className="buy__item--input form__radio-input" type="radio" id="your-resume"
                                       name="product-1"
                                       checked={checked === 'product1' ? true : false}
                                       onChange={this.handleOnChange.bind(this, 'product1')}></input>
                                <label className="buy__item--label form__radio-label" htmlFor="your-resume">
                                    <span className="form__radio-button"></span>
                                    Buy your <br/>customised resume
                                    <strong>Rs. 999/-</strong>
                                </label>
                            </div>
                            <div className="buy__item--right">
                                <span className="buy__item--image">
                                    <img src={`${this.staticUrl}react/assets/images/mobile/Resume4.png`} alt="Resume"/>
                                </span>
                                <a className="fs-12 mt-5" onClick onClick={()=>{this.props.history.push(`/resume-builder/edit/?type=profile`) }}>Edit</a>
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
                                    <Slider {...settings}>
                                        <div className="buy__recommended__item">
                                            <span className="buy__recommended__image">
                                                <span className="sprite icon--zoom"></span>
                                                <img src={`${this.staticUrl}react/assets/images/mobile/resume-2.png`} alt="Custom resume" />
                                            </span>
                                        </div>
                                        
                                        <div className="buy__recommended__item">
                                            <span className="buy__recommended__image">
                                                <span className="sprite icon--zoom"></span>
                                                <img src={`${this.staticUrl}react/assets/images/mobile/resume-1.png`} alt="Custom resume" />
                                            </span>
                                        </div>
                                       
                                        <div className="buy__recommended__item">
                                            <span className="buy__recommended__image">
                                                <span className="sprite icon--zoom"></span>
                                                <img src={`${this.staticUrl}react/assets/images/mobile/resume-2.png`} alt="Custom resume" />
                                            </span>
                                        </div>
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
        loader: state.loader,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        'getProductIds': () => {
            return dispatch(action.getProductIds())
        },
        'addToCart': (data) => {
            return new Promise((resolve, reject) => {
                dispatch(action.addToCart({data, resolve, reject}));
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Buy);