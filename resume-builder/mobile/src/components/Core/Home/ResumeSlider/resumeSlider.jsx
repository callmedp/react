import React, {Component} from 'react';
import './resumeSlider.scss'

export default class ResumeSlider extends Component {
    constructor(props) {
        super(props)
        this.customise = this.customise.bind(this)
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
    }

    customise() {
        window.location = '/resume-builder/edit/?type=profile'
    }

    render() {
        return (
            <section className="section proven-resume pt-30" id="templates">
                <div className="text-center">
                    <h2 className="section__head">Proven resume templates</h2>
                    <p className="section__subHead">Choose from a library of classic templates <br/>and land a new job
                    </p>
                </div>

                <div className="proven-resume__slideWrap">
                    <ul>
                        <li>
                            <div className="proven-resume__imageWrap">
                                <img src={`${this.staticUrl}react/assets/images/mobile/resume.jpg`} alt=""/>
                            </div>
                        </li>
                    </ul>

                    <a className="btn btn__shadow btn__round btn__primary" onClick={this.customise}>Customise</a>
                </div>
            </section>
        )
    }

}
