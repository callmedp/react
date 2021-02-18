import React from 'react';
import { Link } from 'react-router-dom';
import './guidanceRecommendations.scss';


const GuidanceRecommendations = (props) => {
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
                    <li className="active">
                        <Link to={"#"}>
                            <figure>
                                <img src="./media/images/mobile/ui-list-icon1.png" alt="Find the right job" />
                            </figure>
                            <h3>Find the right job</h3>
                        </Link>
                    </li>
                    <li>
                        <Link to={"#"}>
                            <figure>
                                <img src="./media/images/mobile/ui-list-icon2.png" alt="Make a career change" />
                            </figure>
                            <h3>Make a career change</h3>
                        </Link>
                    </li>
                    <li>
                        <Link to={"#"}>
                            <figure>
                                <img src="./media/images/mobile/ui-list-icon3.png" alt="Improve your profile" />
                            </figure>
                            <h3>Improve your profile</h3>
                        </Link>
                    </li>
                    <li>
                        <Link to={"#"}>
                            <figure>
                                <img src="./media/images/mobile/ui-list-icon4.png" alt="Progress your career" />
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