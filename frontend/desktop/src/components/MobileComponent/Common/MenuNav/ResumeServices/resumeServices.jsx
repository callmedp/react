import React from "react";
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom';
import { resumeShineSiteDomain } from 'utils/domains';

const ResumeServices = props => {
    const { setType, setOpen } = props
    const resetNav = () => {
        setOpen(state => !state);
        setType('menu')
    }

  return (
    <Menu className='navigation' width={'300px'} isOpen={true}>
      <div className="m-guest-section">
        <React.Fragment>
          <div className="micon-back-menu-white" onClick={() => setType('menu')}></div>
          <div className="media-body">
            <p className="menuText">Resume Services</p>
          </div>
        </React.Fragment>
      </div>
      <div className="m-menu-links">
        <a className="menu-item" href={`${resumeShineSiteDomain}/product/entry-level/1922/`} onClick={resetNav} >Resume Writing Services</a>
        <a className="menu-item" href={`${resumeShineSiteDomain}/product/entry-level-freshers/2052`} onClick={resetNav} >Visual Resume</a>
        <a className="menu-item" href={`${resumeShineSiteDomain}/product/entry-level-freshers-4/2553`} onClick={resetNav} >International Resume</a>
      </div>
    </Menu>
  );
}

export default ResumeServices;