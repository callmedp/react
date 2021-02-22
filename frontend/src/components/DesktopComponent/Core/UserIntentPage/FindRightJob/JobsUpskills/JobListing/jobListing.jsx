import React from 'react';
import { Link } from 'react-router-dom';

const JobListing = (props) => {

    const { jobList } = props;

    return (
        <ul className="shine-courses-listing ml-10n mt-30">
            {
                jobList?.map((job, index) => {
                    return (
                        <li className="col" key={index}>
                            <div className="course">
                                <div className="d-flex p-20">
                                    <div className="course__content">
                                        <span className="hot-badge">
                                            <figure className="icon-hot"></figure> Hot
                                                            </span>
                                        <h3 className="heading3">
                                            <Link to={"#"}>UI UX Designer Web,HTML5,CSS3,Adobe suite, Sketch, Invision</Link>
                                        </h3>
                                        <strong>eInfochips</strong>

                                        <ul>
                                            <li>2 - 4 Years </li>
                                            <li>Gurgaon</li>
                                        </ul>

                                        <p className="mt-10">Prospects Should Build stunning UI / UX experience in our products that will enable in get more customer engagement. Identify blockers in the current user experience and provide a better</p>
                                    </div>
                                    <div className="course__price-date">
                                        <span>Dec 18, 2020</span>
                                        <Link to={"#"} class="btn btn-secondary mt-10">Apply now</Link>
                                    </div>
                                </div>
                                <div className="course__bottom">
                                    <strong>Skills: </strong>
                                    <ul>
                                        <li>adobe photoshop,</li>
                                        <li>html,</li>
                                        <li>jquery,</li>
                                        <li>research,</li>
                                        <li>android</li>
                                    </ul>
                                </div>
                            </div>
                        </li>
                    )
                })
            }
        </ul>
    )
}

export default JobListing;
