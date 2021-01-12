import React from 'react';
import Badge from 'react-bootstrap/Badge';
import './otherSkills.scss'
import { useDispatch, useSelector, connect } from 'react-redux';
import { siteDomain } from 'utils/domains';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const OtherSkills = (props) => {

    const { otherSkills } = useSelector( store => store.skillBanner )
    const tracking_data = getTrackingInfo();
    const dispatch = useDispatch();
    const { userTrack } = props;
    
    return (
        otherSkills.length ? (
            <section className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
                <div className="row">
                    <div className="container">
                            <div className="other-skills">
                                <h2 className="heading2 mt-40">Other Skills To Explore</h2>
                                <div className="other-skills__list">
                                    {
                                        otherSkills?.map((skill, index) => {
                                            return (
                                                <React.Fragment key={index} >
                                                <Badge pill itemScope itemType="http://schema.org/ItemList" variant="light"><a onClick={() => userTrack({"query" : tracking_data, "action" : 'exit_skill_page' })}  href={`${siteDomain}${skill.url}`} >{skill.name}</a></Badge>&nbsp;
                                                </React.Fragment>
                                            )
                                        })
                                    }
                                </div>

                            </div>

                    </div>
                </div>
            </section>
        ) : null
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "userTrack": (data) => {
            return dispatch(trackUser(data))
        }
    }
}

export default connect(null, mapDispatchToProps)(OtherSkills);