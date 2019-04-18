import React, {Component} from 'react';
import './leftSideBar.scss'
import queryString from "query-string";
import { Link} from 'react-router-dom';
export default class LeftSideBar extends Component {

    constructor(props) {
        super(props);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        this.addMore = this.addMore.bind(this);
        this.addItem = this.addItem.bind(this);
        this.removeItem = this.removeItem.bind(this);
        const values = queryString.parse(this.props.location.search);

        this.state = {
            type: (values && values.type) || '',
            addmore:{
                "profile":true,
                "summary":true,
                "experience":true,
                "education":true,
                "skill":true,
                'language':false,
                "award":false,
                "course":false,
                "project":false,
                "reference":false
            },
            sidebar_open:false
        };
        if (!(values && values.type)) {
            this.props.history.push('/resume-builder/edit/?type=profile')
        }
    }


    handleSpanClick(e) {
        e.stopPropagation();
    }

    addMore(){
        this.setState({
            sidebar_open:true
        })

    }

    addItem(item){
        let addmore = {...this.state.addmore};
        addmore[item] = true
        this.setState({
            addmore
        })
    }

    removeItem(item){
        let addmore = {...this.state.addmore};
        addmore[item] = false
        this.setState({
            addmore
        })
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
        const {type,addmore,sidebar_open} = this.state;
        return (
            

            <section className={"left-sidebar sidebar " + (sidebar_open ? "sidebar-open" : "")}>
                
                <div className="sidebar__menuWrap">
                    <ul className="sidebar__items">
                        <li className="sidebar__item user">
                            <span className="user__image">
                                <img src="/media/static/react/assets/images/mobile/default-user.jpg" alt="" />
                            </span>
                            <span className="user__name">Hello Amit</span>
                        </li>

                        <li className={"sidebar__item " + (type === 'profile' ? 'sidebar--active' : '')
                            + (addmore.profile || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=profile" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--personal"></i>
                                    <span className="sidebar__link" href="#">Personal</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Personal</span>
                                    <i className={"sprite " + (addmore.profile ? "icon--delete" : "icon--add-more")}
                                       onClick={addmore.profile ? this.removeItem.bind(this,"profile") : this.addItem.bind(this,"profile")}></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'summary' ? 'sidebar--active' : '')
                            + (addmore.summary || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=summary" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--summary"></i>
                                    <span className="sidebar__link" href="#">Summary</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Summary</span>
                                    <i className={"sprite " + (addmore.summary ? "icon--delete" : "icon--add-more")}
                                     onClick={addmore.summary ? this.removeItem.bind(this,"summary") : this.addItem.bind(this,"summary")}></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'experience' ? 'sidebar--active' : '')
                            + (addmore.experience || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=experience" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--experience"></i>
                                    <span className="sidebar__link" href="#">Experience</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Experience</span>
                                    <i className={"sprite " + (addmore.experience ? "icon--delete" : "icon--add-more")}
                                     onClick={addmore.experience ? this.removeItem.bind(this,"experience") : this.addItem.bind(this,"experience")}></i>
                                </div>
                            </Link>
                        </li>
                    
                        <li className={"sidebar__item " + (type === 'education' ? 'sidebar--active' : '')
                            + (addmore.education || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=education" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--education"></i>
                                    <span className="sidebar__link" href="#">Education </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Education </span>
                                    <i className={"sprite " + (addmore.education ? "icon--delete" : "icon--add-more")}
                                     onClick={addmore.education ? this.removeItem.bind(this,"education") : this.addItem.bind(this,"education")}></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'skill' ? 'sidebar--active' : '')
                            + (addmore.skill || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=skill" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--skills"></i>
                                    <span className="sidebar__link" href="#">Skills </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Skills </span>
                                    <i className={"sprite " + (addmore.skill ? "icon--delete" : "icon--add-more")}
                                     onClick={addmore.skill ? this.removeItem.bind(this,"skill") : this.addItem.bind(this,"skill")}></i>
                                </div>
                            </Link>
                        </li>
                        <li className={"sidebar__item " + (type === 'language' ? 'sidebar--active' : '')
                            + (addmore.language || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=language" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--language"></i>
                                    <span className="sidebar__link" href="#">Languages</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Languages</span>
                                    <i className={"sprite " + (addmore.language ? "icon--delete" : "icon--add-more")}
                                     onClick={addmore.language ? this.removeItem.bind(this,"language") : this.addItem.bind(this,"language")}></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'award' ? 'sidebar--active' : '')
                            + (addmore.award || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=award" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--award"></i>
                                    <span className="sidebar__link" href="#">Awards </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Awards </span>
                                    <i className={"sprite " + (addmore.award ? "icon--delete" : "icon--add-more")}
                                     onClick={addmore.award ? this.removeItem.bind(this,"award") : this.addItem.bind(this,"award")}></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'course' ? 'sidebar--active' : '')
                            + (addmore.course || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=course" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--course"></i>
                                    <span className="sidebar__link" href="#">Courses </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Courses </span>
                                    <i className={"sprite " + (addmore.course ? "icon--delete" : "icon--add-more")}
                                     onClick={addmore.course ? this.removeItem.bind(this,"course") : this.addItem.bind(this,"course")}></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'project' ? 'sidebar--active' : '')
                                + (addmore.project || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=project" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--project"></i>
                                    <span className="sidebar__link" href="#">Projects </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Projects </span>
                                    <i className={"sprite " + (addmore.project ? "icon--delete" : "icon--add-more")}
                                     onClick={addmore.project ? this.removeItem.bind(this,"project") : this.addItem.bind(this,"project")}></i>
                                </div>
                            </Link>
                        </li>
                        
                        <li className={"sidebar__item " + (type === 'reference' ? 'sidebar--active' : '')
                            + (addmore.reference || sidebar_open ? '' : 'hide')}>
                            <Link to="/resume-builder/edit/?type=reference" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--reference"></i>
                                    <span className="sidebar__link" href="#">References </span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">References </span>
                                    <i className={"sprite " + (addmore.reference ? "icon--delete" : "icon--add-more")}
                                     onClick={(event) => addmore.reference ? this.removeItem.bind(this,"reference",event) : this.addItem.bind(this,"reference",event)}></i>
                                </div>
                            </Link>
                        </li>
                        <li className={"sidebar__item " + (sidebar_open ? "hide" : "")}>
                            <a href="#" className="sidebar__anchor">
                                <div className="sidebar__wrap">
                                    <i className="sprite icon--add-more"></i>
                                    <span className="sidebar__link" onClick={this.addMore}>Add more</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link" href="#">Add more sections</span>
                                </div>
                            </a>
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