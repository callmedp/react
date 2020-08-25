import React, {Component} from 'react';
import Header from '../../../Common/Header/header';
import './menu.scss';
import {connect} from "react-redux";
import {entityLinkNameLink,iconClassList,delete_icon} from '../../../../Utils/entitydata.js'
import {updateListOfLink} from "../../../../store/sidenav/actions";
import {updatePersonalInfo} from "../../../../store/personalInfo/actions"
import Menuitem from './menuItem';
import moment from 'moment'
import Loader from '../../../Common/Loader/loader';
import {eventClicked} from '../../../../store/googleAnalytics/actions/index'
import { trackUser } from '../../../../store/tracking/actions/index';
import { isTrackingInfoAvailable, getTrackingInfo } from "../../../../Utils/common";

class Menu extends Component {

    constructor(props){
        super(props);
        this.state = {
            addmore: [
            ]
        }
        this.addItem = this.addItem.bind(this);
        this.removeItem = this.removeItem.bind(this);
        this.saveMenu = this.saveMenu.bind(this);
        this.closeMenu = this.closeMenu.bind(this);
        this.sendTrackingInfo = this.sendTrackingInfo.bind(this);
    }

    componentDidMount(){
        const {personalInfo:{entity_preference_data},history} = this.props
        if(!entity_preference_data.length){
            history.push(`/resume-builder/edit/?type=profile`)
        }
        this.setState({addmore: entity_preference_data})
    }
    sendTrackingInfo(action, position) {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId, productId } = getTrackingInfo();
            const {userTrack} = this.props;
            userTrack({ trackingId, productTrackingMappingId, productId, action, position });
        }
    }

    componentDidUpdate(prevProps){
        const {personalInfo:{entity_preference_data}} = this.props

        if (entity_preference_data !== prevProps.personalInfo.entity_preference_data) {  
            this.setState({addmore: entity_preference_data})
        }

    }

    async saveMenu() {
        const {addmore} = this.state
        const {sidenav:{currentLinkPos},updateMenuItems,personalInfo,updateListOfLink,history,eventClicked} = this.props

        eventClicked({
            'action':'CompletedAddRemove',
            'label':'Click'
        })

        this.sendTrackingInfo('mobile_done_add_remove_menu',1)
        let links = []
        for (let i of addmore) {
            if (i.active) {
                links.push(entityLinkNameLink[i.entity_id])
            }
        }
        updateListOfLink({listOfLinks: links})
        await updateMenuItems(addmore,personalInfo)
        let page = entityLinkNameLink[parseInt(currentLinkPos)+ 1]
        for(let link of links){
            if(page === link){
                history.push(`/resume-builder/edit/?type=${page}`)
                return;
            }
        }
        history.push(`/resume-builder/edit/?type=${entityLinkNameLink[1]}`)
        
    }

    closeMenu(){
        const {sidenav:{currentLinkPos},history} = this.props
        this.sendTrackingInfo('mobile_cancel_add_remove_menu',1)
        history.push(`/resume-builder/edit/?type=${entityLinkNameLink[parseInt(currentLinkPos)+ 1]}`)
    }

    addItem(pos) {
        let {addmore} = this.state;
        addmore[pos -1].active = true;
        this.setState({addmore})
        this.sendTrackingInfo('menu_add_section',1);
    }

    removeItem(pos) {
        let {addmore} = this.state;
        addmore[pos -1].active = false
        this.setState({addmore})
        this.sendTrackingInfo('menu_remove_section',1);
    }

    render() {
        const {addmore} = this.state;
        const {ui:{mainloader},sidenav:{currentLinkPos},history} = this.props
        return (
            <div className="addMore">
                {mainloader ? <Loader/> :""}
                <Header page={'menu'} backPage={entityLinkNameLink[parseInt(currentLinkPos)+ 1]} history={history}/>
                <p className="fs-14">Add / remove sections in your resume</p>
                <ul className="addMore__items">
                    {addmore.filter(item =>(item.active ===true && item.entity_id !== 1 && item.entity_id !==6 && item.entity_id !==11)).map((item, key) =>
                        {
                            return(
                                    <Menuitem 
            
                                        label={item.entity_text}
                                        key={key}
                                        pos={item.entity_id}
                                        iconClass={iconClassList[item.entity_id]}
                                        exist={item.active}
                                        addItem={this.addItem}
                                        removeItem={this.removeItem}
                                        deleteIconExist={delete_icon[item.entity_id]}
                                />)
                        }
                        
                    )}
                </ul>
                {addmore.filter(item =>item.active ===false).length ?
                    <ul className="addMore__items grey-bg pt-0 pb-0">
                        {addmore.filter(item =>item.active ===false && item.entity_id !==11).map((item, key) =>
                            {
                                return(
                                        <Menuitem 
                            
                                            label={item.entity_text}
                                            key={key}
                                            pos={item.entity_id}
                                            iconClass={iconClassList[item.entity_id]}
                                            exist={item.active}
                                            addItem={this.addItem}
                                            removeItem={this.removeItem}
                                            deleteIconExist={delete_icon[item.entity_id]}
                                    />)
                            }
                            
                        )}
                    </ul>:''
                }

                <div className="bottom-ctc">
                    <span className="link-color" onClick={this.closeMenu}>Cancel</span>
                    <span className="btn__primary" onClick={this.saveMenu}>Done</span>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        personalInfo : state.personalInfo,
        sidenav: state.sidenav,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "updateListOfLink": (data) => {
            return dispatch(updateListOfLink(data))
        },
        "updateMenuItems": (addmore,personalInfo) => {
            let { date_of_birth, extracurricular,image,gender} = personalInfo;
            let interest = extracurricular
            interest =  ((interest|| []).filter((item)=>item !==null).map((item)=>item.value)).join(",")
            let personalDetails = {
                ...personalInfo,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'extracurricular':interest,
                    'entity_preference_data': addmore,
                    'image' : image,
                    'gender' : gender
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        },
        "userTrack" : ( data ) => dispatch(trackUser(data)),
        
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Menu);
