import React, {Component} from 'react';
import './leftSideBar.scss'
import * as actions from "../../../../store/sidenav/actions";
import {connect} from "react-redux";
import queryString from "query-string";
import RenderNavItem from './renderNavItem';
import {entityLinkNameLink, iconClassList} from '../../../../Utils/entitydata.js'
import AlertModal from '../../../Common/AlertModal/alertModal';
import {formCategoryList} from '../../../../Utils/formCategoryList'


const isSame = (initialField, formField) => {
    let isSame = true;
    if (initialField instanceof Array && formField instanceof Array) {
        (initialField || []).map((el, index) => (initialField[index] === formField[index] ? true : isSame = false))
        return isSame;
    }
    if (initialField === formField) return true;
    return false;

}

class LeftSideBar extends Component {

    constructor(props) {
        super(props);
        this.handleSpanClick = this.handleSpanClick.bind(this);
        this.changeLink = this.changeLink.bind(this);
        this.updateLink = this.updateLink.bind(this);
        this.openMenu = this.openMenu.bind(this);
        this.showErrorMessage = this.showErrorMessage.bind(this);
        this.closeModal = this.closeModal.bind(this);
        const values = queryString.parse(this.props.location.search);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.state = {
            type: (values && values.type) || '',
            addmore: [],
            modal_status: false,
            link: ''
        };
        if (!(values && values.type)) {
            this.props.history.push(`/resume-builder/edit/?type=profile`)
        }
    }


    handleSpanClick(e) {
        e.stopPropagation();
    }

    changeLink(page, pos) {
        const {sidenav: {listOfLinks}, updateCurrentLinkPos, eventClicked, sendTrackingInfo} = this.props
        sendTrackingInfo('mobile_left_edit_change_section',1)
        for (let i in listOfLinks) {
            if (page === listOfLinks[i]) {
                updateCurrentLinkPos({currentLinkPos: i})
            }
        }
        eventClicked({
            'action': 'SelectSection',
            'label': formCategoryList[pos].name
        })

    }


    componentDidMount() {
        const {fetchPersonalInfo, fetchSideNavStatus, location: {search}, sidenav: {listOfLinks}, updateCurrentLinkPos, fetchAlertModalStatus} = this.props;
        fetchPersonalInfo()
        fetchAlertModalStatus()
        let current_page = search.split('=')[1]
        fetchSideNavStatus()
        for (let i in listOfLinks) {
            if (current_page === listOfLinks[i]) {
                updateCurrentLinkPos({currentLinkPos: i})
            }
        }
    }

    closeModal() {
        this.props.updateAlertModalStatus(false)
        this.setState({link: ''})
    }

    showErrorMessage(link) {
        this.props.updateAlertModalStatus(true)
        this.setState({link})
    }

    componentDidUpdate(prevProps) {
        const {location, sidenav: {listOfLinks}, updateCurrentLinkPos, personalInfo: {entity_preference_data}} = this.props
        if (location !== prevProps.location) {
            const values = queryString.parse(location.search);
            this.setState({
                type: (values && values.type) || ''
            })
        }
        if (entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.updateLink(entity_preference_data)
        }
        if (listOfLinks !== prevProps.sidenav.listOfLinks) {
            let current_page = location.search.split('=')[1]
            for (let i in listOfLinks) {
                if (current_page === listOfLinks[i]) {
                    updateCurrentLinkPos({currentLinkPos: i})
                }
            }
        }
    }

    openMenu() {
        this.props.sendTrackingInfo('mobile_left_section_add_or_remove',1);
        const {history, eventClicked} = this.props
        history.push(`/resume-builder/menu`)
        eventClicked({
            'action': 'Add/Remove',
            'label': 'Click'
        })
    }

    updateLink(entity_preference_data) {
        let links = []
        for (let i of entity_preference_data) {
            if (i.active) {
                links.push(entityLinkNameLink[i.entity_id])
            }
        }
        this.props.updateListOfLink({listOfLinks: links})
    }

    render() {
        const {type, sidenav_active_pos, link} = this.state;
        const {formData, ui: {formName, alertModalStatus, generateResumeModal}, personalInfo: {first_name, entity_preference_data}, history, updateAlertModalStatus, eventClicked} = this.props
        let error = [], filled = [], isError = false, isFilled = false;
        const obj = formData && formData[formName] || {};
        let syncErrors = obj['syncErrors'] || {};
        let values = obj['values'] || {};
        let initial = obj['initial'] || {};
        const newUser = localStorage.getItem('newUser')
        if ('fields' in obj) {
            if ('list' in syncErrors) ((syncErrors && syncErrors['list']) || []).map((el, ind) => {
                error[ind] = false;
                return (el ? Object.values(el)
                    : []).map(value => (!!value ? error[ind] = true : false))
            });
            else {
                error[0] = false;
                Object.values(syncErrors || {}).map(value => (!!value ? error[0] = true : false));
            }
            if ('list' in initial) {
                initial = initial && initial['list'][0]
            }
            if ('list' in values) ((values && values['list'] || [])).map((el, index) => {
                    filled[index] = false;
                    return (el ? Object.keys(el) : []).map(
                        key => (isSame(initial[key], el[key]) ? false : filled[index] = true)
                    )
                }
            )
            else {
                filled[0] = false;
                Object.keys(values || {}).map(key => (isSame(initial[key], values[key]) ? false : filled[0] = true))
            }

            // Currently only feasible for single item in any list
            for (let ind = 0; ind < error.length; ind++) {
                if (error[ind] && filled[ind]) {
                    isError = true;
                    isFilled = true;
                    break;
                }
            }
        }

        return (
            <React.Fragment>
                <AlertModal modal_status={alertModalStatus || generateResumeModal}
                            generateResumeModal={generateResumeModal} link={link} history={history} newUser={newUser}
                            closeModal={this.closeModal}/>
                {(entity_preference_data.length) ?
                    <div>
                        <div className={"overlay-sidenav"}></div>

                        <section
                            className={"left-sidebar sidebar sidebar-close"}>

                            <div className="sidebar__menuWrap">
                                <ul className="sidebar__items">
                                    <li className="sidebar__item user">
                                    <span className="user__image">
                                        <img src={`${this.staticUrl}react/assets/images/mobile/default-user.jpg`}
                                             alt=""/>
                                    </span>
                                        <span className="user__name">Hello {first_name ? first_name : 'User'}</span>
                                    </li>
                                    {entity_preference_data.filter(item => item.active === true).map((item, key) => {
                                            return (<RenderNavItem label={item.entity_text}
                                                                   key={key}
                                                                   newUser={newUser}
                                                                   pos={item.entity_id}
                                                                   type={type}
                                                                   title={entityLinkNameLink[item.entity_id]}
                                                                   exist={item.active}
                                                                   changeLink={this.changeLink}
                                                                   iconClass={iconClassList[item.entity_id]}
                                                                   error={isError}
                                                                   filled={isFilled}
                                                                   sidenav_active_pos={sidenav_active_pos}
                                                                   showErrorMessage={this.showErrorMessage}
                                            />)
                                        }
                                    )}

                                    <li className={"sidebar__item add-reamove"}>
                                        <a className="sidebar__anchor" onClick={newUser ? () => {
                                            updateAlertModalStatus(true)
                                        } : this.openMenu}>
                                            <div className="sidebar__wrap">
                                                <i className="sprite icon--add-remove"></i>
                                                <span className="sidebar__link">Add/<br/>Remove</span>
                                            </div>
                                        </a>
                                    </li>
                                </ul>
                            </div>
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
        ui: state && state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchSideNavStatus": () => {
            return dispatch(actions.fetchSideNavStatus())
        },
        "updateCurrentLinkPos": (data) => {
            return dispatch(actions.updateCurrentLinkPos(data))
        },
        "updateListOfLink": (data) => {
            return dispatch(actions.updateListOfLink(data))
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(LeftSideBar);