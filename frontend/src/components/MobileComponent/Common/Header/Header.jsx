import React from 'react';
import { Link } from 'react-router-dom';
import './header.scss'
import { useSelector } from 'react-redux';
import { siteDomain, resumeShineSiteDomain } from 'utils/domains'; 

const Header = (props) => {
    const { setShowSearchPage } = props
    const { name } = useSelector( store => store.skillBanner )
    const { count } = useSelector(store => store.header)
    return(
        <div className="d-flex pl-50">
            <strong className="m-heading2">{name}</strong>
            <div className="m-header__links">
                <a className="micon-search" href="#" onClick={(e)=>{e.preventDefault();setShowSearchPage(true)}}></a>
                <a href={`${siteDomain}/cart/payment-summary/`} className="micon-cart m-header__counter" >
                    { localStorage.getItem('userId') ? <span>{count}</span> : '' }
                </a>
            </div>
        </div>
    )
}

export default Header;