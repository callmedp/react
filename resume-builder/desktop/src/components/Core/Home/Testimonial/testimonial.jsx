import React, {Component} from 'react';
import './testimonial.scss'
import Slider from "react-slick";



export default class Testimonial extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'

    }

    render() {
        const settings = {
            dots: true,
            infinite: true,
            speed: 500,
            slidesToShow: 3,
            slidesToScroll: 3,
            arrows: false,
            variableWidth: true,
            dotClass: "testimonials--indicators"
        };
        return (
            <section className="section-container grey-bg testimonial-slider">
                <h2>Success stories</h2>
                <strong className="section-container--sub-head">What are our customers saying about our resume
                    builder</strong>
                <Slider {...settings}>
                    {
                        [1, 2, 3, 4, 5, 6, 7].map(el => (
                            <div className="testimonials--list">
                                <div className="testimonials--wrap">
                                
                                    <div className="testimonials--image">
                                        <span className="mr-20">
                                            <img alt={"Testimonial 1"}
                                            src={`${this.staticUrl}react/assets/images/testimonial1.jpg`}/>
                                        </span>
                                        <span>
                                            <strong>Sumit Sharma</strong>
                                            Project Manager, Sapient
                                        </span>
                                    </div>
                                    <div className="testimonials--content">
                                        <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley.</p>
                                    </div>
                                </div>
                            </div>
                        ))
                    }
                </Slider>
                {/*<div className="testimonials--indicators">*/}
                    {/*<span></span> <span className="active"></span> <span></span>*/}
                {/*</div>*/}
            </section>
        )
    }

}
