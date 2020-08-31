import React, { Component } from 'react';
import Header from '../../../Common/Header/header.jsx';
import './preview.scss';
import { connect } from "react-redux";
import { fetchTemplate, updateModalStatus, customizeTemplate, fetchDefaultCustomization, reorderSection, reGeneratePDF, } from "../../../../store/template/actions/index"
import { updatePersonalInfo, fetchPersonalInfo, getChatBotUrl } from "../../../../store/personalInfo/actions/index"
import { updateAlertModalStatus, showGenerateResumeModal, hideGenerateResumeModal } from "../../../../store/ui/actions/index"
import Loader from '../../../Common/Loader/loader.jsx';
import ChangeTemplateModal from './changeTemplateModal.jsx';
import { loginCandidate } from '../../../../store/landingPage/actions/index';
import { trackUser } from '../../../../store/tracking/actions/index';
import moment from 'moment'
import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";
import InputRange from 'react-input-range';
import Swal from 'sweetalert2'
import { siteDomain } from "../../../../Utils/domains";
import AlertModal from '../../../Common/AlertModal/alertModal.jsx';
import { eventClicked } from '../../../../store/googleAnalytics/actions/index'
import { formCategoryList } from '../../../../Utils/formCategoryList'
// import * as lscache from '../../../../../node_modules/lscache/lscache';
import { Helmet } from "react-helmet";
import propTypes from 'prop-types';
import { getTrackingInfo, isTrackingInfoAvailable } from '../../../../Utils/common';

class Preview extends Component {

    constructor(props) {
        super(props)
        // check if the userexperinece is greater or equal to 4 years. (7 is the pid for 4 years (mapping done here))
        this.state = {
            'customize': false,
            currentTab: 1,
            selectedColor: 1,
            headingFontSize: 1,
            textFontSize: 1,
            activeSection: 'left',
            sectionEntityName: '',
            selectedEntity: '',
            startingReorderUpDowmIndex: 0,
            zoomIn: false
        }
        this.handleCustomization = this.handleCustomization.bind(this);
        this.selectSection = this.selectSection.bind(this);
        this.moveUpSection = this.moveUpSection.bind(this);
        this.moveDownSection = this.moveDownSection.bind(this);
        this.handleActiveSection = this.handleActiveSection.bind(this);
        this.handleZoomTemplate = this.handleZoomTemplate.bind(this);
        this.showReorderErrorToast = this.showReorderErrorToast.bind(this);
        this.getResume = this.getResume.bind(this);
        this.themeChange = this.themeChange.bind(this);
        this.fontChange = this.fontChange.bind(this);
        this.toggleUploadResume = this.toggleUploadResume.bind(this);
        this.customizeTemplate = this.customizeTemplate.bind(this);
        this.selectTab = this.selectTab.bind(this);
        this.sendTrackingInfo = this.sendTrackingInfo.bind(this);
    }

    componentWillUpdate(prevProps) {
        const { template } = this.props

        if (template !== prevProps.template) {

            this.setState({
                selectedColor: template.color,
                headingFontSize: template.heading_font_size - 1,
                textFontSize: template.text_font_size - 1
            })
        }
    }

    async componentDidUpdate(prevProps) {
        const { template: { entity_position, reorderFailToast }, personalInfo: { selected_template }, loginCandidate } = this.props;
        if (!localStorage.getItem('candidateId') || !localStorage.getItem('token')) {
            await loginCandidate()
        }
        const { selectedEntity } = this.state
        if (entity_position !== prevProps.template.entity_position) {
            (entity_position && eval(entity_position) || []).map((el) => {
                if (selectedEntity && selectedEntity['entity_id'] === el.entity_id) {
                    this.setState({ selectedEntity: el })
                }
            })
        }
        if (selected_template !== prevProps.personalInfo.selected_template) {
            this.props.fetchTemplate();
            this.props.fetchDefaultCustomization(selected_template);
        }
        if (reorderFailToast !== prevProps.template.reorderFailToast) {
            this.showReorderErrorToast()
        }
    }


    toggleUploadResume(event) {
        let { personalInfo: { upload_resume: uploadResume }, personalInfo, updateSelectedTemplate } = this.props;
        this.sendTrackingInfo('preview_update_resume_on_shine', 1)
        personalInfo['upload_resume'] = !uploadResume;
        updateSelectedTemplate(personalInfo);
    }

    showReorderErrorToast() {
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        });

        Toast.fire({
            type: 'error',
            title: 'Sorry, this section cannot be moved.'
        })
    }


    async componentDidMount() {

        if (parseInt(localStorage.getItem('userExperience') || 0) >= 7) {
            if (document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) {
                document.getElementsByClassName('chat-bot')[0].style.display = 'none';
            }
        }
        else {
            if (document.getElementsByClassName('chat-bot') && document.getElementsByClassName('chat-bot')[0]) {
                document.getElementsByClassName('chat-bot')[0].style.display = 'block';
            }
        }
        await this.props.fetchPersonalInfo();
        // await this.props.getChatBotUrl();
        this.props.fetchTemplate();
        const { personalInfo: { selected_template } } = this.props
        this.props.fetchDefaultCustomization(selected_template || 1);
    }

    selectSection(section) {

        this.setState({
            sectionEntityName: section['entity_text'],
            selectedEntity: section,
            startingReorderUpDowmIndex: -1
        })

    }

    themeChange(colorNo, colorName) {
        this.setState({ selectedColor: colorNo })
        this.sendTrackingInfo('preview_change_theme', 1)
        this.props.eventClicked({
            'action': 'ChangeTheme',
            'label': colorName
        })
    }

    fontChange(fontSize, isHeadingFontSize) {
        isHeadingFontSize ? this.setState({ headingFontSize: fontSize }) : this.setState({ textFontSize: fontSize })
        this.props.eventClicked({
            'action': 'ChangeFont',
            'label': fontSize === 0 ? 'S' : fontSize === 1 ? 'M' : 'L'
        })
    }

    handleActiveSection(section) {
        this.setState({
            activeSection: section,
            startingReorderUpDowmIndex: 0,
            sectionEntityName: ''
        })
    }

    handleZoomTemplate() {
        const { zoomIn } = this.state;
        zoomIn ? this.setState({ zoomIn: false }) : this.setState({ zoomIn: true })
    }

    moveUpSection(selectedEntity, selectedTemplate) {
        const { eventClicked, reorderSection } = this.props;
        this.sendTrackingInfo('preview_reorder_section', 1);

        eventClicked({
            'action': 'ReorderSection',
            'label': formCategoryList[selectedEntity['entity_id']].name
        })
        reorderSection({
            templateId: selectedTemplate,
            info: { entity_id: selectedEntity['entity_id'], step: -1, pos: selectedEntity['pos'] }
        })
    }

    moveDownSection(selectedEntity, selectedTemplate) {
        const { eventClicked, reorderSection } = this.props;
        this.sendTrackingInfo('preview_reorder_section', 1);

        eventClicked({
            'action': 'ReorderSection',
            'label': formCategoryList[selectedEntity['entity_id']].name
        })
        reorderSection({
            templateId: selectedTemplate,
            info: { entity_id: selectedEntity['entity_id'], step: 1, pos: selectedEntity['pos'] }
        })
    }

    getResume() {
        const { personalInfo: { order_data, resume_generated }, history, reGeneratePDF, showGenerateResumeModal, hideGenerateResumeModal, eventClicked } = this.props;
        this.sendTrackingInfo('get_your_resume', 1);
        eventClicked({
            'action': 'GetYourResume',
            'label': 'Click'
        })
        if (order_data && order_data.id && (localStorage.getItem('subscriptionActive') && localStorage.getItem('subscriptionActive') === 'true' ? true : false)) {
            if (!resume_generated) {
                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-success btn__round btn--outline mt-10',
                        cancelButton: 'btn btn-danger btn__round btn--outline mt-10'
                    },
                    buttonsStyling: false
                })

                swalWithBootstrapButtons.fire({
                    title: 'Are you sure?',
                    text: "You won't be able to change your template again.",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Yes, generate resume!',
                    cancelButtonText: 'No, cancel!',
                    reverseButtons: true
                }).then((result) => {
                    if (result.value) {
                        showGenerateResumeModal()
                        reGeneratePDF(order_data.id)
                        setTimeout(function () {
                            window.location.href = `${siteDomain}/dashboard`
                            hideGenerateResumeModal()
                        }, 5000);
                    }
                })
            }
            else {
                showGenerateResumeModal()
                reGeneratePDF(order_data.id)
                setTimeout(function () {
                    window.location.href = `${siteDomain}/dashboard`
                    hideGenerateResumeModal()
                }, 5000);
            }
        }
        else {
            history.push(`/resume-builder/buy`)
        }
    }

    sendTrackingInfo(action, pos) {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId, productId,
                triggerPoint, uId, position, utmCampaign } = getTrackingInfo();
            const { userTrack } = this.props;
            userTrack({
                trackingId, productTrackingMappingId, productId, action, position,
                triggerPoint, uId, utmCampaign
            });
        }
    }


    async handleCustomization(data) {
        await this.props.customizeTemplate(data)
        this.props.fetchTemplate();
        this.setState({ customize: false, currentTab: 1 })
    }
    customizeTemplate() {
        this.setState({ customize: true })
        this.sendTrackingInfo('preview_customize_template', 1);
    }

    selectTab(tabNo) {
        this.setState({ currentTab: tabNo })
        this.sendTrackingInfo('preview_tab_selected', 1);
    }


    render() {
        const { customize, currentTab, selectedColor, headingFontSize, textFontSize, sectionEntityName, startingReorderUpDowmIndex, zoomIn } = this.state
        const { template: { html, zoomInHtml, entity_position, entity_id_count_mapping }, ui: { mainloader, alertModalStatus, generateResumeModal }, personalInfo: { selected_template, order_data, resume_generated, upload_resume: uploadResume }, history, eventClicked } = this.props
        return (
            <div className="preview">
                <Helmet
                    script={[
                        { "src": (localStorage.getItem('script_link') ? localStorage.getItem('script_link') : null), "type": "text/javascript" }
                    ]}
                />
                <Header page={'preview'} {...this.props} order_data={order_data} eventClicked={eventClicked} />
                <AlertModal modal_status={alertModalStatus || generateResumeModal} history={history} generateResumeModal={generateResumeModal} />

                {
                    (!(order_data && order_data.id) || !(resume_generated)) ?
                        <ChangeTemplateModal {...this.props} /> :
                        (order_data && order_data.id && order_data.combo) ? <ChangeTemplateModal {...this.props} /> :
                            (order_data && order_data.id && order_data.expiry) ? <ChangeTemplateModal {...this.props} /> : ''
                }

                {mainloader ? <Loader /> : ""}

                <div className="toss-widget">
                    <div className="checkbox-wrap">
                        <input type="checkbox" name="update" id="update" onClick={this.toggleUploadResume} defaultChecked={uploadResume} />
                        <label htmlFor="update">
                            Update resume on shine profile
            </label>
                    </div>
                </div>

                <div className="iframe__wrap">
                    <span className="sprite icon--zoom" onClick={this.handleZoomTemplate}></span>
                    {zoomIn ?
                        <iframe srcDoc={zoomInHtml} className={"iframe-new"}></iframe> :
                        <iframe srcDoc={html} className={"iframe-new"}></iframe>
                    }
                </div>

                <div className="preview__bottom-btns pos-fixed">
                    <span className="btn btn__round btn--outline" onClick={() => { this.setState({ customize: true }) }}>Customize template</span>
                    <span className="btn btn__round btn__primary" onClick={this.getResume}>Get your resume</span>
                </div>

                {customize ?
                    <div className="filter">
                        <div className="filter__overlay"></div>
                        <div className="filter__wrap">

                            <div className="filter__accordion">
                                <h2 className="filter__wrap--heading">Customize template</h2>
                                <Accordion preExpanded={["1"]}>
                                    <AccordionItem uuid="1">
                                        <div className={"filter__accordion__card " + (currentTab === 1 ? "filter__accordion--active" : "")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                    <div className="filter__accordion__card__heading" onClick={() => this.selectTab(1)}>
                                                        <div className="filter__accordion__card__heading--left">
                                                            <i className="sprite icon--theme mr-10"></i>
                                                            <span>Change theme</span>
                                                        </div>

                                                        <div className="filter__accordion__card__heading--right">
                                                            <i className={"sprite " + (currentTab === 1 ? "icon--minus" : "icon--plus")}></i>
                                                        </div>
                                                    </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
                                                <div className="filter__accordion__card--content">
                                                    <ul className="resume-color-theme">
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="green" value="green"
                                                                onClick={() => { this.themeChange(1, 'Green') }}
                                                                checked={selectedColor === 1} readOnly />
                                                            <label htmlFor="green" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--green"></span>
                                                            </label>
                                                        </li>

                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="blue" value="blue"
                                                                onClick={() => { this.themeChange(2, 'Blue') }}
                                                                checked={selectedColor === 2} readOnly />
                                                            <label htmlFor="blue" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--blue"></span>
                                                            </label>
                                                        </li>

                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="red" value="red"
                                                                onClick={() => { this.themeChange(3, 'Red') }}
                                                                checked={selectedColor === 3} readOnly />
                                                            <label htmlFor="red" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--red"></span>
                                                            </label>
                                                        </li>

                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="black" value="black"
                                                                onClick={() => { this.themeChange(4, 'Black') }}
                                                                checked={selectedColor === 4} readOnly />
                                                            <label htmlFor="black" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--black"></span>
                                                            </label>
                                                        </li>

                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="brown" value="brown"
                                                                onClick={() => { this.themeChange(5, 'Brown') }}
                                                                checked={selectedColor === 5} readOnly />
                                                            <label htmlFor="brown" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--brown"></span>
                                                            </label>
                                                        </li>

                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="violet" value="violet"
                                                                onClick={() => { this.themeChange(6, 'Violet') }}
                                                                checked={selectedColor === 6} readOnly />
                                                            <label htmlFor="violet" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--violet"></span>
                                                            </label>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </AccordionItemPanel>
                                        </div>
                                    </AccordionItem>
                                    <AccordionItem >
                                        <div className={"filter__accordion__card " + (currentTab === 2 ? "filter__accordion--active" : "")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                    <div className="filter__accordion__card__heading" onClick={() => this.selectTab(2)}>
                                                        <div className="filter__accordion__card__heading--left">
                                                            <i className="sprite icon--font mr-10"></i>
                                                            <span>Font size</span>
                                                        </div>

                                                        <div className="filter__accordion__card__heading--right">
                                                            <i className={"sprite " + (currentTab === 2 ? "icon--minus" : "icon--plus")}></i>
                                                        </div>
                                                    </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
                                                <div className="filter__accordion__card--content">
                                                    <div className="font-filter">
                                                        {/* <h3>Section Heading</h3>
                    <div className="font-filter__slide-bar">
                    <span className="font-filter__dot"></span>
                    <span className="font-filter--small mt-10 fs-12">S</span>
                    <span className="font-filter--medium mt-10 fs-12">M</span>
                    <span className="font-filter--large mt-10 fs-12">L</span>
                </div> */}
                                                        <h3>Section Heading</h3>
                                                        <InputRange
                                                            name="heading_font_size"
                                                            maxValue={2}
                                                            minValue={0}
                                                            value={headingFontSize}
                                                            onChange={value => this.fontChange(value, true)} />
                                                        <div className="heading-size">
                                                            <div className="heading-size-item">S</div>
                                                            <div className="heading-size-item">M</div>
                                                            <div>L</div>
                                                        </div>
                                                        <h3>Section Text</h3>
                                                        <InputRange
                                                            name="text_font_size"
                                                            maxValue={2}
                                                            minValue={0}
                                                            value={textFontSize}
                                                            onChange={value => this.fontChange(value, false)} />
                                                        <div className="heading-size">
                                                            <div className="heading-size-item">S</div>
                                                            <div className="heading-size-item">M</div>
                                                            <div>L</div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </AccordionItemPanel>
                                        </div>
                                    </AccordionItem>
                                    <AccordionItem >
                                        <div className={"filter__accordion__card " + (currentTab === 3 ? "filter__accordion--active" : "")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                    <div className="filter__accordion__card__heading" onClick={() => this.selectTab(3)}>
                                                        <div className="filter__accordion__card__heading--left">
                                                            <i className="sprite icon--reorder mr-10"></i>
                                                            <span>Reorder section</span>
                                                        </div>

                                                        <div className="filter__accordion__card__heading--right">
                                                            <i className={"sprite " + (currentTab === 3 ? "icon--minus" : "icon--plus")}></i>
                                                        </div>
                                                    </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
                                                <div className="filter__accordion__card--content">

                                                    {/* <ul className="tabs">
                <li className={activeSection ==='left' ? "active":""} 
                onClick={() => this.handleActiveSection('left')}>Left</li>
                <li className={activeSection ==='right' ? "active":""}
                onClick={() => this.handleActiveSection('right')}>Right</li>
            </ul> */}
                                                    <div className="reorder">
                                                        <ul className="reorder__items">
                                                            {entity_position.filter(item =>
                                                                (item.entity_id !== 1 && item.entity_id !== 6)
                                                                && (item['active']) && entity_id_count_mapping[item['entity_id']]).map((el, index, arr) => {
                                                                    return (
                                                                        <li key={index} className={"reorder__item " + ((el['entity_text'] === sectionEntityName || startingReorderUpDowmIndex === index) ? " reorder--select" : "")}
                                                                            onClick={() => this.selectSection(el)} >
                                                                            <span className="reorder__title">{el.entity_text}</span>
                                                                            <div className="reorder__nav">
                                                                                {index !== 0 ?
                                                                                    <span className="reorder__nav--item">
                                                                                        <i className="sprite icon--upArrow" onClick={() => { this.moveUpSection(el, selected_template); }}></i>
                                                                                    </span> : ''
                                                                                }
                                                                                {index + 1 !== arr.length ?
                                                                                    <span className="reorder__nav--item">
                                                                                        <i className="sprite icon--downArrow" onClick={() => { this.moveDownSection(el, selected_template); }}></i>
                                                                                    </span> : ''
                                                                                }
                                                                            </div>
                                                                        </li>
                                                                    )

                                                                })}
                                                        </ul>
                                                    </div>



                                                </div>
                                            </AccordionItemPanel>
                                        </div>
                                    </AccordionItem>
                                </Accordion>
                            </div>

                            <div className="filter__apply-btn">
                                <span className="btn" onClick={() => { this.setState({ customize: false, currentTab: 1 }) }}>Cancel</span>
                                <span className="btn btn__round btn--outline"
                                    onClick={() => this.handleCustomization({
                                        color: selectedColor,
                                        template: selected_template,
                                        heading_font_size: headingFontSize + 1,
                                        text_font_size: textFontSize + 1
                                    })} >Apply</span>
                            </div>
                        </div>
                    </div>
                    : ''
                }
            </div>


        )
    }

}

Preview.propTypes = {
    allinfo: propTypes.object,
    customizeTemplate: propTypes.func,
    eventClicked: propTypes.func,
    fetchDefaultCustomization: propTypes.func,
    fetchPersonalInfo: propTypes.func,
    fetchTemplate: propTypes.func,
    getChatBot: propTypes.func,
    hideGenerateResumeModal: propTypes.func,
    location: propTypes.shape({
        hash: propTypes.string,
        pathname: propTypes.string,
        search: propTypes.string,
        state: undefined
    }),
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
    loginCandidate: propTypes.func,
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
    reGeneratePDF: propTypes.func,
    reorderSection: propTypes.func,
    routes: propTypes.func,
    showGenerateResumeModal: propTypes.func,
    staticContext: propTypes.func,
    template: propTypes.shape({
        color: propTypes.number,
        entity_position: propTypes.array,
        heading_font_size: propTypes.number,
        html: propTypes.string,
        modal_status: propTypes.bool,
        reorderFailToast: propTypes.bool,
        templateImage: propTypes.string,
        text_font_size: propTypes.number,
        thumbnailImages: propTypes.array,
        zoomInHtml: propTypes.string,
    }),
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
    updateAlertModalStatus: propTypes.func,
    updateModalStatus: propTypes.func,
    updateSelectedTemplate: propTypes.func,
}

const mapStateToProps = (state) => {
    return {
        template: state.template,
        ui: state.ui,
        personalInfo: state.personalInfo,
        allinfo: state
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchTemplate": () => {
            return dispatch(fetchTemplate())
        },
        "getChatBot": () => {
            return new Promise((resolve, reject) => {
                return dispatch(getChatBotUrl())
            })
        },
        'reGeneratePDF': (data) => {
            return dispatch(reGeneratePDF(data))
        },
        "updateModalStatus": (data) => {
            return dispatch(updateModalStatus(data))
        },
        "fetchPersonalInfo": (data) => {
            return dispatch(fetchPersonalInfo(data))
        },
        "customizeTemplate": (template_data) => {
            return new Promise((resolve, reject) => {
                return dispatch(customizeTemplate({ template_data, resolve, reject }))
            })
        },
        "fetchDefaultCustomization": (templateId) => {
            return dispatch(fetchDefaultCustomization(templateId))
        },
        "reorderSection": (data) => {
            return dispatch(reorderSection(data))
        },
        "updateAlertModalStatus": (data) => {
            return dispatch(updateAlertModalStatus(data))
        },
        'showGenerateResumeModal': () => {
            return dispatch(showGenerateResumeModal())
        },
        'hideGenerateResumeModal': () => {
            return dispatch(hideGenerateResumeModal())
        },
        "updateSelectedTemplate": (personalInfo) => {
            let { date_of_birth, extracurricular, image, gender } = personalInfo;
            let interest = extracurricular
            interest = ((interest || []).filter((item) => item !== null).map((item) => item.value)).join(",")
            let personalDetails = {
                ...personalInfo,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'extracurricular': interest,
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
        "loginCandidate": (token) => {
            return new Promise((resolve, reject) => {
                dispatch(loginCandidate({ payload: { alt: token }, resolve, reject, isTokenAvail: false }))
            })
        },
        "userTrack": (data) => dispatch(trackUser(data)),
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Preview);