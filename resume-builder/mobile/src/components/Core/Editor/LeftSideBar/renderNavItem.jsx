import React, {Component} from 'react';
import { Link} from 'react-router-dom';

export default class  RenderNavItem extends Component {

    render(){
        const {label,type,sidenavStatus,title,exist,current_page,changeLink,iconClass,
            removeItem,addItem,deleteIconExist} = this.props
        return(
            <React.Fragment>
            <li>{label}</li>
            <li>{type}</li>
            <li>{sidenavStatus}</li>
            <li>{title}</li>
            <li>{exist}</li>
            </React.Fragment>
            // <li className={"sidebar__item " + (type === {title} ? 'sidebar--active' : '')
            //     + (exist || sidenavStatus ? '' : 'hide')}>
            //     <Link to={"/resume-builder/edit/?type=" +(!sidenavStatus ? {title}  : current_page)} 
            //         className="sidebar__anchor" onClick={!sidenavStatus ? changeLink(title) : ()=>{}}>
            //         <div className="sidebar__wrap">
            //             <i className={iconClass}></i>
            //             <span className="sidebar__link" href="#">{label}</span>
            //         </div>

            //         <div className="sidebar-open__wrap">
            //             <span className="sidebar-open__link" href="#">{label}</span>
            //             {deleteIconExist ?
            //                 <i className={"sprite " + (exist? "icon--delete" : "icon--add-more")}
            //                     onClick={exist ? removeItem("summary") : addItem("summary")}></i> :
            //                 ""
            //             }
            //         </div>
            //     </Link>
            // </li>
        )
        
    }
    
}