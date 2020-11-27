import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { slide as Menu } from 'react-burger-menu';
import './menuNav.scss'
 
 
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
          <Link className="menu-item" to="{#}"><figure className="micon-resume-service"></figure> Resume Services <figure className="icon-arrow-menusm ml-auto"></figure></Link>
          <Link className="menu-item" to="{#}"><figure className="micon-linkedin-service"></figure> Linkedin</Link>
          <Link className="menu-item" to="{#}"><figure className="micon-recruiter-service"></figure> Recruiter Reach</Link>
          <Link className="menu-item" to="{#}"><figure className="micon-free-resources"></figure> Free Resources <figure className="icon-arrow-menusm ml-auto"></figure></Link>
          <Link className="menu-item" to="{#}"><figure className="micon-other-services"></figure> Other Services <figure className="icon-arrow-menusm ml-auto"></figure></Link>
          <Link className="menu-item" to="{#}"><figure className="micon-courses-services"></figure> Courses</Link>
          <Link className="menu-item" to="{#}"><figure className="micon-blog-services"></figure> Blog</Link>
          <Link className="menu-item" to="{#}">About us</Link>
          <Link className="menu-item" to="{#}">Contact us</Link>
        </div>
      </Menu>
    );
  }
}

export default MenuNav;