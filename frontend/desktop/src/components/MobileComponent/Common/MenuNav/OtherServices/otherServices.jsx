import React from "react";
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom';
import '../FreeResources/freeResources.scss';
import { resumeShineSiteDomain } from 'utils/domains';

const OtherServices = props => {
    const { setType, setOpen, open } = props
    const resetNav = () => {
            setOpen(state => !state);
            setType('menu')
        }
  
    return (
        <Menu className={ 'navigation' } width={ '300px' } isOpen={open} onStateChange={state=>setOpen(state.isOpen)}>
        <div className="m-guest-section">
            <React.Fragment>
            <div className="micon-back-menu-white" onClick={() => setType('menu')}></div>
            <div className="media-body">
                <p className="menuText">Other Services</p>
            </div>
            </React.Fragment>  
        </div>
        <div className="m-menu-links">
            <a className="menu-item" href={`${resumeShineSiteDomain}/resume-builder`} onClick={resetNav} >Resume Builder</a>
            <a className="menu-item" href={`${resumeShineSiteDomain}/product/jobs-on-the-move-4/3414`} onClick={resetNav} >Jobs on the move</a>
            <a className="menu-item" href={`${resumeShineSiteDomain}/resume-score-checker`} onClick={resetNav} >Resume Score Checker</a>
        </div>
        </Menu>
    );
}

export default OtherServices;