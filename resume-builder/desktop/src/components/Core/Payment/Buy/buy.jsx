import React, {Component} from 'react';
import './buy.scss'
import TopBar from '../../Editor/TopBar/topBar.jsx'
import Header from '../../../Common/Header/header.jsx'
import Footer from '../../../Common/Footer/footer.jsx'
import * as action from '../../../../store/buy/actions'
import {connect} from "react-redux";
import {siteDomain} from "../../../../Utils/domains";

export class Buy extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'checked': 'product1'
        }
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'


    }

    componentWillMount() {
        if (!localStorage.getItem('token')) {
            window.location.href = `${siteDomain}/login/?next=/resume-builder/`;
            return;
        }
    }

    async redirectToCart() {

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
        await this.props.addToCart(data);
        window.location.href = '/cart'
    }

    componentDidMount() {
        this.props.getProductIds();

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
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
                <Header/>
                <div className="page-container">
                    <TopBar page={'buy'}/>
                    <section className={'flex-container mt-30'}>

                        <section className="left-sidebar half-width pos-rel">
                            <span className="zoom"></span>
                            <div className="right-sidebar-scroll-main">
                            <img src={`${this.staticUrl}react/assets/images/resume1_Preview.jpg`} className="img-responsive" alt=""/>
                            </div>

                        </section>

                        <section className="right-sidebar right-sidebar-scroll-main">
                            <div className="choose-plan">
                                <h2 className="mt-10">Choose your plan</h2>
                                <ul>
                                    <li>
                                        <div className="flex-container">
	                    					<span className="choose-plann--child">
	                    						<input type="radio" name="product1"
                                                       checked={this.state.checked === 'product1' ? true : false}
                                                       onChange={this.handleOnChange.bind(this, 'product1')}/>
	                    					</span>
                                            <span className="choose-plan--price">
	                    						<p>Buy your customised resume</p>
	                    						Rs. <strong>999/-</strong>
	                    					</span>
                                        </div>
                                    </li>
                                    <li className="bdr pos-rel">
                                        <div className="flex-container">
                                            <span className="choose-plan--ribbon">Recommended</span>
                                            <span className="choose-plann--child">
	                    						<input type="radio" name="product2"
                                                       checked={this.state.checked === 'product2' ? true : false}
                                                       onChange={this.handleOnChange.bind(this, 'product2')}/>
	                    					</span>
                                            <span className="choose-plan--price">
	                    						<p>Buy all 6 customised resumes</p>
	                    						Rs. <strong>1249/-</strong>
	                    						<strike className="ml-10">Rs. 3499</strike>
	                    						<span className="choose-plan--off ml-10">63% off</span>
	                    					</span>
                                        </div>
                                        <div className="carousel-box">
                                            <ul className="carousel-box--carousel">
                                                <li className="carousel-box--slide">
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume1.jpg`}
                                                             className="img-responsive"
                                                             alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume2.jpg`}
                                                             className="img-responsive"
                                                             alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume3.jpg`}
                                                             className="img-responsive"
                                                             alt=""/>
                                                    </div>
                                                </li>
                                            </ul>
                                            <span className="carousel-box--right"></span>
                                        </div>
                                    </li>
                                </ul>
                                <div className="">
                                    <div className="choose-plan--pay-price">
                                        You pay
                                        <span>Rs. <strong>999/-</strong></span>
                                    </div>
                                    <button
                                        className="choose-plan--orange-button-change orange-button items-right pull-right mt-10"
                                        onClick={this.redirectToCart.bind(this)}>Pay now
                                    </button>
                                </div>
                            </div>
                        </section>

                    </section>

                    <div className="bottom-links">
                        <a href="#">Change template</a> | <a href="#">Edit template</a>
                    </div>
                </div>
                <Footer/>

            </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {productIds: state.productIds}
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