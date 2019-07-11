import React, {Component} from 'react';
import './downloadResume.scss'
import TopBar from '../../Editor/TopBar/topBar.jsx'
import Header from '../../../Common/Header/header.jsx'
import Footer from '../../../Common/Footer/footer.jsx'

export default class DownloadResume extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
    }

    render() {
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
                <Header/>
                <div className="page-container">
                    <TopBar page={'download'}/>
                    <section className={'flex-container mt-30'}>
                        <section className="right-sidebar right-sidebar-scroll-main ml0">
                            <div className="order-complete">
                                <ul className="pt-20">
                                    <li>
                                        <p>Hello Amit,</p>
                                        <span className="mt-30">Your customized resume is ready for download.  </span>
                                        <strong className="mt-10">An order confirmation has been sent
                                            to <b>amit.kumar@gmail.com</b></strong>
                                    </li>
                                    <li>
                                        <div className="carousel-box">
                                            <ul className="carousel-box--carousel">
                                                <li className="carousel-box--slide">
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume1.jpg`}
                                                             className="img-responsive" alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume2.jpg`}
                                                             className="img-responsive" alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume3.jpg`}
                                                             className="img-responsive" alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume4.jpg`}
                                                             className="img-responsive" alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume5.jpg`}
                                                             className="img-responsive" alt=""/>
                                                    </div>
                                                    <div className="carousel-box--slide__content">
                                                        <img src={`${this.staticUrl}react/assets/images/resume2.jpg`}
                                                             className="img-responsive" alt=""/>
                                                    </div>
                                                </li>
                                            </ul>
                                        </div>
                                    </li>
                                    <li>
                    					<span className="mt-20">
                    						Download now and start applying for jobs! 
	                    				</span>
                                        <button
                                            className="order-complete--orange-button-change orange-button mt-20 mb-20">Download
                                        </button>
                                    </li>
                                </ul>
                                <div className="links">
                                    To download your resume anytime later, just visit My Orders on <a
                                    href="#"> ShineLearning.com</a>.
                                </div>
                            </div>
                        </section>

                    </section>

                </div>
                <Footer/>

            </div>
        )
    }

}

