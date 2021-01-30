import React, {useState} from 'react';
import './learningAdvantage.scss';
import { Link } from 'react-router-dom';

   
const LearningAdvantage = (props) => {
    return(
        <section className="m-container m-learning-advantage mt-0 mb-0 pr-0" data-aos="fade-up">
            <h2 className="m-heading2-home text-center mt-20">Shine learning advantage</h2>
            <ul className="mt-40">
                <li className="col">
                    <div className="learning-advantage__txt">
                        <figure className="micon-advantage1"></figure>
                        <p>Practice test/Assessments to find your strengths</p>
                    </div>
                </li>
                <li className="col">
                    <div className="learning-advantage__txt">
                        <figure className="micon-advantage2"></figure>
                        <p>Take Quality courses to upskill yourself with the latest skills</p>
                    </div>
                </li>
                <li className="col">
                    <div className="learning-advantage__txt">
                        <figure className="micon-advantage3"></figure>
                        <p>Badging/ Highlight these skills in your profile</p>
                    </div>
                </li>
                <li className="col">
                    <div className="learning-advantage__txt">
                        <figure className="micon-advantage4"></figure>
                        <p>Job assistance services  for best job in market</p>
                    </div>
                </li>
                <li className="col">
                    <div className="learning-advantage__txt">
                        <figure className="micon-advantage5"></figure>
                        <p>Build your dream career</p>
                    </div>
                </li>
            </ul>
        </section>
    )
}
   
export default LearningAdvantage;