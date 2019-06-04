import React, {Component} from 'react';


export default class Menuitem extends Component {
    render(){
        const {iconClass,label,exist,addItem,removeItem,pos,deleteIconExist} = this.props;
        return( 
            <li className="addMore__anchor">
                <div className="addMore__anchor__wrap">
                    <span className="addMore__anchor__wrap--icon">
                        <i className={iconClass}></i>
                    </span>
                    <span className="addMore__anchor__wrap--link">{label}</span>
                </div>
                <div className="delete-wrap" onClick={exist ? removeItem.bind(this,pos) : addItem.bind(this,pos) }>
                    {deleteIconExist ? 
                        <i className={"sprite ml-auto " + (exist ? "icon--delete":"icon--add-element")}></i>:''
                    }
                </div>
            </li>
        )
    }
}