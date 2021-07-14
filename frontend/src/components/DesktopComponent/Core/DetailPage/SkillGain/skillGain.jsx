import React from 'react';
import Badge from 'react-bootstrap/Badge';
import { Link as LinkScroll } from "react-scroll";
import '../../SkillPage/SkillGain/skillGain';
import { imageUrl } from 'utils/domains';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const SkillGain = (props) => {
    const {skill, prd_H1, product_id} = props;
    window['course_skills'] = skill.slice(0,4);
    const sendLearningTracking = useLearningTracking();

    const trackEnquireNow = () => {
        sendLearningTracking({
            productId: '',
            event: `course_detail_skill_gain_${stringReplace(prd_H1)}_${product_id}_enquire_now_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: 'skill_gain',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
        <section className="container-fluid lightblue-bg mt-40" data-aos="fade-up">
            <div className="row">
                <div className="container">
                    <div className="d-flex">
                        <div className="skill-gain">
                            <h3 className="heading2 mt-40">Skills you will gain</h3>
                            <div className="skill-gain__list">
                                {
                                    skill?.map((skl, indx) => {
                                        return (
                                            <Badge pill variant="light" key={indx}>{skl}</Badge>
                                        )
                                    })
                                }
                                {' '}
                            </div>
                            <div className="d-flex mt-50 mb-20">
                                <LinkScroll to={"enquire-now"} onClick={trackEnquireNow} className="btn btn-outline-primary btn-custom" offset={-160}>Enquire now</LinkScroll>
                            </div>
                        </div>
                        <figure className="skill-gain__img mt-40">
                            <span className="skill-tween1">
                                <img src={`${imageUrl}desktop/skill-tween1.svg`} />
                            </span>
                            <span className="skill-tween2">
                                <img src={`${imageUrl}desktop/skill-tween2.svg`} />
                            </span>
                            <span className="skill-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="400">
                                <img src={`${imageUrl}desktop/skill-tween3.svg`} />
                            </span>
                            <span className="skill-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500">
                                <img src={`${imageUrl}desktop/skill-tween4.svg`} />
                            </span>
                            <span className="skill-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="600">
                                <img src={`${imageUrl}desktop/skill-tween5.svg`} />
                            </span>
                            <span className="skill-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700">
                                <img src={`${imageUrl}desktop/skill-tween6.svg`} />
                            </span>
                            <span className="skill-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="800">
                                <img src={`${imageUrl}desktop/skill-tween7.svg`} />
                            </span>
                            <span className="skill-tween8" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900">
                                <img src={`${imageUrl}desktop/skill-tween8.svg`} />
                            </span>
                        </figure>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default SkillGain;