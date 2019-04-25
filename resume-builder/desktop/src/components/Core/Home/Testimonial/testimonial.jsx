import React, {Component} from 'react';
import './testimonial.scss'

export default class Testimonial extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'

    }

    render() {
        return (
            <section className="section-container grey-bg">
                <h2>Success stories</h2>
                <strong className="section-container--sub-head">What are our customers saying about our resume
                    builder</strong>
                <ul className="testimonials mt-30">
                    <li className="testimonials--list">
                        <div className="testimonials--image">
                            <span className="mr-20"><img alt={"Testimonial 1"}
                                                         src={`${this.staticUrl}react/assets/images/testimonial1.jpg`}/></span>
                            <span><strong>Sumit Sharma</strong>
                            Project Manager, Sapient</span>
                        </div>
                        <div className="testimonials--content">
                            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum
                                has been the industry's standard dummy text ever since the 1500s, when an unknown
                                printer took a galley.</p>
                        </div>
                    </li>
                    <li className="testimonials--list">
                        <div className="testimonials--image">
                            <span className="mr-20"><img alt={"Testimonial 2"}
                                                         src={`${this.staticUrl}react/assets/images/testimonial2.jpg`}/></span>
                            <span><strong>Shreya Verma</strong>
                            Associate, Amazon</span>
                        </div>
                        <div className="testimonials--content">
                            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum
                                has been the industry's standard dummy text ever since the 1500s, when an unknown
                                printer took a galley.</p>
                        </div>
                    </li>
                    <li className="testimonials--list">
                        <div className="testimonials--image">
                            <span className="mr-20"><img alt={"testimonial 3"}
                                                         src={`${this.staticUrl}react/assets/images/testimonial3.jpg`}/></span>
                            <span><strong>Amit Sinha</strong>
                            IT Manager, HCL</span>
                        </div>
                        <div className="testimonials--content">
                            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum
                                has been the industry's standard dummy text ever since the 1500s, when an unknown
                                printer took a galley.</p>
                        </div>
                    </li>
                </ul>
                <div className="testimonials--indicators">
                    <span></span> <span className="active"></span> <span></span>
                </div>
            </section>
        )
    }

}
