import React from 'react';
import { Link } from 'react-router-dom';
import './header.scss'
import { useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains'; 
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const Header = (props) => {
    const { setShowSearchPage, hideName, name, showSearchButton=true, icon=false } = props
    const { count } = useSelector(store => store.header)
    const sendLearningTracking = useLearningTracking();

    const cartTracking = () => {
        MyGA.SendEvent('header_icons','ln_header_icons', 'ln_cart', 'cart','', false, true)
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_add_to_cart`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'add_to_cart',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return(
        <div className="d-flex pl-50">
            { !hideName && !icon && <strong className="m-heading2 flex-1">{name}</strong>}
            { icon &&  <strong className="m-heading2"><figure className="icon-shine-learning"></figure></strong> } {/* for homepage */}
            <div className="m-header__links">
                {   showSearchButton &&
                    <a className="micon-search" href="#" onClick={(e)=>{e.preventDefault();setShowSearchPage(true)}}></a>
                }
                <a href={`${siteDomain}/cart/payment-summary/`} className="micon-cart m-header__counter" onClick={cartTracking}>
                    <span>{count}</span>
                </a>
            </div>
        </div>
    )
}

export default Header;