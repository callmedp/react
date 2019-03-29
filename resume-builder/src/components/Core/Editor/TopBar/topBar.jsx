import React, {Component} from 'react'
import './topBar.scss'

export default class TopBar extends Component {

    constructor(props) {
        super(props);

    }


    render() {
        const {page} = this.props;
        return (
            <section className="flex-container">
                <div className="top-banner">
                    {
                        page === 'buy' ?
                            <div className="top-banner--banner-txt">
                                <h1>Buy page.</h1>
                                <p>Fill the details to generate your resume </p>
                            </div> :
                            page === 'download' ?
                                <div className="top-banner--banner-txt">
                                    <h1>Download Page.</h1>
                                    <p>Fill the details to generate your resume </p>
                                </div> :
                                <div className="top-banner--banner-txt">
                                    <h1>You are closer to your perfect resume.</h1>
                                    <p>Fill the details to generate your resume </p>
                                </div>
                    }
                    {
                        page === 'download' ?
                            <div className="top-banner--banner-right">
                                <button className="white-button mr-20" href="#">Change template</button>
                                <span className="top-banner--banner-right--banner-thumb">
                			    <img src="/media/static/react/assets/images/resume-thumb.jpg" alt=""/>
                		        </span>
                            </div> :
                            page === 'buy' ?
                                '' :
                                <div className="top-banner--banner-right">
                                    <button className="white-button mr-20" href="#">Change template</button>
                                    <span className="top-banner--banner-right--banner-thumb">
                                    <img src="/media/static/react/assets/images/resume-thumb.jpg" alt=""/>
                		            </span>
                                </div>
                    }
                </div>
            </section>
        )
    }
}