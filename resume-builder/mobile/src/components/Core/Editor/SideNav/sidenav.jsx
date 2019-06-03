import React, {Component} from 'react';
import Header from '../../../Common/Header/header';
import './addRemoveNav.scss';


export default class SideNav extends Component {

    render() {
        return (
            <div className="addMore">
                <Header page={'sidenav'}/>
                <p className="fs-14">Add / remove sections in your resume</p>
                <ul className="addMore__items">
                    <li className="addMore__anchor">
                        <div className="addMore__anchor__wrap">
                            <span className="addMore__anchor__wrap--icon">
                                <i class="sprite icon--experience"></i>
                            </span>
                            <span class="addMore__anchor__wrap--link">Experience</span>
                        </div>
                        <i class="sprite icon--delete ml-auto"></i>
                    </li>
                    
                    <li className="addMore__anchor">
                        <div className="addMore__anchor__wrap">
                            <span className="addMore__anchor__wrap--icon">
                                <i class="sprite icon--education"></i>
                            </span>
                            <span class="addMore__anchor__wrap--link">Education</span>
                        </div>
                        <i class="sprite icon--delete ml-auto"></i>
                    </li>
                    
                    <li className="addMore__anchor">
                        <div className="addMore__anchor__wrap">
                            <span className="addMore__anchor__wrap--icon">
                                <i class="sprite icon--skills"></i>
                            </span>
                            <span class="addMore__anchor__wrap--link">Skills</span>
                        </div>
                        <i class="sprite icon--delete ml-auto"></i>
                    </li>
                    
                    <li className="addMore__anchor">
                        <div className="addMore__anchor__wrap">
                            <span className="addMore__anchor__wrap--icon">
                                <i class="sprite icon--language"></i>
                            </span>
                            <span class="addMore__anchor__wrap--link">Languages</span>
                        </div>
                        <i class="sprite icon--delete ml-auto"></i>
                    </li>
                    
                    <li className="addMore__anchor">
                        <div className="addMore__anchor__wrap">
                            <span className="addMore__anchor__wrap--icon">
                                <i class="sprite icon--award"></i>
                            </span>
                            <span class="addMore__anchor__wrap--link">Awards</span>
                        </div>
                        <i class="sprite icon--delete ml-auto"></i>
                    </li>
                </ul>{/* Default menu set */}
                
                <ul className="addMore__items grey-bg pt-0">
                    <li className="addMore__anchor">
                        <div className="addMore__anchor__wrap">
                            <span className="addMore__anchor__wrap--icon">
                                <i class="sprite icon--course"></i>
                            </span>
                            <span class="addMore__anchor__wrap--link">Courses</span>
                        </div>
                        <i class="sprite icon--add-element ml-auto"></i>
                    </li>
                    
                    <li className="addMore__anchor">
                        <div className="addMore__anchor__wrap">
                            <span className="addMore__anchor__wrap--icon">
                                <i class="sprite icon--project"></i>
                            </span>
                            <span class="addMore__anchor__wrap--link">Projects</span>
                        </div>
                        <i class="sprite icon--add-element ml-auto"></i>
                    </li>
                    
                    <li className="addMore__anchor">
                        <div className="addMore__anchor__wrap">
                            <span className="addMore__anchor__wrap--icon">
                                <i class="sprite icon--reference"></i>
                            </span>
                            <span class="addMore__anchor__wrap--link">References</span>
                        </div>
                        <i class="sprite icon--add-element ml-auto"></i>
                    </li>
                </ul>{/* To add on  menu set */}

                <div className="bottom-ctc">
                    <span className="link-color">Cancel</span>
                    <span className="btn__primary">Done</span>
                </div>
            </div>
        )
    }
}

