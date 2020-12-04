import React from "react";
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom';
import { resumeShineSiteDomain } from 'utils/domains';

const RecruiterReach = props => {
    const { setType, setOpen, open } = props
    const resetNav = () => {
        setOpen(state => !state);
        setType('menu')
    }

  return (
    <Menu className='navigation' width={'300px'} isOpen={open} onStateChange={state=> setOpen(state.isOpen)}>
      <div className="m-guest-section">
        <React.Fragment>
          <div className="micon-back-menu-white" onClick={() => setType('menu')}></div>
          <div className="media-body">
            <p className="menuText">Recruiter Reach</p>
          </div>
        </React.Fragment>
      </div>
      <div className="m-menu-links">
        <a className="menu-item" href={`${resumeShineSiteDomain}/product/application-highlighter-3/4117`} onClick={resetNav} >Application Highlighter</a>
        <a className="menu-item" href={`${resumeShineSiteDomain}/product/featured-profile-10/1939`} onClick={resetNav} >Featured Profile</a>
        <a className="menu-item" href={`${resumeShineSiteDomain}/product/improved-visibility-package-3-month/2645`} onClick={resetNav} >Improved Visibility Package</a>
      </div>
    </Menu>
  );
}

export default RecruiterReach;