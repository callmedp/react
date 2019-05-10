import React, {Component} from 'react'
import {Link} from 'react-router-dom'
import './topBar.scss'

export default class TopBar extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }

    render() {
        const {page} = this.props;
        let {selected_template} =this.props.userInfo
        if(localStorage.getItem('selected_template')){
            selected_template =localStorage.getItem('selected_template')
        }
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
                                    <Link to={'/resume-builder/#templates'}>
                                        <button className="white-button mr-20">Change template</button>
                                    </Link>
                                    <span className="top-banner--banner-right--banner-thumb">
                                    <img src={`${this.staticUrl}react/assets/images/resume-thumb-${selected_template}.jpg`}
                                         alt=""/>
                		            </span>
                                </div>
                    }
                </div>
            </section>
        )
    }
}