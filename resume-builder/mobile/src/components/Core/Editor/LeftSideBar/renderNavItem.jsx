import React, {Component} from 'react';
import { Link} from 'react-router-dom';

export default class  RenderNavItem extends Component {

    render(){
        const {label,type,sidenavStatus,title,exist,listOfLinks,changeLink,iconClass,
            error,showErrorMessage,newUser} = this.props
        return( 
            <React.Fragment>
               {error || newUser ?
                    <li className={"sidebar__item " + (type === title ? 'sidebar--active' : '') 
                        + (exist || sidenavStatus ? '' : 'hide')} onClick={()=>{showErrorMessage(title)}}>
                            <div 
                                className="sidebar__anchor" >
                                <div className="sidebar__wrap">
                                    <i className={iconClass}></i>
                                    <span className="sidebar__link">{label}</span>
                                </div>
                            </div>
                        </li>:

                        <li className={"sidebar__item " + (type === title ? 'sidebar--active' : '')}>
                            <Link to={`/resume-builder/edit/?type=${title}`} 
                                className="sidebar__anchor" onClick={changeLink.bind(this,title,listOfLinks)}>
                                <div className="sidebar__wrap">
                                    <i className={iconClass}></i>
                                    <span className="sidebar__link">{label}</span>
                                </div>
                            </Link>
                        </li>
                    }
            </React.Fragment>
        )
        
    }
    
}