import React, { Component } from 'react';
import Header from '../../../Common/Header/header';
import './menu.scss';
import { connect } from "react-redux";
import { entityLinkNameLink, iconClassList, delete_icon } from '../../../../Utils/entitydata.js'
import { updateListOfLink } from "../../../../store/sidenav/actions";
import { updatePersonalInfo } from "../../../../store/personalInfo/actions"
import Menuitem from './menuItem';
import moment from 'moment'
import Loader from '../../../Common/Loader/loader';
import { eventClicked } from '../../../../store/googleAnalytics/actions/index'
import { trackUser } from '../../../../store/tracking/actions/index';
import { isTrackingInfoAvailable, getTrackingInfo } from "../../../../Utils/common";
import propTypes from 'prop-types';

class Menu extends Component {

    constructor(props) {
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

    componentDidMount() {
        const { personalInfo: { entity_preference_data }, history } = this.props
        if (!entity_preference_data.length) {
            history.push(`/resume-builder/edit/?type=profile`)
        }
        this.setState({ addmore: entity_preference_data })
    }

    componentDidUpdate(prevProps) {
        const { personalInfo: { entity_preference_data } } = this.props

        if (entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({ addmore: entity_preference_data })
        }

    }

    sendTrackingInfo(action, pos) {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId, productId,
                triggerPoint, uId, utmCampaign } = getTrackingInfo();
            const { userTrack } = this.props;
            let { position } = getTrackingInfo() 
            if(position === ""){
                position = pos;
            }
            userTrack({
                trackingId, productTrackingMappingId, productId, action, position,
                triggerPoint, uId, utmCampaign
            });
        }
    }

    async saveMenu() {
        const { addmore } = this.state
        const { sidenav: { currentLinkPos }, updateMenuItems, personalInfo, updateListOfLink, history, eventClicked } = this.props

        eventClicked({
            'action': 'CompletedAddRemove',
            'label': 'Click'
        })

        this.sendTrackingInfo('menu_done_add_remove_menu', 1)
        let links = []
        for (let i of addmore) {
            if (i.active) {
                links.push(entityLinkNameLink[i.entity_id])
            }
        }
        updateListOfLink({ listOfLinks: links })
        await updateMenuItems(addmore, personalInfo)
        let page = entityLinkNameLink[parseInt(currentLinkPos) + 1]
        for (let link of links) {
            if (page === link) {
                history.push(`/resume-builder/edit/?type=${page}`)
                return;
            }
        }
        history.push(`/resume-builder/edit/?type=${entityLinkNameLink[1]}`)

    }

    closeMenu() {
        const { sidenav: { currentLinkPos }, history } = this.props
        this.sendTrackingInfo('menu_cancel_add_remove_menu', 1)
        history.push(`/resume-builder/edit/?type=${entityLinkNameLink[parseInt(currentLinkPos) + 1]}`)
    }

    addItem(pos) {
        let { addmore } = this.state;
        addmore[pos - 1].active = true;
        this.setState({ addmore })
        this.sendTrackingInfo('menu_add_section', 1);
    }

    removeItem(pos) {
        let { addmore } = this.state;
        addmore[pos - 1].active = false
        this.setState({ addmore })
        this.sendTrackingInfo('menu_remove_section', 1);
    }

    render() {
        const { addmore } = this.state;
        const { ui: { mainloader }, sidenav: { currentLinkPos }, history } = this.props
        return (
            <div className="addMore">
                {mainloader ? <Loader /> : ""}
                <Header page={'menu'} backPage={entityLinkNameLink[parseInt(currentLinkPos) + 1]} history={history} />
                <p className="fs-14">Add / remove sections in your resume</p>
                <ul className="addMore__items">
                    {addmore.filter(item => (item.active === true && item.entity_id !== 1 && item.entity_id !== 6 && item.entity_id !== 11)).map((item, key) => {
                        return (
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
                {addmore.filter(item => item.active === false).length ?
                    <ul className="addMore__items grey-bg pt-0 pb-0">
                        {addmore.filter(item => item.active === false && item.entity_id !== 11).map((item, key) => {
                            return (
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
                    </ul> : ''
                }

                <div className="bottom-ctc">
                    <span className="link-color" onClick={this.closeMenu}>Cancel</span>
                    <span className="btn__primary" onClick={this.saveMenu}>Done</span>
                </div>
            </div>
        )
    }
}

Menu.propTypes = {
    eventClicked: propTypes.func,
    history: propTypes.shape({
        action: propTypes.string,
        block: propTypes.func,
        createHref: propTypes.func,
        go: propTypes.func,
        goBack: propTypes.func,
        goForward: propTypes.func,
        length: propTypes.number,
        listen: propTypes.func,
        location: propTypes.shape({
            hash: propTypes.string,
            pathname: propTypes.string,
            search: propTypes.string,
            state: undefined
        }),
        push: propTypes.func,
        replace: propTypes.func,
    }),
    location: propTypes.shape({
        hash: propTypes.string,
        pathname: propTypes.string,
        search: propTypes.string,
        state: undefined
    }),
    match: propTypes.shape({
        isExact: propTypes.bool,
        params: propTypes.object,
        path: propTypes.string,
        url: propTypes.string,
    }),
    personalInfo: propTypes.shape({
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        gender: propTypes.string,
        hide_subscribe_button: propTypes.bool,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
    }),
    routes: propTypes.func,
    sidenav: propTypes.shape({
        sidenavStatus: propTypes.bool,
        listOfLinks: propTypes.array,
        currentLinkPos: propTypes.string
    }),
    staticContext: propTypes.func,
    ui: propTypes.shape({
        alertModal: propTypes.bool,
        alertType: propTypes.string,
        formName: propTypes.string,
        generateResumeModal: propTypes.bool,
        helpModal: propTypes.bool,
        loader: propTypes.bool,
        loginModal: propTypes.bool,
        modal: propTypes.bool,
        previewClicked: propTypes.bool,
        select_template_modal: propTypes.bool,
        showMoreSection: propTypes.bool,
        successLogin: propTypes.bool,
        suggestionModal: propTypes.bool,
        suggestionType: propTypes.string,
        suggestions: propTypes.array,
    }),
    updateListOfLink: propTypes.func,
    updateMenuItems: propTypes.func,
}

const mapStateToProps = (state) => {
    return {
        personalInfo: state.personalInfo,
        sidenav: state.sidenav,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "updateListOfLink": (data) => {
            return dispatch(updateListOfLink(data))
        },
        "updateMenuItems": (addmore, personalInfo) => {
            let { date_of_birth, extracurricular, image, gender } = personalInfo;
            let interest = extracurricular
            interest = ((interest || []).filter((item) => item !== null).map((item) => item.value)).join(",")
            let personalDetails = {
                ...personalInfo,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'extracurricular': interest,
                    'entity_preference_data': addmore,
                    'image': image,
                    'gender': gender
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(updatePersonalInfo({ personalDetails, resolve, reject }));
            })
        },
        'eventClicked': (data) => {
            return dispatch(eventClicked(data))
        },
        "userTrack": (data) => dispatch(trackUser(data)),

    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Menu);

