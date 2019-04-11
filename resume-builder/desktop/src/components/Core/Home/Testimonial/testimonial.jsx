import React, {Component} from 'react';
import './testimonial.scss'

export default class Testimonial extends Component {
    render() {
        return (
            <section className="section-container grey-bg">
                <h2>Success stories</h2>
                <strong className="section-container--sub-head">What are our customers saying about our resume
                    builder</strong>
                <ul className="testimonials mt-30">
                    <li className="testimonials--list">
                        <div className="testimonials--image">
<<<<<<< HEAD:resume-builder/desktop/src/components/Core/Home/Testimonial/testimonial.jsx
                            <span className="mr-20"><img src="/media/static/react/assets/images/testimonial1.jpg" /></span>
=======
                            <span className="mr-20"><img alt={"Testimonial 1"}
                                                         src="/media/static/react/assets/images/testimonial1.jpg"/></span>
>>>>>>> 965a2a5ee483958b41faa199ec9653eb6fe0a2ee:resume-builder/src/components/Core/Home/Testimonial/testimonial.jsx
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
<<<<<<< HEAD:resume-builder/desktop/src/components/Core/Home/Testimonial/testimonial.jsx
                            <span className="mr-20"><img src="/media/static/react/assets/images/testimonial2.jpg" /></span>
=======
                            <span className="mr-20"><img alt={"Testimonial 2"}
                                                         src="/media/static/react/assets/images/testimonial2.jpg"/></span>
>>>>>>> 965a2a5ee483958b41faa199ec9653eb6fe0a2ee:resume-builder/src/components/Core/Home/Testimonial/testimonial.jsx
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
<<<<<<< HEAD:resume-builder/desktop/src/components/Core/Home/Testimonial/testimonial.jsx
                            <span className="mr-20"><img src="/media/static/react/assets/images/testimonial3.jpg" /></span>
=======
                            <span className="mr-20"><img alt={"testimonial 3"}
                                                         src="/media/static/react/assets/images/testimonial3.jpg"/></span>
>>>>>>> 965a2a5ee483958b41faa199ec9653eb6fe0a2ee:resume-builder/src/components/Core/Home/Testimonial/testimonial.jsx
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
