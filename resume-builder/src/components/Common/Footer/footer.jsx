import React, {Component} from 'react';
import './footer.scss'

export default class Footer extends Component {
    render() {
        return (
            <footer>
	            <div className="container">
	            	<div className="container--footer-links">
	            	<a href="/about-us">About Us</a> <a href="/privacy-policy">Privacy Policy</a> <a href="/tnc">Terms & Condition</a> <a href="/contact-us">Contact us</a>
		            </div>
		            <div className="container--footer-txt">Copyright © 2019 HT Media Limited.</div>
	            </div>
            </footer>
        )
    }

}
