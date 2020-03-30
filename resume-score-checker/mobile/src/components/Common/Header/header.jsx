import React from 'react';
import { Link } from 'react-router-dom';
import './header.scss';

export default function Header() {
    return(
        <div className="header">
            <Link to = "/">
                <span className="header__logo">
                    <img src="/media/images/logo.png" alt=""/>
                </span>
            </Link>
            <span className="sprite header__barMenu"></span>
        </div>
    );
}