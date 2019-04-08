import React, {Component} from 'react';
import './buy.scss'
import TopBar from '../../Editor/TopBar/topBar.jsx'
import Header from '../../../Common/Header/header.jsx'
import Footer from '../../../Common/Footer/footer.jsx'
import * as action from '../../../../store/buy/actions'
import {connect} from "react-redux";

export class Buy extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'checked': 'product1'
        }

    }

    async redirectToCart() {
        
        if(!this.props.productIds[0])
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
        console.log(this.props.productIds[0])

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
                            <div className="right-sidebar-scroll-main" dangerouslySetInnerHTML={{
                                __html: "<!doctype html>\n" +
                                    "<html lang=\"en\">\n" +
                                    "  <head>\n" +
                                    "    <!-- Required meta tags -->\n" +
                                    "    <meta charset=\"utf-8\">\n" +
                                    "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">\n" +
                                    "    <title>Resume</title>\n" +
                                    "  </head>\n" +
                                    "  <body style=\"margin: 0; padding: 0; font-family: 'Segoe UI', 'Helvetica Neue', 'Roboto', Arial, 'sans-serif';\">\n" +
                                    "    <div style=\"max-width: 1536px; width: 100%; font-family: 'Segoe UI', 'Helvetica Neue', 'Roboto', Arial, 'sans-serif'; font-size: 14px; color: #777777; line-height: 18px;\">\n" +
                                    "\n" +
                                    "      <div style=\"width: 100%; background: #d34d4d; padding: 3%;\">\n" +
                                    "\n" +
                                    "        <!--top left-->\n" +
                                    "        <div style=\"width: 45%; margin-right: 5%; display: inline-block; vertical-align: top;\">\n" +
                                    "          <h1 style=\"margin: 0; color: #ffffff; font-size: 32px;\">Your Name</h1>\n" +
                                    "          <strong style=\"display: block; font-size: 16px; color: #ffd7d7; font-weight: normal; margin-bottom: 20px;\">IT Project Manager</strong>\n" +
                                    "          <span style=\"float: left; margin-right: 15px;\"><img style=\"width: 150px; height: 150px; border-radius: 100%;\" src=\"images/resume-pic.png\" alt=\"Resume\"></span>\n" +
                                    "          <p style=\"color: #ffffff\">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis ipsum suspend isse ultrices gravida. Risus commodo viverra maecenas accumsan lacus vel facilisis.</p>\n" +
                                    "          <p style=\"color: #ffffff\">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>\n" +
                                    "        </div>\n" +
                                    "\n" +
                                    "        <!--top right-->\n" +
                                    "        <div style=\"width: 49%; display: inline-block; vertical-align: top;\">\n" +
                                    "          <ul style=\"margin: 20px 0 0 0; padding: 0; font-size: 14px; color: #ffffff; list-style-type: none;\">\n" +
                                    "            <li style=\"display: table; margin-bottom: 15px;\"><span style=\"display: table-cell; padding-right: 10px; vertical-align: middle;\"><img src=\"images/mobile-icon.png\" alt=\"Mobile\"></span>+91 9876512345</li>\n" +
                                    "            <li style=\"display: table; margin-bottom: 15px;\"><span style=\"display: table-cell; padding-right: 10px; vertical-align: middle;\"><img src=\"images/email-icon.png\" alt=\"Email\"></span>youremailid@gmail.com</li>\n" +
                                    "            <li style=\"display: table; margin-bottom: 15px;\"><span style=\"display: table-cell; padding-right: 10px; vertical-align: middle;\"><img src=\"images/location-icon.png\" alt=\"Location\"></span>BPTP Park Centra, 7th Floor Tower A Jal Vayu Vihar, Sector 30, Gurugram, Haryana 122003</li>\n" +
                                    "            <li style=\"display: table; margin-bottom: 15px;\"><span style=\"display: table-cell; padding-right: 10px; vertical-align: middle;\"><img src=\"images/linkedin-icon.png\" alt=\"Linkedin\"></span>linkedin.com/candidatename</li>\n" +
                                    "            <li style=\"display: table; margin-bottom: 15px;\"><span style=\"display: table-cell; padding-right: 10px; vertical-align: middle;\"><img src=\"images/facebook-icon.png\" alt=\"Facebook\"></span>Facebook.com/candidatename</li>\n" +
                                    "          </ul>\n" +
                                    "        </div>\n" +
                                    "\n" +
                                    "      </div>\n" +
                                    "\n" +
                                    "      <div style=\"width: 100%; border-bottom: 13px solid #d34d4d; padding: 3%;\">\n" +
                                    "\n" +
                                    "        <!--Experience-->\n" +
                                    "        <div style=\"vertical-align: top; font-size: 13px; color: #999999;\">\n" +
                                    "          <strong style=\"background: #333333; padding: 10px; display: block; text-transform: uppercase; color: #ffffff; font-weight: normal; font-size: 16px;\">Experience</strong>\n" +
                                    "          <ul style=\"padding: 10px; margin: 0; list-style-type: none;\">\n" +
                                    "            <li style=\"vertical-align: top; margin: 10px 0;\">\n" +
                                    "              <span style=\"width: 9px; height: 9px; border-radius: 100%; background: #d34d4d; display: inline-block; margin-right: 10px; vertical-align: baseline;\"></span> \n" +
                                    "              <span style=\"font-style: italic; color: #333333; width: 20%; display: inline-block; vertical-align: top;\">(Oct 2016 - Current)</span> \n" +
                                    "              <span style=\"display: inline-block; width: 75%; vertical-align: top;\">\n" +
                                    "                <strong style=\"display: block; font-size: 16px; color: #333333;\">IT Project Manager</strong>\n" +
                                    "                Infocom Network Pvt. Ltd\n" +
                                    "                <p style=\"font-size: 14px; color: #777777; margin-top: 5px;\">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis ipsum suspendisse ultrices gravida. Lorem ipsum dolor sit amet, consectetur adipiscing elit,</p>\n" +
                                    "              </span>\n" +
                                    "            </li>\n" +
                                    "            <li style=\"vertical-align: top; margin: 10px 0;\">\n" +
                                    "              <span style=\"width: 9px; height: 9px; border-radius: 100%; background: #d34d4d; display: inline-block; margin-right: 10px; vertical-align: baseline;\"></span> \n" +
                                    "              <span style=\"font-style: italic; color: #333333; width: 20%; display: inline-block; vertical-align: top;\">(Oct 2016 - Current)</span> \n" +
                                    "              <span style=\"display: inline-block; width: 75%; vertical-align: top;\">\n" +
                                    "                <strong style=\"display: block; font-size: 16px; color: #333333;\">IT Project Manager</strong>\n" +
                                    "                Infocom Network Pvt. Ltd\n" +
                                    "                <p style=\"font-size: 14px; color: #777777; margin-top: 5px;\">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis ipsum suspendisse ultrices gravida. Lorem ipsum dolor sit amet, consectetur adipiscing elit,</p>\n" +
                                    "              </span>\n" +
                                    "            </li>\n" +
                                    "            <li style=\"vertical-align: top; margin: 10px 0;\">\n" +
                                    "              <span style=\"width: 9px; height: 9px; border-radius: 100%; background: #d34d4d; display: inline-block; margin-right: 10px; vertical-align: baseline;\"></span> \n" +
                                    "              <span style=\"font-style: italic; color: #333333; width: 20%; display: inline-block; vertical-align: top;\">(Oct 2016 - Current)</span> \n" +
                                    "              <span style=\"display: inline-block; width: 75%; vertical-align: top;\">\n" +
                                    "                <strong style=\"display: block; font-size: 16px; color: #333333;\">IT Project Manager</strong>\n" +
                                    "                Infocom Network Pvt. Ltd\n" +
                                    "                <p style=\"font-size: 14px; color: #777777; margin-top: 5px;\">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis ipsum suspendisse ultrices gravida. Lorem ipsum dolor sit amet, consectetur adipiscing elit,</p>\n" +
                                    "              </span>\n" +
                                    "            </li>\n" +
                                    "          </ul>\n" +
                                    "        </div>\n" +
                                    "\n" +
                                    "        <!--Skills-->\n" +
                                    "        <div style=\"vertical-align: top; font-size: 13px; color: #999999;\">\n" +
                                    "          <strong style=\"background: #333333; padding: 10px; display: block; text-transform: uppercase; color: #ffffff; font-weight: normal; font-size: 16px;\">Skills</strong>\n" +
                                    "        </div>\n" +
                                    "\n" +
                                    "        <div style=\"width: 35%; margin-right: 5%; display: inline-block; font-size: 13px; color: #333333; text-align: center;\">\n" +
                                    "          <span style=\"position: relative; display: table; margin: 18% 0 0 30%;\">\n" +
                                    "            <span style=\"width: 155px; height: 155px; border-radius: 100%; background: #d8d8d8; vertical-align: middle; text-align: center; display: table-cell;\">Data enginerring</span>\n" +
                                    "            <span style=\"width: 86px; height: 86px; border-radius: 100%; background: #ef8080; vertical-align: middle; text-align: center; display: table-cell; position: absolute; top: -45px; left: 35px;\">\n" +
                                    "              <b style=\"vertical-align: middle; display: inline-block; margin-top: 35%;\">Dev OPS</b>\n" +
                                    "            </span>\n" +
                                    "            <span style=\"width: 86px; height: 86px; border-radius: 100%; background: #a7c4f4; vertical-align: middle; text-align: center; display: table-cell; position: absolute; top: 40px; right: -70px;\">\n" +
                                    "              <b style=\"vertical-align: middle; display: inline-block; margin-top: 35%;\">Full stack developer</b>\n" +
                                    "            </span>\n" +
                                    "            <span style=\"width: 86px; height: 86px; border-radius: 100%; background: #e2bd58; vertical-align: middle; text-align: center; display: table-cell; position: absolute; bottom: -45px; left: 35px;\">\n" +
                                    "              <b style=\"vertical-align: middle; display: inline-block; margin-top: 35%;\">Machine Learning</b>\n" +
                                    "            </span>\n" +
                                    "            <span style=\"width: 86px; height: 86px; border-radius: 100%; background: #abc881; vertical-align: middle; text-align: center; display: table-cell; position: absolute; top: 40px; left: -70px;\">\n" +
                                    "              <b style=\"vertical-align: middle; display: inline-block; margin-top: 35%;\">OOP</b>\n" +
                                    "            </span>\n" +
                                    "          </span>\n" +
                                    "          \n" +
                                    "        </div>\n" +
                                    "\n" +
                                    "        <div style=\"width: 59%; display: inline-block; position: relative; vertical-align: top;\">\n" +
                                    "          <div style=\"width: 44%; display: inline-block; margin: 30px 0 0 5%;\">\n" +
                                    "            <strong style=\"font-size: 14px; display: block; color: #333333; margin-bottom: 5px;\">Microsoft projects</strong>\n" +
                                    "              <div style=\"background: #e0e0e0; height: 8px; border-radius: 5px; overflow: hidden; width: 88%; position: relative; font-size: 12px; color: #333333;\">\n" +
                                    "                <div role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 40%; background-color: #333333; line-height: 8px; height: 8px;\">\n" +
                                    "                  <span style=\"position: absolute; right: 0; width: 1px; height: 1px; overflow: hidden;\"></span>\n" +
                                    "                </div>\n" +
                                    "              </div>\n" +
                                    "              <span style=\"float: right; display: inline-block; margin-top: -15px; font-size: 12px;\"><b style=\"font-size: 16px; color: #333333;\">4/</b>10</span>\n" +
                                    "          </div>\n" +
                                    "          <div style=\"width: 44%; display: inline-block; margin: 30px 0 0 5%;\">\n" +
                                    "            <strong style=\"font-size: 14px; display: block; color: #333333; margin-bottom: 5px;\">Android Studio</strong>\n" +
                                    "              <div style=\"background: #e0e0e0; height: 8px; border-radius: 5px; overflow: hidden; width: 88%; position: relative; font-size: 12px; color: #333333;\">\n" +
                                    "                <div role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 60%; background-color: #333333; line-height: 8px; height: 8px;\">\n" +
                                    "                  <span style=\"position: absolute; right: 0; width: 1px; height: 1px; overflow: hidden;\"></span>\n" +
                                    "                </div>\n" +
                                    "              </div>\n" +
                                    "              <span style=\"float: right; display: inline-block; margin-top: -15px; font-size: 12px;\"><b style=\"font-size: 16px; color: #333333;\">6/</b>10</span>\n" +
                                    "          </div>\n" +
                                    "          <div style=\"width: 44%; display: inline-block; margin: 30px 0 0 5%;\">\n" +
                                    "            <strong style=\"font-size: 14px; display: block; color: #333333; margin-bottom: 5px;\">MS windows server</strong>\n" +
                                    "              <div style=\"background: #e0e0e0; height: 8px; border-radius: 5px; overflow: hidden; width: 88%; position: relative; font-size: 12px; color: #333333;\">\n" +
                                    "                <div role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 80%; background-color: #333333; line-height: 8px; height: 8px;\">\n" +
                                    "                  <span style=\"position: absolute; right: 0; width: 1px; height: 1px; overflow: hidden;\"></span>\n" +
                                    "                </div>\n" +
                                    "              </div>\n" +
                                    "              <span style=\"float: right; display: inline-block; margin-top: -15px; font-size: 12px;\"><b style=\"font-size: 16px; color: #333333;\">8/</b>10</span>\n" +
                                    "          </div>\n" +
                                    "          <div style=\"width: 44%; display: inline-block; margin: 30px 0 0 5%;\">\n" +
                                    "            <strong style=\"font-size: 14px; display: block; color: #333333; margin-bottom: 5px;\">SQL</strong>\n" +
                                    "              <div style=\"background: #e0e0e0; height: 8px; border-radius: 5px; overflow: hidden; width: 88%; position: relative; font-size: 12px; color: #333333;\">\n" +
                                    "                <div role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 40%; background-color: #333333; line-height: 8px; height: 8px;\">\n" +
                                    "                  <span style=\"position: absolute; right: 0; width: 1px; height: 1px; overflow: hidden;\"></span>\n" +
                                    "                </div>\n" +
                                    "              </div>\n" +
                                    "              <span style=\"float: right; display: inline-block; margin-top: -15px; font-size: 12px;\"><b style=\"font-size: 16px; color: #333333;\">4/</b>10</span>\n" +
                                    "          </div>\n" +
                                    "          <div style=\"width: 44%; display: inline-block; margin: 30px 0 0 5%;\">\n" +
                                    "            <strong style=\"font-size: 14px; display: block; color: #333333; margin-bottom: 5px;\">Linux server</strong>\n" +
                                    "              <div style=\"background: #e0e0e0; height: 8px; border-radius: 5px; overflow: hidden; width: 88%; position: relative; font-size: 12px; color: #333333;\">\n" +
                                    "                <div role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 60%; background-color: #333333; line-height: 8px; height: 8px;\">\n" +
                                    "                  <span style=\"position: absolute; right: 0; width: 1px; height: 1px; overflow: hidden;\"></span>\n" +
                                    "                </div>\n" +
                                    "              </div>\n" +
                                    "              <span style=\"float: right; display: inline-block; margin-top: -15px; font-size: 12px;\"><b style=\"font-size: 16px; color: #333333;\">6/</b>10</span>\n" +
                                    "          </div>\n" +
                                    "          <div style=\"width: 44%; display: inline-block; margin: 30px 0 0 5%;\">\n" +
                                    "            <strong style=\"font-size: 14px; display: block; color: #333333; margin-bottom: 5px;\">Linux server</strong>\n" +
                                    "              <div style=\"background: #e0e0e0; height: 8px; border-radius: 5px; overflow: hidden; width: 88%; position: relative; font-size: 12px; color: #333333;\">\n" +
                                    "                <div role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 60%; background-color: #333333; line-height: 8px; height: 8px;\">\n" +
                                    "                  <span style=\"position: absolute; right: 0; width: 1px; height: 1px; overflow: hidden;\"></span>\n" +
                                    "                </div>\n" +
                                    "              </div>\n" +
                                    "              <span style=\"float: right; display: inline-block; margin-top: -15px; font-size: 12px;\"><b style=\"font-size: 16px; color: #333333;\">6/</b>10</span>\n" +
                                    "          </div>\n" +
                                    "          <div style=\"width: 44%; display: inline-block; margin: 30px 0 0 5%;\">\n" +
                                    "            <strong style=\"font-size: 14px; display: block; color: #333333; margin-bottom: 5px;\">Linux server</strong>\n" +
                                    "              <div style=\"background: #e0e0e0; height: 8px; border-radius: 5px; overflow: hidden; width: 88%; position: relative; font-size: 12px; color: #333333;\">\n" +
                                    "                <div role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 60%; background-color: #333333; line-height: 8px; height: 8px;\">\n" +
                                    "                  <span style=\"position: absolute; right: 0; width: 1px; height: 1px; overflow: hidden;\"></span>\n" +
                                    "                </div>\n" +
                                    "              </div>\n" +
                                    "              <span style=\"float: right; display: inline-block; margin-top: -15px; font-size: 12px;\"><b style=\"font-size: 16px; color: #333333;\">6/</b>10</span>\n" +
                                    "          </div>\n" +
                                    "          <div style=\"width: 44%; display: inline-block; margin: 30px 0 0 5%;\">\n" +
                                    "            <strong style=\"font-size: 14px; display: block; color: #333333; margin-bottom: 5px;\">Java</strong>\n" +
                                    "              <div style=\"background: #e0e0e0; height: 8px; border-radius: 5px; overflow: hidden; width: 88%; position: relative; font-size: 12px; color: #333333;\">\n" +
                                    "                <div role=\"progressbar\" aria-valuenow=\"40\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 90%; background-color: #333333; line-height: 8px; height: 8px;\">\n" +
                                    "                  <span style=\"position: absolute; right: 0; width: 1px; height: 1px; overflow: hidden;\"></span>\n" +
                                    "                </div>\n" +
                                    "              </div>\n" +
                                    "              <span style=\"float: right; display: inline-block; margin-top: -15px; font-size: 12px;\"><b style=\"font-size: 16px; color: #333333;\">9/</b>10</span>\n" +
                                    "          </div>\n" +
                                    "          \n" +
                                    "        </div>\n" +
                                    "        \n" +
                                    "      </div>\n" +
                                    "\n" +
                                    "      \n" +
                                    "\n" +
                                    "\n" +
                                    "    </div>\n" +
                                    "  </body>\n" +
                                    "</html>"
                            }}>
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
                                                        <img src="/images/resume1.jpg" className="img-responsive"
                                                             alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src="/images/resume2.jpg" className="img-responsive"
                                                             alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src="/images/resume3.jpg" className="img-responsive"
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