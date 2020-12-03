import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { slide as Menu } from 'react-burger-menu';
import './menuNav.scss'
import { siteDomain } from 'utils/domains'; 
 
 
class MenuNav extends React.Component {
  showSettings (event) {
    event.preventDefault();
  }
 
  render () {
    return (
      <Menu>
        <div className="m-guest-section">
          <figure className="micon-user-pic"></figure>
          <div className="media-body">
            <strong>Welcome Guest</strong>
            <p>
              <Link className="btn-white-outline" to="{#}">Login</Link>
              <Link className="btn-white-outline" to="{#}">Register</Link>
            </p>
          </div>
        </div>
        <div className="m-menu-links">
          <Link className="menu-item" to="{#}"><figure className="micon-home"></figure> Home</Link>
          <Link className="menu-item" to="{#}"><figure className="micon-resume-service"></figure> Resume Services <figure className="micon-arrow-menusm ml-auto"></figure></Link>
          <Link className="menu-item" to="{#}"><figure className="micon-linkedin-service"></figure> Linkedin Profile Writing</Link>
          <Link className="menu-item" to="{#}"><figure className="micon-recruiter-service"></figure> Recruiter Reach <figure className="micon-arrow-menusm ml-auto"></figure></Link>
          <Link className="menu-item" to="{#}"><figure className="micon-free-resources"></figure> Free Resources <figure className="micon-arrow-menusm ml-auto"></figure></Link>
          <Link className="menu-item" to="{#}"><figure className="micon-other-services"></figure> Other Services <figure className="micon-arrow-menusm ml-auto"></figure></Link>
          <a className="menu-item" href={`${siteDomain}/`}><figure className="micon-courses-services"></figure> Courses</a>
          <a className="menu-item" href={`${siteDomain}/talenteconomy/`}><figure className="micon-blog-services"></figure> Blog</a>
          <a className="menu-item" href={`${siteDomain}/about-us`}>About us</a>
          <a className="menu-item" href={`${siteDomain}/contact-us`}>Contact us</a>
        </div>
      </Menu>
    );
  }
}

export default MenuNav;