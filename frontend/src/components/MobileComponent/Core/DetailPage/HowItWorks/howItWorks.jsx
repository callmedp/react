import React from 'react';
import './howItWorks.scss';

const HowItWorks = (props) => {
    const { steps } = props

    return (
        <section className="m-container mt-0 mb-0" data-aos="fade-up">
            <div className="m-how-works">
                <h2 className="m-heading2 mb-10">{steps?.main_heading}</h2>
                <ul>
                    {
                        steps?.articles?.map((article, index) => {
                            return (
                                <li key={index}>
                                    <figure className="micon-how-works">
                                        <i className="micon-how-works1"></i>
                                    </figure>
                                    <div>
                                        <strong className="">{article.heading}</strong>
                                        <p>{article.article}</p>
                                    </div>
                                </li>
                            )
                        })
                    }
                    {/* <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works1"></i>
                        </figure>
                        <div>
                            <strong className="">Introduce yourself</strong>
                            <p>Place order and upload your initial resume</p>
                        </div>
                    </li>
                    <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works2"></i>
                        </figure>
                        <div>
                            <strong>We Update</strong>
                            <p>Our expert will update your profile</p>
                        </div>
                    </li>
                    <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works3"></i>
                        </figure>
                        <div>
                            <strong>Featured</strong>
                            <p>Get featured on shine</p>
                        </div>
                    </li>
                    <li>
                        <figure className="micon-how-works">
                            <i className="micon-how-works4"></i>
                        </figure>
                        <div>
                            <strong>View</strong>
                            <p>Get 10x recruiter views</p>
                        </div>
                    </li> */}
                </ul>
            </div>
        </section>
    )
}

export default HowItWorks;