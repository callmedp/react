import React, {Component} from 'react';
import './footer.scss'

export default class Footer extends Component {
    render() {
        return (
            <footer>
	            <div className="container">
	            	<div className="container--footer-links">
	            	<a href="#">About Us</a> <a href="#">Privacy Policy</a> <a href="#">Terms & Condition</a> <a href="#">Contact us</a>
		            </div>
		            <div className="container--footer-txt">Copyright © 2019 HT Media Limited.</div>
	            </div>
            </footer>
        )
    }

}
