import React from 'react';
import { Link } from 'react-router-dom';
import './guidanceRecommendations.scss';


const GuidanceRecommendations = (props) => {
    return (
        <section className="container-fluid mt-30n mb-0">
            <div className="row">
                <div className="container">
                    <div className="ui-main col">
                        <div className="ui-steps">
                            <Link className="current" to={"#"}>1</Link>
                            <Link>2</Link>
                            <Link>3</Link>
                        </div>

                        <h2 className="heading3 mt-30">How can we help you?</h2>
                        <p>Make your choice to go ahead</p>

                        <ul className="ui-list mt-40 mb-30">
                            <li className="active">
                                <Link to={"/user-intent/find-right-job/"}>
                                    <figure>
                                        <img src="/media/images/desktop/ui-list-icon1.png" alt="Find the right job" />
                                    </figure>
                                    <h3>Find the right job</h3>
                                </Link>
                            </li>
                            <li>
                                <Link to={"/user-intent/make-career-change/"}>
                                    <figure>
                                        <img src="/media/images/desktop/ui-list-icon2.png" alt="Make a career change" />
                                    </figure>
                                    <h3>Make a career change</h3>
                                </Link>
                            </li>
                            <li>
                                <Link to={"/user-intent/improve-profile/"}>
                                    <figure>
                                        <img src="/media/images/desktop/ui-list-icon3.png" alt="Improve your profile" />
                                    </figure>
                                    <h3>Improve your profile</h3>
                                </Link>
                            </li>
                            <li>
                                <Link to={"/user-intent/progress-career"}>
                                    <figure>
                                        <img src="/media/images/desktop/ui-list-icon4.png" alt="Progress your career" />
                                    </figure>
                                    <h3>Progress your career</h3>
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default GuidanceRecommendations;