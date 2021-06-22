import React from 'react';
import './comboIncludes.scss';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const ComboIncludes = (props) => {
    const { combo_list } = props;
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
        <div className="combo-includes mt-20">
            <h2 className="heading2">Combo includes</h2>
            <ul className="combo-includes__list">
                {
                    combo_list?.map((combo, indx) => {
                        return (
                            <li key={indx}>
                                <a href={`${combo.url}`} onClick={() => comboIncludesTracking(combo, indx)}>{combo.heading}</a>
                            </li>
                        )
                    })
                }
            </ul>
        </div>
    )
}

export default ComboIncludes;