import React, { Component, Fragment } from 'react';
import './resumeSlider.scss'
import Slider from "react-slick";
import TemplateModal from "../../../Modal/tempateModal";
import LoginModal from "../../../Modal/loginModal";


export default class ResumeSlider extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.selectTemplate = this.selectTemplate.bind(this);
        this.showZoomedImage = this.showZoomedImage.bind(this);
    }

    async selectTemplate() {
        this.props.eventClicked({
            'action': 'SelectTemplate',
            'label': 'HomePage'
        })
        const templateId = parseInt(document.getElementsByClassName('slick-current slick-center')[0].getAttribute('data-index')) + 1;
        const { page, fetchSelectedTemplateImage, history } = this.props;

        // get candidate details 
        try {
            await this.props.getCandidateShineDetails();
        }
        catch (e) {
                console.log('error ', e);
        }
        if (page == 'home') {
            //   this.props.showLoginModal()
        }
        else {
            const { page, fetchSelectedTemplateImage, history } = this.props;
            localStorage.setItem('selected_template', (templateId))
            const select_template_modal = this.props.ui ? this.props.ui.select_template_modal : false
            if (select_template_modal) {
                this.props.hideSelectTemplateModal();
                if (page === 'edit') {
                    this.props.fetchDefaultCustomization(templateId);
                }
                this.props.updateSelectedTemplate(this.props.userInfo)
                if (fetchSelectedTemplateImage && page === 'buy') {
                    this.props.fetchSelectedTemplateImage(templateId, false)
                }
            } else {
                history.push('/resume-builder/edit/?type=profile')
            }
        }
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
        const { ui: { select_template_modal }, page } = this.props;
        return (
            <Fragment>
                <TemplateModal {...this.props} page={'home'} />
                <LoginModal {...this.props} />
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
                    <a onClick={this.selectTemplate} className="orange-button proven-resume--customise">Select
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
