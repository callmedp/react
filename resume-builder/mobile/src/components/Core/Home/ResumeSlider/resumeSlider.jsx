import React, { Component, ReactDOM } from 'react';
import './resumeSlider.scss'
import Slider from "react-slick";
import queryString from "query-string";
import propTypes from 'prop-types';

export default class ResumeSlider extends Component {
    constructor(props) {
        super(props);
        this.customise = this.customise.bind(this);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.handleSelectTemplate = this.handleSelectTemplate.bind(this);

    }

    handleSelectTemplate(templateId, showtext, updateSelectedTemplate, updateModalStatus, pathFrom, history) {
        localStorage.setItem('selected_template', (templateId));
        if (!showtext) {
            updateModalStatus({ modal_status: false })
            updateSelectedTemplate(this.props.personalInfo)
        } else {
            if (pathFrom) {
                history.push(pathFrom);
            }
            else {
                history.push('/resume-builder/edit/?type=profile')
            }
        }
    }

    async customise() {
        const { eventClicked, showtext, updateModalStatus, updateSelectedTemplate ,location, history, checkSessionAvaialability, getCandidateShineDetails, sendTrackingInfo} = this.props
        eventClicked({
            'action': 'SelectTemplate',
            'label': 'HomePage'
        })
        sendTrackingInfo('select_template',1);

        const templateId = (parseInt(document.getElementsByClassName('slick-current')[0].getAttribute('data-index')) + 1);

        localStorage.setItem('selected_template', templateId);

        const values = queryString.parse(location.search),
            pathFrom = location.state && location.state.from || '',
            template = (values && values.template) || '';

        // only template selection required
        if (template === 'false') {
            this.handleSelectTemplate(templateId, showtext, updateSelectedTemplate, updateModalStatus, pathFrom, history)
        }
        else {
            if (!localStorage.getItem('candidateId') || !localStorage.getItem('token')) {
                const isSessionAvailable = await checkSessionAvaialability();
                if (isSessionAvailable) {
                    await getCandidateShineDetails()
                    this.handleSelectTemplate(templateId, showtext, updateSelectedTemplate, updateModalStatus, pathFrom, history)
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
                this.handleSelectTemplate(templateId, showtext, updateSelectedTemplate, updateModalStatus, pathFrom, history)
            }
        }
    }

    render() {
        let settings = {
            dots: false,
            infinite: true,
            speed: 500,
            slidesToShow: 1,
            slidesToScroll: 1,
        };
        if (localStorage.getItem('selected_template')) {
            settings['initialSlide'] = localStorage.getItem('selected_template') - 1;
        }
        const { showtext } = this.props

        return (

            <section className="section proven-resume mt-30 home-slider" id="templates">
                {showtext ?
                    <div className="text-center">
                        <h2 className="section__head">Proven resume templates</h2>
                        <p className="section__subHead">Choose from a library of classic templates <br />and land a new job
                    </p>
                    </div> : ''
                }

                <div className="proven-resume__slideWrap">
                    <Slider {...settings}>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-1.jpg`} alt="Resume 1"/>
                        </div>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-2.jpg`} alt="Resume 2"/>
                        </div>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-3.jpg`} alt="Resume 3"/>
                        </div>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-4.jpg`} alt="Resume 4"/>
                        </div>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-5.jpg`} alt="Resume 5"/>
                        </div>
                    </Slider>

                    <a className="btn btn__shadow btn__round btn__primary" alt="Select Template" onClick={this.customise}>Select Template</a>
                </div>
            </section>
        )
    }
}

ResumeSlider.propTypes = {
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
    showLoginModal: propTypes.func,
    showtext: propTypes.bool,
    updateModalStatus: propTypes.func,
    updateSelectedTemplate: propTypes.func,
    checkSessionAvaialability: propTypes.func,
    getCandidateShineDetails: propTypes.func,
}
