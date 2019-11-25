import React, { Component, ReactDOM } from 'react';
import './resumeSlider.scss'
import Slider from "react-slick";
import queryString from "query-string";


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
        const { eventClicked, showtext, updateModalStatus, updateSelectedTemplate ,location, history, checkSessionAvaialability, getCandidateShineDetails} = this.props
        eventClicked({
            'action': 'SelectTemplate',
            'label': 'HomePage'
        })

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
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-1.jpg`} alt="" />
                        </div>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-2.jpg`} alt="" />
                        </div>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-3.jpg`} alt="" />
                        </div>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-4.jpg`} alt="" />
                        </div>
                        <div className="proven-resume__imageWrap">
                            <img src={`${this.staticUrl}react/assets/images/mobile/resume-5.jpg`} alt="" />
                        </div>
                    </Slider>

                    <a className="btn btn__shadow btn__round btn__primary" onClick={this.customise}>Select Template</a>
                </div>
            </section>
        )
    }
}
