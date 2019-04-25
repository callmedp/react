import React, {Component} from 'react';
import './leftSideBar.scss'
import * as actions from "../../../../store/sidenav/actions";
import * as profileActions from '../../../../store/personalInfo/actions/index';
import {connect} from "react-redux";
import queryString from "query-string";
import { Link} from 'react-router-dom';
import RenderNavItem from './renderNavItem';
class LeftSideBar extends Component {

    constructor(props) {
        super(props);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        this.addMore = this.addMore.bind(this);
        this.addItem = this.addItem.bind(this);
        this.removeItem = this.removeItem.bind(this);
        this.changeLink = this.changeLink.bind(this);
        this.closeSideNav = this.closeSideNav.bind(this);
        this.updateLink =this.updateLink.bind(this);
        const values = queryString.parse(this.props.location.search);

        this.state = {
            type: (values && values.type) || '',
            addmore:[],
            current_page: '',
            loaded:false
        };
        if (!(values && values.type)) {
            this.props.history.push(`/resume-builder/edit/?type=profile`)
        }
    }


    handleSpanClick(e) {
        e.stopPropagation();
    }

    addMore(){
        document.body.classList.add('sto-body-scroll')
        this.props.updateSidenavStatus(true)

    }

    changeLink(page){
        ////console.log(page)
        this.setState({
            current_page : page
        })
        const {listOfLinks} = this.props.sidenav
        //console.log(listOfLinks)
        for(let i in listOfLinks){
            if (page === listOfLinks[i]){
                this.props.updateCurrentLinkPos({currentLinkPos: i})
                ////console.log("Change pos")
            }
        }

    }

    addItem(item){
        let addmore = {...this.state.addmore};
        addmore[item].active =true
        const addmore_sorted = [].concat(this.state.addmore).sort((a,b)=>b.active -a.active )
        this.setState({addmore:addmore_sorted})
    }

    removeItem(item){
        let addmore = {...this.state.addmore};
        addmore[item].active = false
        const addmore_sorted = [].concat(this.state.addmore).sort((a,b)=>b.active -a.active )
        this.setState({addmore:addmore_sorted})
    }

    closeSideNav(){
        this.props.onSubmit(this.state.addmore,this.props.personalInfo)
        this.updateLink()
        this.props.updateSidenavStatus(false)
        document.body.classList.remove('sto-body-scroll')
        const {current_page,addmore} =this.state
        for(let i=0;i<addmore.length;i++){
            if(current_page === addmore[i].entity_link){
                if(addmore[i].active === false){
                    this.props.history.push(`/resume-builder/edit/?type=profile`)
                }
            }
        }

    }

    componentDidMount() {
        ////console.log("mount")
        this.props.fetchPersonalInfo()
        let current_page = this.props.location.search.split('=')[1]
        this.setState({
            current_page
        })
        this.props.fetchSideNavStatus()
        let found_link =false
        for(let i in this.props.sidenav.listOfLinks){
            if (current_page === this.props.sidenav.listOfLinks[i]){
                found_link = true
                this.props.updateCurrentLinkPos({currentLinkPos: i})
            }
        }
        if(!found_link){
            this.props.history.push(`/resume-builder/edit/?type=${this.props.sidenav.listOfLinks[0]}`)
            this.props.updateCurrentLinkPos({currentLinkPos: 0})
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search);
            this.setState({
                type: (values && values.type) || ''
            })
        }
        if (this.props.personalInfo.entity_preference_data != prevProps.personalInfo.entity_preference_data && !this.state.loaded){

            this.setState({addmore:this.props.personalInfo.entity_preference_data,loaded:true},this.updateLink)
            //console.log("UpdateMount here")
            
        }
        // this.updateLink()


    }

    updateLink(){
        //console.log("came here")
        let links = []
        for(let i of this.state.addmore){
            if(i.active){
                links.push(i.entity_link)
                ////console.log(i.entity_link)
            }
        }
        this.props.updateListOfLink({listOfLinks:links})
        ////console.log("I am here")
    }

    render() {
        const {type,addmore,current_page} = this.state;
        const {sidenavStatus} = this.props.sidenav
        
        return (
            <React.Fragment>
            { (addmore.length) ?
                <div>
                    <div className={"overlay"} style={sidenavStatus ? {visibility : "visible",opacity : 1} : {}}
                        onClick={this.closeSideNav}></div>
                    
                    <section className={"left-sidebar sidebar " + (sidenavStatus ? "sidebar-open" : "sidebar-close")}>
                        
                        <div className="sidebar__menuWrap">
                            <ul className="sidebar__items">
                                <li className="sidebar__item user">
                                    <span className="user__image">
                                        <img src="/media/static/react/assets/images/mobile/default-user.jpg" alt="" />
                                    </span>
                                    <span className="user__name">Hello Amit</span>
                                </li>
                                {addmore.map((item, key) =>
                                
                                    <RenderNavItem label={item.entity_text}
                                                    key={key}
                                                    pos={key}
                                                    type={type}
                                                    sidenavStatus={sidenavStatus}
                                                    title={item.entity_link}
                                                    exist={item.active}
                                                    current_page={current_page}
                                                    changeLink={this.changeLink}
                                                    iconClass={item.icon_class}
                                                    removeItem={this.removeItem}
                                                    addItem={this.addItem}
                                                    deleteIconExist={item.delete_icon}/>
                                )}
                                
                                <li className={"sidebar__item " + (sidenavStatus ? "hide" : "")}>
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
                </div>:""
            }
            </React.Fragment>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        sidenav: state.sidenav,
        personalInfo: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchSideNavStatus": () => {
            return dispatch(actions.fetchSideNavStatus())
        },
        "updateSidenavStatus": (status) => {
            return dispatch(actions.updateSidenavStatus(status))
        },
        "fetchListOfLink": () => {
            return dispatch(actions.fetchListOfLink())
        },
        "updateListOfLink": (data) => {
            return dispatch(actions.updateListOfLink(data))
        },
        "updateCurrentLinkPos": (data) => {
            return dispatch(actions.updateCurrentLinkPos(data))
        },
        "fetchPersonalInfo": () => {
            return dispatch(profileActions.fetchPersonalInfo())
        },
        "onSubmit": (entity_data,personalInfo) => {
            let personalDetails={
                ...personalInfo,
                ...{
                    'entity_preference_data':entity_data,
                    'extracurricular':''
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(profileActions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LeftSideBar);