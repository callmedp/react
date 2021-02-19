import React from 'react';
import { Link } from 'react-router-dom';
import './header.scss'
import { useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains'; 
import { MyGA } from 'utils/ga.tracking.js';

const Header = (props) => {
    const { setShowSearchPage, hideName, name, showSearchButton=true, icon=false } = props
    const { count } = useSelector(store => store.header)
    return(
        <div className="d-flex pl-50">
            { !hideName && !icon && <strong className="m-heading2">{name}</strong>}
            { icon &&  <strong className="m-heading2"><figure className="icon-shine-learning"></figure></strong> } {/* for homepage */}
            <div className="m-header__links">
                {   showSearchButton &&
                    <a className="micon-search" href="#" onClick={(e)=>{e.preventDefault();setShowSearchPage(true)}}></a>
                }
                <a href={`${siteDomain}/cart/payment-summary/`} className="micon-cart m-header__counter" onClick={() => MyGA.SendEvent('header_icons','ln_header_icons', 'ln_cart', 'cart','', false, true)}>
                    <span>{count}</span>
                </a>
            </div>
        </div>
    )
}

export default Header;