import React from 'react';
import { Link } from 'react-router-dom';
import './otherSkills.scss'
import { useDispatch, useSelector, connect } from 'react-redux';
import { siteDomain } from 'utils/domains';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const OtherSkills = (props) => {
    const { otherSkills } = useSelector( store => store.skillBanner )
    const tracking_data = getTrackingInfo();
    const dispatch = useDispatch();
    const { trackUser } = props;
    const getOtherSkills = (skill, index) => {
        return (
            <li key={index} itemscope itemtype="http://schema.org/ItemList">
                <a itemprop="url" href={`${siteDomain}${skill.url}`} onClick={() => trackUser({"query":tracking_data, "action": 'exit_skill_page'})}>{skill.name}</a>
            </li>
        )
    }

    const showOtherSkills = () =>{
        return (
            <section className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up">
                <div className="d-flex">
                    <div className="m-other-skill">
                        <h2 className="m-heading2">Other Skills To Explore</h2>
                        <ul className="m-other-skill__list">
                            {/* <li>
                                <Link to={"#"}>Sales Courses</Link>
                            </li>*/}
                            {
                                otherSkills?.map(getOtherSkills)
                            }
                        </ul>

                    </div>
                </div>
            </section>
        )
    }

    return (
        otherSkills.length ? showOtherSkills() : null
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "trackUser": (data) => {
            return dispatch(trackUser(data))
        }
    }
}

export default connect(null, mapDispatchToProps)(OtherSkills);