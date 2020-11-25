import React from 'react';
import Badge from 'react-bootstrap/Badge';
import './otherSkills.scss'
import { useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';

const OtherSkills = (props) => {

    const { otherSkills } = useSelector( store => store.skillBanner )
    
    
    return (
        otherSkills.length ? (
            <section className="container-fluid lightblue-bg mt-40">
                <div className="row">
                    <div className="container">
                            <div className="other-skills">
                                <h2 className="heading2 mt-40">Other Skills To Explore</h2>
                                <div className="other-skills__list">
                                    {
                                        otherSkills?.map((skill, index) => {
                                            return (
                                                <React.Fragment key={index}>
                                                <Badge pill variant="light"><a href={`${siteDomain}${skill.url}`}>{skill.name}</a></Badge>&nbsp;
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

export default OtherSkills;