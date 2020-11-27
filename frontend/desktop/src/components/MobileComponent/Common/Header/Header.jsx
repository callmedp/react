import React from 'react';
import { Link } from 'react-router-dom';
import './header.scss'

const Header = (props) => {
    return(
        <header className="m-container m-header m-skill-ht">
            <strong className="m-heading2">Digital Marketing</strong>
            <div className="m-header__links">
                <Link className="micon-search" to={"#"}></Link>
                <Link className="micon-cart m-header__counter" to={"#"}>
                    <span>5</span>
                </Link>
            </div>
        </header>
    )
}

export default Header;