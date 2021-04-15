import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './guidanceRecommendations.scss';
import {imageUrl} from 'utils/domains'

const GuidanceRecommendations = (props) => {
    const [activeId, setActiveId] = useState(0)
    return (
        <section className="container-fluid mt-30n mb-0">
            <div className="row">
                <div className="container">
                    <div className="ui-main col">
                        <div className="ui-steps">
                            <Link className="current" to={"#"}>1</Link>
                            <Link to={'#'}>2</Link>
                            <Link to={'#'}>3</Link>
                        </div>

                        <h2 className="heading3 mt-30">How can we help you?</h2>
                        <p>Make your choice to go ahead</p>

                        <ul className="ui-list mt-40 mb-30">
                        {/* className="active" */}
                            <li className={ activeId === 1 && 'active'} onMouseEnter={() => setActiveId(1)} onMouseLeave={() => setActiveId(0)}> 
                                <Link to={"/user-intent/find-right-job/"}>
                                    <figure>
                                        <img src={`${imageUrl}desktop/ui-list-icon1.png`} alt="Find the right job" />
                                    </figure>
                                    <h3>Find the right job</h3>
                                </Link>
                            </li>
                            <li className={ activeId === 2 && 'active'} onMouseEnter={() => setActiveId(2)} onMouseLeave={() => setActiveId(0)}>
                                <Link to={"/user-intent/make-career-change/"}>
                                    <figure>
                                        <img src={`${imageUrl}desktop/ui-list-icon2.png`} alt="Make a career change" />
                                    </figure>
                                    <h3>Make a career change</h3>
                                </Link>
                            </li>
                            <li className={ activeId === 3 && 'active'} onMouseEnter={() => setActiveId(3)} onMouseLeave={() => setActiveId(0)}>
                                <Link to={"/user-intent/improve-profile/"}>
                                    <figure>
                                        <img src={`${imageUrl}desktop/ui-list-icon3.png`} alt="Improve your profile" />
                                    </figure>
                                    <h3>Improve your profile</h3>
                                </Link>
                            </li>
                            <li className={ activeId === 4 && 'active'} onMouseEnter={() => setActiveId(4)} onMouseLeave={() => setActiveId(0)}>
                                <Link to={"/user-intent/progress-career"}>
                                    <figure>
                                        <img src={`${imageUrl}desktop/ui-list-icon4.png`} alt="Progress your career" />
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