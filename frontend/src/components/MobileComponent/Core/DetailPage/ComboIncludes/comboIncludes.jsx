import React from 'react';
import '../../SkillPage/DomainJobs/domainJobs.scss';
import { siteDomain } from 'utils/domains';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const ComboIncludes = (props) => {
    const { comboList } = props;
    const sendLearningTracking = useLearningTracking();

    const comboIncludesTracking = (combo, indx) => {
        sendLearningTracking({
            productId: '',
            event: `course_detail_${stringReplace(combo.heading ? combo.heading : combo.name)}_combo_includes_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: 'combo_includes',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    return (
        <section className="m-container m-domain-jobs mb-0 pt-0 pb-0" data-aos="fade-up">
            <div className="m-domain-jobs__list">
                <strong className="m-heading2">Combo includes</strong>
                <ul>
                    {
                        comboList?.map((combo, indx) => {
                            return (
                            <li key={indx}><a href={`${siteDomain}${combo.url}`} onClick={() => comboIncludesTracking(combo, indx)}>{ combo.heading ? combo.heading : combo.name }</a></li>
                            )
                        })
                    }
                </ul>
            </div>
        </section>
    )
}

export default ComboIncludes;