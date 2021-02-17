import React, {useState} from 'react';
import './learningAdvantage.scss';
import { Link } from 'react-router-dom';

   
const LearningAdvantage = (props) => {
    
    return(
        <section className="container-fluid learning-advantage" data-aos="fade-up">
            <div className="row">
                <div className="container mt-40 mb-20"> 
                    <div className="row">
                        <h2 className="heading2 mx-auto mb-5">Shine learning advantages</h2>
                        <ul className="mt-50">
                            <li className="col">
                                <div className="learning-advantage__txt">
                                    <figure className="icon-advantage1"></figure>
                                    <p>Practice test/Assessments to find your strengths</p>
                                </div>
                            </li>
                            <li className="col">
                                <div className="learning-advantage__txt">
                                    <figure className="icon-advantage2"></figure>
                                    <p>Take Quality courses to upskill yourself with the latest skills</p>
                                </div>
                            </li>
                            <li className="col">
                                <div className="learning-advantage__txt">
                                    <figure className="icon-advantage3"></figure>
                                    <p>Badging/ Highlight these skills in your profile</p>
                                </div>
                            </li>
                            <li className="col">
                                <div className="learning-advantage__txt">
                                    <figure className="icon-advantage4"></figure>
                                    <p>Job assistance services  for best job in market</p>
                                </div>
                            </li>
                            <li className="col">
                                <div className="learning-advantage__txt">
                                    <figure className="icon-advantage5"></figure>
                                    <p>Build your dream career</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
}
   
export default LearningAdvantage;