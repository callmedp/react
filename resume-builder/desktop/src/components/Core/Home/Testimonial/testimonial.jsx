import React, {Component} from 'react';
import './testimonial.scss'
import Slider from "react-slick";
import {testimonials} from "../../../../Utils/testimonials";

console.log('---', testimonials);
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
                        (testimonials || []).map((el, key) => {
                            return(
                                <div className="testimonials--list" key={key}>
                                    <div className="testimonials--wrap">

                                        <div className="testimonials--image">
                                        <span className="mr-20">
                                            <img alt={"Testimonial 1"}
                                                 src={`${this.staticUrl}react/assets/images/user-${key+1}.jpg`}/>
                                        </span>
                                            <span>
                                            <strong>{el.name}</strong>
                                        </span>
                                        </div>
                                        <div className="testimonials--content">
                                        </div>
                                        <p>{el.review}</p>
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
