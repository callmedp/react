import React, {Component} from 'react'
import './topBar.scss'

export default class TopBar extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }

    render() {
        const {page} = this.props;

        return (
            <section className="flex-container">
                <div className="top-banner">
                    {
                        page === 'buy' ?
                            <div className="top-banner--banner-txt">
                                <h1>Your customised resume is ready!</h1>
                                <p>Buy more templates and save more </p>
                            </div> :
                            page === 'download' ?
                                <div className="top-banner--banner-txt">
                                    <h1>Congratulations!</h1>
                                    <p>Your order is confirmed, download your resume</p>
                                </div> :
                                <div className="top-banner--banner-txt">
                                    <h1>You are closer to your perfect resume.</h1>
                                    <p>Fill the details to generate your resume </p>
                                </div>
                    }
                    {
                        page === 'download' ?
                            <div className="top-banner--banner-right">
                                
                                <span className="top-banner--banner-right--payment-done ml-0">
                			    
                		        </span>
                            </div> :
                            page === 'buy' ?
                                '' :
                                <div className="top-banner--banner-right">
                                    <button className="white-button mr-20" href="#">Change template</button>
                                    <span className="top-banner--banner-right--banner-thumb">
                                    <img src={`${this.staticUrl}react/assets/images/resume-thumb.jpg`}
                                         alt=""/>
                		            </span>
                                </div>
                    }
                </div>
            </section>
        )
    }
}