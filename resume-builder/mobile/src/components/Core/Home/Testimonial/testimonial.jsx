import React, {Component} from 'react';
import './testimonial.scss'

export default class Testimonial extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';

    }
    render() {
        return (
            <section className="section grey-bg">
                <div className="text-center">
                    <h2 className="section__head">Success stories</h2>
                    <p className="section__subHead">What are our customers saying about our
                        <br/>resume builder</p>
                </div>

                <div className="success-stories mt-20">
                    <ul className="success-stories__items">
                        <li className="success-stories__item white-box pt-30">
                            <div className="success-stories__infoWrap">
                                <p>I am really grateful to have found this resume builder. Its intuitive and structured flow helped me build the resume in no time. It has definitely played a pivotal role in getting my dream job</p>
                                <div className="success-stories__nameInfo">
                                    <h3>Sumit Sharma</h3>
                                    {/* <p>Project Manager, Sapient</p> */}
                                </div>
                            </div>
                        </li>

                        <li className="success-stories__item white-box pt-30">
                            <div className="success-stories__infoWrap">
                                <p>This system for writing a resume was extremely helpful and really made the process a more thoughtful one and it made my resume look extremely sharp and professional. Kudos</p>

                                <div className="success-stories__nameInfo">
                                    <h3>Shreya Verma</h3>
                                    {/* <p>Project Manager, Sapient</p> */}
                                </div>
                            </div>
                        </li>

                        <li className="success-stories__item white-box pt-30">
                            <div className="success-stories__infoWrap">
                                <p>It is one of the best resume builder I have ever seen. You can prepare your resume within no time. The attractive and decent templates are designed in such a way that you will end up getting calls for interview</p>
                                <div className="success-stories__nameInfo">
                                    <h3>Amit Sinha</h3>
                                    <p>Project Manager, Sapient</p>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </section>

        )
    }

}
