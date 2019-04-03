import React, {Component} from 'react';
import './testimonial.scss'

export default class Testimonial extends Component {
    constructor(props) {
        super(props)
    }


    render() {
        return (
            <section className="section-container grey-bg">
                <h2>Success stories</h2>
                <strong className="section-container--sub-head">What are our customers saying about our resume builder</strong>
                <ul className="testimonials mt-30">
                    <li className="testimonials--list">
                        <div className="testimonials--image">
                            <div><img src="/images/testimonial1.jpg" /></div>
                            <div><strong>Sumit Sharma</strong>
                            Project Manager, Sapient</div>
                        </div>
                        <div className="testimonials--content">
                            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley.</p>
                        </div>
                    </li>
                    <li className="testimonials--list">
                        <div className="testimonials--image">
                            <div><img src="/images/testimonial2.jpg" /></div>
                            <div><strong>Shreya Verma</strong>
                            Associate, Amazon</div>
                        </div>
                        <div className="testimonials--content">
                            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley.</p>
                        </div>
                    </li>
                    <li className="testimonials--list">
                        <div className="testimonials--image">
                            <div><img src="/images/testimonial3.jpg" /></div>
                            <div><strong>Amit Sinha</strong></div>
                            IT Manager, HCL
                        </div>
                        <div className="testimonials--content">
                            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley.</p>
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
