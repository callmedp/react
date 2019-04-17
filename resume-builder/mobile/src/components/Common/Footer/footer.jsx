import React, {Component} from 'react';
import './footer.scss'

export default class Footer extends Component {
    render() {
        return (
            <footer className="footer">
                <ul className="footer__items">
                    <li className="footer__item"><a href="#">Privacy Policy</a></li>
                    <li className="footer__item"><a href="#">Terms & Condition</a></li>
                    <li className="footer__item"><a href="#">Contact us</a></li>
                </ul>
                <p>Copyright © 2019 HT Media Limited. All rights reserved</p>
            </footer>
        )
    }

}
