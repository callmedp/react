import React, {Component} from 'react'
import './topBar.scss'
export default class TopBar extends Component {
    render() {
        return (
            <section className="flex-container">
                <div className="top-banner">
                	<div className="top-banner--banner-txt">
                		<h1>You are closer to your perfect resume.</h1>
	                	<p>Fill the details to generate your resume </p>
                	</div>
                	<div className="top-banner--banner-right">
                		<a className="white-button mr-20" href="#">Change template</a>
                		<span className="top-banner--banner-right--banner-thumb">
                			<img src="/images/resume-thumb.jpg" alt="" />
                		</span>
                	</div>
                </div>
            </section>
        )
    }
}