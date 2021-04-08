import React from 'react';
import './howItWorks.scss';

const HowItWorks = (props) => {
    const { steps } = props

    return (
        <section className="m-container mt-0 mb-0" id="begin" data-aos="fade-up">
            <div className="m-how-works">
                <h2 className="m-heading2 mb-10">{steps?.main_heading}</h2>
                <ul>
                    {
                        steps?.articles?.map((article, index) => {
                            return (
                                <li key={index}>
                                    <figure className="micon-how-works">
                                        <i className={`micon-how-works${index + 1}`}></i>
                                    </figure>
                                    <div>
                                        <strong className="">{article.heading}</strong>
                                        <p>{article.article}</p>
                                    </div>
                                </li>
                            )
                        })
                    }
                </ul>
            </div>
        </section>
    )
}

export default HowItWorks;