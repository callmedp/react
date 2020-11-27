import React from 'react';
import { Link } from 'react-router-dom';
import './footer.scss'

const Footer = (props) => {
    return(
        <footer className="m-container m-footer">
            <span className="m-footer__social mb-10">
                <Link to={"#"}>
                    <figure className="micon-facebook"></figure>
                </Link>
                <Link to={"#"}>
                    <figure className="micon-linkedin"></figure>
                </Link>
                <Link to={"#"}>
                    <figure className="micon-twitter"></figure>
                </Link>
            </span>

            <p className="m-footer__txt">Copyright © 2019 HT Media Limited. <br /><Link to={"#"}>Privacy Policy</Link>  |  <Link to={"#"}>Terms & Conditions</Link></p>
        </footer>
    )
}

export default Footer;