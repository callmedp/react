import React from 'react';
import { Link } from 'react-router-dom';
import './otherSkills.scss'
import { useSelector } from 'react-redux';
import { siteDomain } from 'utils/domains';

const OtherSkills = (props) => {
    const { otherSkills } = useSelector( store => store.skillBanner )
    const getOtherSkills = (skill, index) => {
        return (
            <li key={index}>
                <a href={`${siteDomain}${skill.url}`}>{skill.name}</a>
            </li>
        )
    }

    const showOtherSkills = () =>{
        return (
            <section className="m-container m-lightblue-bg mt-0 mb-0">
                <div className="d-flex">
                    <div className="m-other-skill">
                        <h2 className="m-heading2">Other Skills To Explore</h2>
                        <ul className="m-other-skill__list">
                            {/* <li>
                                <Link to={"#"}>Sales Courses</Link>
                            </li>*/}
                            {
                                otherSkills?.map((skill, index) => getOtherSkills(skill, index))
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

export default OtherSkills;