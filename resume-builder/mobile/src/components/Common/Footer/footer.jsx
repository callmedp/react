import React, {Component} from 'react';
import './footer.scss'

export default class Footer extends Component {
    render() {
        return (
            <footer className="footer">
                <ul className="footer__items">
                    <li className="footer__item"><a href="/privacy-policy">Privacy Policy</a></li>
                    <li className="footer__item"><a href="/tnc">Terms & Condition</a></li>
                    <li className="footer__item"><a href="/contact-us">Contact us</a></li>
                </ul>
                <p>Copyright © 2020 HT Media Limited. All rights reserved</p>
            </footer>
        )
    }

}
