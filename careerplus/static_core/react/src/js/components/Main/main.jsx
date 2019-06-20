import React from "react";
import {NavLink} from "react-router-dom";
import {RouteWithSubRoutes} from "../../routes";

class Main extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {

        const {routes, location} = this.props;
        const isPricing = !!(location.pathname === '/resume-builder/pricing') || !!(location.pathname === '/resume-builder/pricing/');
        return (
            <div className="container pr">
                {
                    !isPricing &&
                    <div>
                        <div>
                            <ul className={'Row-navigation'}>
                                <li>
                                    <NavLink to="/resume-builder" exact activeClassName={'Highlight'}>Home</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/register"
                                             activeClassName={'Highlight'}>Register</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/detail" activeClassName={'Highlight'}>Detail</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/skill" activeClassName={'Highlight'}>Skill</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/experience"
                                             activeClassName={'Highlight'}>Experience</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/education"
                                             activeClassName={'Highlight'}>Education</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/project"
                                             activeClassName={'Highlight'}>Project</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/certification"
                                             activeClassName={'Highlight'}>Certification</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/achievement"
                                             activeClassName={'Highlight'}>Achievement</NavLink>
                                </li>
                                <li>
                                    <NavLink to="/resume-builder/reference"
                                             activeClassName={'Highlight'}>Reference</NavLink>
                                </li>
                            </ul>
                        </div>
                    </div>
                }
                {
                    !isPricing &&
                    <header className="login-page-bg">
                        <div className="login-bg-txt">
                            <figure className="login-icon1"></figure>
                            <strong>1 Lacs+</strong>
                            Satisfied users
                        </div>
                        <div className="login-bg-txt">
                            <figure className="login-icon2"></figure>
                            <strong>300+</strong>
                            Courses
                        </div>
                        <div className="login-bg-txt">
                            <figure className="login-icon3"></figure>
                            <strong>500+</strong>
                            Professional resumes delivered
                        </div>
                    </header>
                }
                {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
            </div>
        );
    }
}

export default Main;