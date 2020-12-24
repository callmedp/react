import React from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector, connect } from 'react-redux';
import './skillGain.scss'
import { Button } from 'react-bootstrap';
import { siteDomain } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const SkillGain = (props) => {

    const { skillGainList, name, slug, heading } = useSelector( store => store.skillBanner );
    const tracking_data = getTrackingInfo();
    const dispatch = useDispatch();
    const { trackUser } = props;

    const testRedirect = () =>{
        MyGA.SendEvent('TestYourSkill','ln_skill_test', "ln_" + name, heading,'', false, true);
        trackUser({"query" : tracking_data, "action":'exit_skill_page'});
        window.location.replace(`${siteDomain}/practice-tests/${slug}/sub`);
    }
    

    return (
        <section className="m-container mt-0 mb-0 pb-0" data-aos="fade-up">
            <div className="d-flex">
                <div className="m-skill-gain">
                    <h2 className="m-heading2">Skills you will gain</h2>
                    <ul className="m-skill-gain__list">
                        {
                            skillGainList?.map((skill, index) => {
                                return <li key={index}>{skill}</li>
                            })
                        } 
                    </ul>
                    <div className="m-skill-gain__banner mt-30" data-aos="fade-up">
                        <p>Take our free practice test to test your skill level in <strong>{name}</strong></p>
                        <Button className="btn-blue-outline" onClick={testRedirect}>Take free test</Button>
                    </div>
                </div>
            </div>
        </section>
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "trackUser": (data) => {
            return dispatch(trackUser(data))
        }
    }
}

export default connect(null, mapDispatchToProps)(SkillGain);