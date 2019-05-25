import React, {Component} from 'react';
import './buy.scss';
import {Link} from 'react-router-dom';
import TopBar from '../../Editor/TopBar/topBar.jsx'
import Header from '../../../Common/Header/header.jsx'
import Footer from '../../../Common/Footer/footer.jsx'
import * as action from '../../../../store/buy/actions'
import {showModal, hideModal, showSelectTemplateModal, hideSelectTemplateModal} from "../../../../store/ui/actions"
import {connect} from "react-redux";
import {siteDomain} from "../../../../Utils/domains";
import TemplateModal from '../../../Modal/tempateModal'
import Slider from "react-slick";
import moment from "moment"
import {fetchPersonalInfo, updatePersonalInfo} from '../../../../store/personalInfo/actions/index'
import SelectTemplateModal from '../../../Modal/selectTemplateModal';
import LoaderPage from '../../../Loader/loaderPage';
import {
    displaySelectedTemplate,
    fetchTemplateImages,
    fetchSelectedTemplateImage,
    fetchThumbNailImages
} from "../../../../store/template/actions";


function SampleNextArrow(props) {
    const {className, style, onClick} = props;
    return (
        <div
            className={className}
            style={{...style, display: "block", background: "red"}}
            onClick={onClick}
        />
    );
}

function SamplePrevArrow(props) {
    const {className, style, onClick} = props;
    return (
        <div
            className={className}
            style={{...style, display: "block", background: "green"}}
            onClick={onClick}
        />
    );
}

export class Buy extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'checked': 'product1'
        }
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.showEnlargedTemplate = this.showEnlargedTemplate.bind(this)
    }

    showEnlargedTemplate(templateId) {
        this.props.displaySelectedTemplate(templateId);
        this.props.showModal()
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
        this.props.fetchThumbNailImages();
        this.props.fetchTemplateImages();
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


    render() {
        const settings = {
            infinite: false,
            speed: 500,
            slidesToShow: 3,
            slidesToScroll: 3,
            variableWidth: true
        };
        const {userInfo: {first_name, selected_template}, ui: {loader}, template: {templateImages, thumbnailImages}} = this.props;
        const {userInfo} = this.props;
        const {checked} = this.state;
        console.log('--template imag---', templateImages, thumbnailImages, selected_template);
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
                <Header userName={first_name}/>
                <TemplateModal {...this.props} />
                <SelectTemplateModal {...this.props}/>
                {
                    !!(loader) &&
                    <LoaderPage/>
                }
                <div className="page-container">
                    <TopBar page={'buy'} userInfo={userInfo}/>
                    <section className={'flex-container mt-30'}>

                        <section className="left-sidebar half-width pos-rel">
                            <span onClick={() => this.showEnlargedTemplate(selected_template)} className="zoom"/>
                            <div className="right-sidebar-scroll-main">
                                {
                                    !!(thumbnailImages && thumbnailImages.length) ?
                                        <img
                                            src={`data:image/png;base64,${templateImages[selected_template - 1]}`}
                                            className="img-responsive" alt=""/>
                                        :
                                        <img
                                            src={`${this.staticUrl}react/assets/images/resume${selected_template || localStorage.getItem(('selected_template')) || 1}_preview.jpg`}
                                            className="img-responsive" alt=""/>
                                }

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
                                                                    className="img-responsive" alt=""/> :
                                                                <img
                                                                    src={`${this.staticUrl}react/assets/images/resume-thumb-${selected_template || el}.jpg`}
                                                                    className="img-responsive" alt=""/>
                                                        }
                                                    </div>
                                                ))
                                            }
                                        </Slider>
                                    </li>
                                </ul>
                                <div className="">
                                    <div className="choose-plan--pay-price">
                                        You pay
                                        <span>Rs. <strong>{checked === 'product1' ? "999" : "1249"}/-</strong></span>
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
                        <a onClick={() => {
                            this.props.showSelectTemplateModal()
                        }}>Change template</a> | <Link to={'/resume-builder/edit'}>Edit template</Link>
                    </div>
                </div>
                <Footer/>

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
        'fetchUserInfo': () => {
            return dispatch(fetchPersonalInfo())
        },
        'getProductIds': () => {
            return dispatch(action.getProductIds())
        },
        'addToCart': (data) => {
            return new Promise((resolve, reject) => {
                dispatch(action.addToCart({data, resolve, reject}));
            })
        },
        'showModal': () => {
            return dispatch(showModal())
        },
        'hideModal': () => {
            return dispatch(hideModal())
        },
        'showSelectTemplateModal': () => {
            return dispatch(showSelectTemplateModal())
        },
        'hideSelectTemplateModal': () => {
            return dispatch(hideSelectTemplateModal())
        },
        "updateSelectedTemplate": (personalDetails) => {
            const {gender, date_of_birth, extracurricular} = personalDetails;
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
                dispatch(updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        displaySelectedTemplate(templateId) {
            return dispatch(displaySelectedTemplate(templateId))
        },
        fetchTemplateImages() {
            return dispatch(fetchTemplateImages())
        },
        fetchThumbNailImages() {
            return dispatch(fetchThumbNailImages())
        },
        fetchSelectedTemplateImage(templateId) {
            return dispatch(fetchSelectedTemplateImage(templateId))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Buy);