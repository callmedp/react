import React, {Component} from 'react';
import { Link} from 'react-router-dom';

export default class  RenderNavItem extends Component {

    render(){
        const {label,type,sidenavStatus,title,exist,current_page,changeLink,iconClass,
            removeItem,addItem,deleteIconExist,pos} = this.props
        return( 
            <React.Fragment>
            {/* {console.log("rendering Started")}
            {console.log("label",label)}{console.log("type",type)}{console.log("sidenavStatus",sidenavStatus)}{console.log("title",title)}
            {console.log("exist",exist)}{console.log("cur_page",current_page)}
            {console.log("rendering End")} */}
            {/* {console.log("iconClass",iconClass)} */}
            <li className={"sidebar__item " + (type === title ? 'sidebar--active' : '')
                + (exist || sidenavStatus ? '' : 'hide')}>
                <Link to={"/resume-builder/edit/?type=" +(!sidenavStatus ? title  : current_page)} 
                    className="sidebar__anchor" onClick={!sidenavStatus ? changeLink.bind(this,title) : ()=>{}}>
                    <div className="sidebar__wrap">
                        <i className={iconClass}></i>
                        <span className="sidebar__link" href="#">{label}</span>
                    </div>

                    <div className="sidebar-open__wrap">
                        <span className="sidebar-open__link" href="#">{label}</span>
                        {deleteIconExist ?
                            <i className={"sprite " + (exist? "icon--delete" : "icon--add-more")}
                                onClick={exist ? removeItem.bind(this,pos) : addItem.bind(this,pos)}></i> :
                            ""
                        }
                    </div>
                </Link>
            </li>
            </React.Fragment>
        )
        
    }
    
}