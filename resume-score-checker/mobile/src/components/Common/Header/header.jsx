import React from 'react';
import { Link } from 'react-router-dom';
import { menuData } from './menuData';
import './header.scss';
import { useState } from 'react';
import { imageUrl } from '../../../Utils/domains';

export default function Header() {
        const [isSideBarOpen, setIsSideBarOpen]=useState(false)
        const handleMenuButtonClick = () => {
            setIsSideBarOpen(!isSideBarOpen)
        };
        return(
            <div className="header">
                <span className="sprite header__barMenu mr-15" onClick={handleMenuButtonClick}></span>
    
                <Link to = "/resume-score-checker">
                    <span className="header__logo">
                        <img src={`${imageUrl}score-checker/images/mobile/logo.png`} alt="Header"/>
                    </span>
                </Link>
    
                {/* SideBar */}
                    { menuData.length && (
                        <nav className={`nav ${isSideBarOpen ? 'show' : ''}`}>
                            <div className="nav__loginWrap align-items-center">
                                <span className="nav__loginWrap__image mr-15">
                                    <img src={`${imageUrl}score-checker/images/user-loggedin.jpg`} alt=""/>
                                </span>

                                <div className="flex-1">
                                    <h3>Welcome Guest</h3>
                                    <div className="mt-10 d-flex justify-content-between">
                                        <a href="https://learning.shine.com/login/" className="py-5 btn btn-round-30 btn-outline-white px-20">Login</a>
                                    </div>
                                </div>


                            </div>
                            <ul>
                                { menuData.map((item) =>
                                    <li key={item.label}>
                                        <a href={item.url}>
                                            <i className={item.icon}></i>
                                            {item.label}
                                        </a>
                                    </li>
                                )}
                            </ul>

                            <hr/>

                            <div className="p-15">
                                <strong className="d-block">Call us:</strong>
                                <a className="d-block" href="tel:0124-4312500">0124-4312500/01</a>
                            </div>
                        </nav>

                    )}
                <div className={`overlay ${isSideBarOpen ? 'show' : ''}`} onClick={handleMenuButtonClick}></div>
            </div>
        );
    }