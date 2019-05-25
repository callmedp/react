import React, {Component} from 'react';
import { Link} from 'react-router-dom';

export default class  RenderNavItem extends Component {

    render(){
        const {label,type,sidenavStatus,title,exist,current_page,changeLink,iconClass,
            removeItem,addItem,deleteIconExist,pos,error,showErrorMessage} = this.props
        return( 
            <React.Fragment>
               {error ?
                    <li className={"sidebar__item " + (type === title ? 'sidebar--active' : '') 
                        + (exist || sidenavStatus ? '' : 'hide')} onClick={()=>{showErrorMessage(title)}}>
                            <div 
                                className="sidebar__anchor" >
                                <div className="sidebar__wrap">
                                    <i className={iconClass}></i>
                                    <span className="sidebar__link">{label}</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link">{label}</span>
                                    {deleteIconExist ?
                                        <i className={"sprite " + (exist? "icon--delete" : "icon--add-more")}
                                            onClick={exist ? removeItem.bind(this,pos) : addItem.bind(this,pos)}></i> :
                                        ""
                                    }
                                </div>
                            </div>
                        </li>:
                        <li className={"sidebar__item " + (type === title ? 'sidebar--active' : '')
                                + (exist || sidenavStatus ? '' : 'hide')}>
                            <Link to={"/resume-builder/edit/?type=" +(!sidenavStatus ? title  : current_page)} 
                                className="sidebar__anchor" onClick={!sidenavStatus ? changeLink.bind(this,title) : ()=>{}}>
                                <div className="sidebar__wrap">
                                    <i className={iconClass}></i>
                                    <span className="sidebar__link">{label}</span>
                                </div>

                                <div className="sidebar-open__wrap">
                                    <span className="sidebar-open__link">{label}</span>
                                    {deleteIconExist ?
                                        <i className={"sprite " + (exist? "icon--delete" : "icon--add-more")}
                                            onClick={exist ? removeItem.bind(this,pos) : addItem.bind(this,pos)}></i> :
                                        ""
                                    }
                                </div>
                            </Link>
                        </li>
                    }
            </React.Fragment>
        )
        
    }
    
}