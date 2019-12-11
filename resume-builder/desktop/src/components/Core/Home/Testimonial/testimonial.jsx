import React, {Component} from 'react';
import './testimonial.scss'
import Slider from "react-slick";
import {testimonials} from "../../../../Utils/testimonials";

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
            adaptiveHeight: true,
            dotClass: "testimonials--indicators"
        };
        return (
            <section className="section-container grey-bg testimonial-slider">
                <h2>Success stories</h2>
                <strong className="section-container--sub-head">What are our customers saying about our resume
                    builder</strong>
                <Slider {...settings}>
                    {
                        (testimonials || [])    .map((el, key) => {
                            return(
                                <div className="testimonials--list" key={key}>
                                    <span className="icon-quote"></span>
                                    <div className="testimonials--wrap">

                                        
                                        <div className="testimonials--content">
                                            <p>{el.review}</p>
                                        </div>
                                        
                                        <div className="testimonials--author">
                                            <strong>{el.name}</strong>
                                            <span>{el.profile}</span>
                                        </div>
                                    </div>
                                </div>
                            )
                        })
                    }
                </Slider>
                {/*<div className="testimonials--indicators">*/}
                {/*<span></span> <span className="active"></span> <span></span>*/}
                {/*</div>*/}
            </section>
        )
    }

}
