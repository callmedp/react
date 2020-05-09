import React, { Component, Fragment } from 'react';
import './resumeSlider.scss'
import Slider from "react-slick";
import TemplateModal from "../../../Modal/tempateModal";
import LoginModal from "../../../Modal/loginModal";
import queryString from "query-string";


export default class ResumeSlider extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.selectTemplate = this.selectTemplate.bind(this);
        this.showZoomedImage = this.showZoomedImage.bind(this);
        this.handleSelectTemplate = this.handleSelectTemplate.bind(this);
    }

    handleSelectTemplate(templateId, ui, hideSelectTemplateModal, page, fetchDefaultCustomization, updateSelectedTemplate, fetchSelectedTemplateImage, pathFrom, userInfo, history) {
        localStorage.setItem('selected_template', (templateId));
        const selectTemplateModal = ui ? ui.select_template_modal : false
        if (selectTemplateModal) {
            hideSelectTemplateModal();
            if (page === 'edit') {
                fetchDefaultCustomization(templateId);
            }
            updateSelectedTemplate(userInfo)
            if (fetchSelectedTemplateImage && page === 'buy') {
                fetchSelectedTemplateImage(templateId, false)
            }
        } else {
            if (pathFrom) {
                history.push(pathFrom);
            }
            else {
                history.push('/resume-builder/edit/?type=profile')
            }
        }
    }

    async selectTemplate() {
        this.props.eventClicked({
            'action': 'SelectTemplate',
            'label': 'HomePage'
        })

        const templateId = parseInt(document.getElementsByClassName('slick-current slick-center')
        [0].getAttribute('data-index')) + 1;
        localStorage.setItem('selected_template', (templateId));
        const { page, fetchSelectedTemplateImage, fetchDefaultCustomization, history, location, ui,
            updateSelectedTemplate, userInfo, getCandidateShineDetails, checkSessionAvaialability, hideSelectTemplateModal } = this.props;
        const values = queryString.parse(location.search),
            pathFrom = location.state && location.state.from || '',
            template = (values && values.template) || '';
        // only template selection required
        if (template === 'false') {
            this.handleSelectTemplate(templateId, ui, hideSelectTemplateModal, page, fetchDefaultCustomization, updateSelectedTemplate, fetchSelectedTemplateImage, pathFrom, userInfo, history)
        }
        else {
            if (!localStorage.getItem('candidateId') || !localStorage.getItem('token')) {
                const isSessionAvailable = await checkSessionAvaialability();
                if (isSessionAvailable) {
                    await getCandidateShineDetails()
                    this.handleSelectTemplate(templateId, ui, hideSelectTemplateModal, page, fetchDefaultCustomization, updateSelectedTemplate, fetchSelectedTemplateImage, pathFrom, userInfo, history)
                    // redirect back from where it comes
                }
                else {
                    await this.props.showLoginModal()
                    // const { state } = this.props.location;
                    // if (state && state.from) {
                    //     this.props.history.push(state.from);
                    // }
                }
            }
            else {
                this.handleSelectTemplate(templateId, ui, hideSelectTemplateModal, page, fetchDefaultCustomization, updateSelectedTemplate, fetchSelectedTemplateImage, pathFrom, userInfo, history)
            }

        }


        // get candidate details 
        // try {
        //     await this.props.getCandidateShineDetails();
        // }
        // catch (e) {
        //     console.log('error ', e);
        // }
        // if (page == 'home') {
        //     //   this.props.showLoginModal()
        // }
        // else {
        //     const { page, fetchSelectedTemplateImage, history } = this.props;
        //     localStorage.setItem('selected_template', (templateId))
        //     const select_template_modal = this.props.ui ? this.props.ui.select_template_modal : false
        //     if (select_template_modal) {
        //         this.props.hideSelectTemplateModal();
        //         if (page === 'edit') {
        //             this.props.fetchDefaultCustomization(templateId);
        //         }
        //         this.props.updateSelectedTemplate(this.props.userInfo)
        //         if (fetchSelectedTemplateImage && page === 'buy') {
        //             this.props.fetchSelectedTemplateImage(templateId, false)
        //         }
        //     } else {
        //         history.push('/resume-builder/edit/?type=profile')
        //     }
        // }
    }

    showZoomedImage(templateId) {
        this.props.displaySelectedTemplate(templateId);
        this.props.showModal()
    }


    render() {

        const settings = {
            dots: false,
            className: "center",
            centerMode: true,
            infinite: true,
            slidesToShow: 3,
            arrow: true,
            speed: 500,
        };
        if (localStorage.getItem('selected_template')) {
            settings['initialSlide'] = (localStorage.getItem('selected_template') - 1)
        }
        const { ui: { select_template_modal, modal }, page, template: { templateId, modalTemplateImage }, hideModal } = this.props;
        return (
            <Fragment>
                <TemplateModal
                    hideModal={hideModal}
                    templateId={templateId}
                    modalTemplateImage={modalTemplateImage}
                    modal={modal}
                    page={'home'} />
                < section
                    name="templates"
                    id="templates"
                    className="section-container proven-resume pos-rel">
                    {
                        select_template_modal ? "" :
                            <React.Fragment>
                                <h2>Proven resume templates</h2>
                                <strong className="section-container--sub-head">Choose from a library of classic
                                    templates and
                                    land a
                                    new job</strong>
                            </React.Fragment>
                    }
                    <a onClick={this.selectTemplate} alt="Select Template" className="orange-button proven-resume--customise">Select
                        Template</a>

                    < Slider
                        {...
                        settings
                        }
                    >
                        {
                            [1, 2, 3, 4, 5].map((item, key) => {
                                return (
                                    <div key={key}>
                                        <div className="proven-resume--slide">
                                            {
                                                !!(page === 'home') &&
                                                <div onClick={() => this.showZoomedImage(item)} className="zoom" />
                                            }
                                            <img
                                                alt="Resume-Slider"
                                                src={`${this.staticUrl}react/assets/images/resume${item}_preview.jpg`} />
                                        </div>
                                    </div>
                                )
                            })
                        }
                    </Slider>
                </section>
            </Fragment>
        )
    }

}
