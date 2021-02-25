import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './guidanceRecommendations.scss';
import {imageUrl} from 'utils/domains'


const GuidanceRecommendations = (props) => {
    const [activeId, setActiveId] = useState(0);
    return (
        <section className="m-container mt-0 mb-0">
            <div className="m-ui-main">
                <div className="m-ui-steps">
                    <Link className="m-current" to={"#"}>1</Link>
                    <Link>2</Link>
                    <Link>3</Link>
                </div>

                <h2 className="m-heading2 mt-20">How can we help you?</h2>
                <p>Make your choice to go ahead</p>

                <ul className="m-ui-list mt-20 mb-30">
                    <li className={ activeId === 1 && 'active'} onTouchStart={() => setActiveId(1)} onTouchEnd={()=> setActiveId(0)} >
                        <Link to={"/user-intent/find-right-job/"}>
                            <figure>
                                <img src={`${imageUrl}mobile/ui-list-icon1.png`} alt="Find the right job" />
                            </figure>
                            <h3>Find the right job</h3>
                        </Link>
                    </li>
                    <li className={ activeId === 2 && 'active'} onTouchStart={() => setActiveId(2)} onTouchEnd={()=> setActiveId(0)}>
                        <Link to={"/user-intent/make-career-change/"}>
                            <figure>
                                <img src={`${imageUrl}mobile/ui-list-icon2.png`} alt="Make a career change" />
                            </figure>
                            <h3>Make a career change</h3>
                        </Link>
                    </li>
                    <li className={ activeId === 3 && 'active'} onTouchStart={() => setActiveId(3)} onTouchEnd={()=> setActiveId(0)}>
                        <Link to={"/user-intent/improve-profile/"}>
                            <figure>
                                <img src={`${imageUrl}mobile/ui-list-icon3.png`} alt="Improve your profile" />
                            </figure>
                            <h3>Improve your profile</h3>
                        </Link>
                    </li>
                    <li className={ activeId === 4 && 'active'} onTouchStart={() => setActiveId(4)} onTouchEnd={()=> setActiveId(0)}>
                        <Link to={"/user-intent/progress-career"}>
                            <figure>
                                <img src={`${imageUrl}mobile/ui-list-icon4.png`} alt="Progress your career" />
                            </figure>
                            <h3>Progress your career</h3>
                        </Link>
                    </li>
                </ul>
            </div>
        </section>
    )
}

export default GuidanceRecommendations;