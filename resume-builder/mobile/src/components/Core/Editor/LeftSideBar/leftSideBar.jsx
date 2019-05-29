import React, {Component} from 'react';
import './leftSideBar.scss'
import * as actions from "../../../../store/sidenav/actions";
import {connect} from "react-redux";
import queryString from "query-string";
import RenderNavItem from './renderNavItem';
import * as profileActions from '../../../../store/personalInfo/actions/index';
import {entityLinkNameLink ,iconClassList,delete_icon} from '../../../../Utils/entitydata.js'
import moment from 'moment'
import Swal from 'sweetalert2'

class LeftSideBar extends Component {

    constructor(props) {
        super(props);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        this.addMore = this.addMore.bind(this);
        this.addItem = this.addItem.bind(this);
        this.removeItem = this.removeItem.bind(this);
        this.changeLink = this.changeLink.bind(this);
        this.closeSideNav = this.closeSideNav.bind(this);
        this.updateLink = this.updateLink.bind(this);
        this.showErrorMessage = this.showErrorMessage.bind(this);
        const values = queryString.parse(this.props.location.search);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.state = {
            type: (values && values.type) || '',
            addmore: [],
            current_page: '',
            loaded: false,
            sidenav_active_pos: 1
        };
        if (!(values && values.type)) {
            this.props.history.push(`/resume-builder/edit/?type=profile`)
        }
    }


    handleSpanClick(e) {
        e.stopPropagation();
    }

    addMore() {
        document.body.classList.add('sto-body-scroll')
        this.props.updateSidenavStatus(true)

    }

    changeLink(page) {
        this.setState({
            current_page: page
        })
        const {listOfLinks} = this.props.sidenav
        for (let i in listOfLinks) {
            if (page === listOfLinks[i]) {
                this.props.updateCurrentLinkPos({currentLinkPos: i})
            }
        }

    }

    addItem(pos) {
        let {addmore} = this.state;
        addmore[pos -1].active = true;
        this.setState({addmore,sidenav_active_pos:pos})
    }

    removeItem(pos) {
        let {addmore} = this.state;
        addmore[pos -1].active = false
        this.setState({addmore,sidenav_active_pos:pos})
    }

    closeSideNav() {
        this.props.updateSideNav(this.state.addmore, this.props.personalInfo)
        this.updateLink()
        this.props.updateSidenavStatus(false)
        document.body.classList.remove('sto-body-scroll')
        const {current_page, addmore} = this.state
        for (let i = 0; i < addmore.length; i++) {
            if (current_page === addmore[i].entity_link) {
                if (addmore[i].active === false) {
                    this.props.history.push(`/resume-builder/edit/?type=profile`)
                }
            }
        }
        this.setState({sidenav_active_pos:1})

    }


    componentDidMount() {
        this.props.fetchPersonalInfo()
        let current_page = this.props.location.search.split('=')[1]
        this.setState({
            current_page
        })
        this.props.fetchSideNavStatus()
        for (let i in this.props.sidenav.listOfLinks) {
            if (current_page === this.props.sidenav.listOfLinks[i]) {
                this.props.updateCurrentLinkPos({currentLinkPos: i})
            }
        }
    }

    showErrorMessage(link) {
        Swal.fire({
            title: 'Are you sure?',
            text: `Some information may be lost as required fields are not filled.`,
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, change it!'
        }).then((result) => {
            if(link === 'addMore'){
                this.addMore();
            }
            else{
                if (result.value) {
                    this.props.history.push(`/resume-builder/edit/?type=${link}`)  
                }
            }
            
        })
    }

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search);
            this.setState({
                type: (values && values.type) || ''
            })
        }
        if(this.props.sidenav.listOfLinks !== prevProps.sidenav.listOfLinks){
            let current_page = this.props.location.search.split('=')[1]
            this.setState({
                current_page
            })
            for (let i in this.props.sidenav.listOfLinks) {
                if (current_page === this.props.sidenav.listOfLinks[i]) {
                    this.props.updateCurrentLinkPos({currentLinkPos: i})
                }
            }
        }

        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data && !this.state.loaded) {
            
            this.setState({addmore: this.props.personalInfo.entity_preference_data},this.updateLink)

        }
    }

    updateLink() {
        let links = []
        for (let i of this.state.addmore) {
            if (i.active) {
                links.push(entityLinkNameLink[i.entity_id])
            }
        }
        this.props.updateListOfLink({listOfLinks: links})
    }

    render() {
        const {type, addmore, current_page,sidenav_active_pos} = this.state;
        const {sidenav:{sidenavStatus},formData,loader:{formName},personalInfo:{first_name}} = this.props
        let error = false;
        const obj = formData && formData[formName] || {};
        let syncErrors = obj['syncErrors'] || {};
        if ('fields' in obj) {
            if ('list' in syncErrors) (syncErrors && syncErrors['list'] || []).map(el => (el ? Object.keys(el) : []).map(key => (!!el[key] ? error = true : false)))
            else Object.keys(syncErrors || {}).map(key => (!!syncErrors[key] ? error = true : false));
        }
        return (
            <React.Fragment>
                {(addmore.length) ?
                    <div>
                        <div className={"overlay-sidenav"} style={sidenavStatus ? {visibility: "visible", opacity: 1} : {}}
                             onClick={this.closeSideNav}></div>

                        <section
                            className={"left-sidebar sidebar " + (sidenavStatus ? "sidebar-open" : "sidebar-close")}>

                            <div className="sidebar__menuWrap">
                                <ul className="sidebar__items">
                                    <li className="sidebar__item user">
                                    <span className="user__image">
                                        <img src={`${this.staticUrl}react/assets/images/mobile/default-user.jpg`}
                                             alt=""/>
                                    </span>
                                        <span className="user__name">Hello {first_name? first_name : 'User'}</span>
                                    </li>
                                    {addmore.filter(item =>item.active ===true).map((item, key) =>
                                        {
                                            return(<RenderNavItem label={item.entity_text}
                                                        key={key}
                                                        pos={item.entity_id}
                                                        type={type}
                                                        sidenavStatus={sidenavStatus}
                                                        title={entityLinkNameLink[item.entity_id]}
                                                        exist={item.active}
                                                        current_page={current_page}
                                                        changeLink={this.changeLink}
                                                        iconClass={iconClassList[item.entity_id]}
                                                        removeItem={this.removeItem}
                                                        addItem={this.addItem}
                                                        error={error}
                                                        sidenav_active_pos={sidenav_active_pos}
                                                        showErrorMessage={this.showErrorMessage}
                                                        deleteIconExist={delete_icon[item.entity_id]}/>)
                                        }
                                        
                                    )}
                                    {addmore.filter(item =>item.active !==true).map((item, key) =>
                                        {
                                            return(<RenderNavItem label={item.entity_text}
                                                        key={key}
                                                        pos={item.entity_id}
                                                        type={type}
                                                        sidenavStatus={sidenavStatus}
                                                        title={entityLinkNameLink[item.entity_id]}
                                                        exist={item.active}
                                                        current_page={current_page}
                                                        changeLink={this.changeLink}
                                                        iconClass={iconClassList[item.entity_id]}
                                                        removeItem={this.removeItem}
                                                        sidenav_active_pos={sidenav_active_pos}
                                                        addItem={this.addItem}
                                                        deleteIconExist={delete_icon[item.entity_id]}/>)
                                        }
                                        
                                    )}

                                    <li className={"sidebar__item " + (sidenavStatus ? "hide" : "")}>
                                        <a href="#" className="sidebar__anchor">
                                            <div className="sidebar__wrap">
                                                <i className="sprite icon--add-more"></i>
                                                <span className="sidebar__link" onClick={!error ?this.addMore:this.showErrorMessage.bind(this,'addMore')}>Add more</span>
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
                    </div> : ""
                }
            </React.Fragment>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.sidenav,
        sidenav: state.sidenav,
        formData: state && state.form,
        loader: state && state.loader
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
        "updateSideNav": (addmore,personalInfo) => {
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
                dispatch(profileActions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LeftSideBar);