import React from 'react';
import './header.scss';

export default function Header() {
    return(
        <div className="header">
            <span className="header__logo">
                <img src="/media/images/logo.png" alt=""/>
            </span>
            <span className="sprite header__barMenu"></span>
        </div>
    );
}