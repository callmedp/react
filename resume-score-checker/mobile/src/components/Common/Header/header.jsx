import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { menuData } from './menuData';
import './header.scss';

class Header extends Component {

    constructor(porps) {
        super(porps);   

        this.state = {
            isSideBarOpen: false
        }
    }

    handleMenuButtonClick = () => {
        this.setState({isSideBarOpen: ! this.state.isSideBarOpen})
	};

    render() {
        const {isSideBarOpen} = this.state;
        return(
            <div className="header">
                <span className="sprite header__barMenu mr-15" onClick={this.handleMenuButtonClick}></span>
    
                <Link to = "/">
                    <span className="header__logo">
                        <img src="/media/images/logo.png" alt=""/>
                    </span>
                </Link>
    
                {/* SideBar */}
                    { menuData.length && (
                        <nav className={`nav ${isSideBarOpen ? 'show' : ''}`}>
                            <div className="nav__loginWrap align-items-center">
                                <span className="nav__loginWrap__image mr-15">
                                    <img src="/media/images/user-loggedin.jpg" alt=""/>
                                </span>

                                <div className="flex-1">
                                    <h3>Welcome Guest</h3>
                                    <div className="mt-10 d-flex justify-content-between">
                                        <a href="#" className="py-5 btn btn-round-30 btn-outline-white px-20">Login</a>
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
                <div className={`overlay ${isSideBarOpen ? 'show' : ''}`} onClick={this.handleMenuButtonClick}></div>
            </div>
        );
    }
}

export default Header;