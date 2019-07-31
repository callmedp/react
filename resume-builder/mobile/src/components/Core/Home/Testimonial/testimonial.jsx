import React, {Component} from 'react';
import './testimonial.scss'
import {testimonials} from "../../../../Utils/testimonials";

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
                        {
                            (testimonials || []).map((el, key) => (
                                <li className="success-stories__item white-box pt-30">
                                    <div className="success-stories__infoWrap">
                                        <p>{el.review}</p>
                                        <div className="success-stories__nameInfo">
                                            <h3>{el.name}</h3>
                                            <span>{el.profile}</span>
                                            {/* <p>Project Manager, Sapient</p> */}
                                        </div>
                                    </div>
                                </li>
                            ))
                        }
                    </ul>
                </div>
            </section>

        )
    }

}
