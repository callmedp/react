import React, {Component} from 'react';
import './leftSideBar.scss'
import queryString from "query-string";
import { Link} from 'react-router-dom';
export default class LeftSideBar extends Component {

    constructor(props) {
        super(props);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        const values = queryString.parse(this.props.location.search);

        this.state = {
            type: (values && values.type) || '',
            addmore:{
                'language':false,
                "award":false,
                "course":false,
                "project":false,
                "reference":false
            }
        };
        if (!(values && values.type)) {
            this.props.history.push('/resume-builder/edit/?type=profile')
        }
    }


    handleSpanClick(e) {
        e.stopPropagation();
    }

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search);
            this.setState({
                type: (values && values.type) || ''
            })
        }
    }
    render() {
        const {type,addmore} = this.state;
        return (
            

            <section className="left-sidebar sidebar">
                
                <div className="sidebar__menuWrap">
                    <ul className="sidebar__items">
                        <li className="sidebar__item user">
                            <span className="user__image">
                                <img src="/media/static/react/assets/images/mobile/default-user.jpg" alt="" />
                            </span>
                            <span className="user__name">Hello Amit</span>
                        </li>

                        <li className={"sidebar__item " + (type === 'profile' ? 'sidebar--active' : '')}>
                            <Link to="/resume-builder/edit/?type=profile" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--personal"></i>
                                    <span className="sidebar__link" href="#">Personal</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Personal</span>
                                    <i className="sprite icon--delete"></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'summary' ? 'sidebar--active' : '')}>
                            <Link to="/resume-builder/edit/?type=summary" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--summary"></i>
                                    <span className="sidebar__link" href="#">Summary</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Summary</span>
                                    <i className="sprite icon--delete"></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'experience' ? 'sidebar--active' : '')}>
                            <Link to="/resume-builder/edit/?type=experience" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--experience"></i>
                                    <span className="sidebar__link" href="#">Experience</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Experience</span>
                                    <i className="sprite icon--delete"></i>
                                </div>
                            </Link>
                        </li>
                    
                        <li className={"sidebar__item " + (type === 'education' ? 'sidebar--active' : '')}>
                            <Link to="/resume-builder/edit/?type=education" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--education"></i>
                                    <span className="sidebar__link" href="#">Education </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Education </span>
                                    <i className="sprite icon--delete"></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'skill' ? 'sidebar--active' : '')}>
                            <Link to="/resume-builder/edit/?type=skill" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--skills"></i>
                                    <span className="sidebar__link" href="#">Skills </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Skills </span>
                                    <i className="sprite icon--delete"></i>
                                </div>
                            </Link>
                        </li>

                        <li className="sidebar__item ">
                            <a href="#" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--add-more"></i>
                                    <span className="sidebar__link" href="#">Add more</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Add more sections</span>
                                </div>
                            </a>
                        </li>
                        <li className={"sidebar__item " + (type === 'language' ? 'sidebar--active' : '')
                            + (addmore.language?'':'hide')}>
                            <Link to="/resume-builder/edit/?type=language" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--language"></i>
                                    <span className="sidebar__link" href="#">Languages</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Languages</span>
                                    <i className="sprite icon--add-more"></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'award' ? 'sidebar--active' : '')
                            + (addmore.award?'':'hide')}>
                            <Link to="/resume-builder/edit/?type=award" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--award"></i>
                                    <span className="sidebar__link" href="#">Awards </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Awards </span>
                                    <i className="sprite icon--add-more"></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'course' ? 'sidebar--active' : '')
                            + (addmore.course?'':'hide')}>
                            <Link to="/resume-builder/edit/?type=course" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--course"></i>
                                    <span className="sidebar__link" href="#">Courses </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Courses </span>
                                    <i className="sprite icon--add-more"></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'project' ? 'sidebar--active' : '')
                                + (addmore.project?'':'hide')}>
                            <Link to="/resume-builder/edit/?type=project" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--project"></i>
                                    <span className="sidebar__link" href="#">Projects </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Projects </span>
                                    <i className="sprite icon--add-more"></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'reference' ? 'sidebar--active' : '')
                            + (addmore.reference?'':'hide')}>
                            <Link to="/resume-builder/edit/?type=reference" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--reference"></i>
                                    <span className="sidebar__link" href="#">References </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">References </span>
                                    <i className="sprite icon--add-more"></i>
                                </div>
                            </Link>
                        </li>
                    </ul>   
                </div>

                <ul className="companyMenu">
                    <li className="companyMenu__link"><a href="#">About us</a></li>
                    <li className="companyMenu__link"><a href="#">Privacy Policy</a></li>
                    <li className="companyMenu__link"><a href="#">Terms & Conditions</a></li>
                    <li className="companyMenu__link"><a href="#">Contact Us</a></li>
                    <li className="companyMenu__link mt-20">Copyright © 2019 HT Media Limited.</li>
                </ul>
            </section>
        )
    }
}