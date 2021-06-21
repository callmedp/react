import React, { useState } from 'react';
import { Link } from 'react-router-dom';

import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const DropDown = (props) => {

    const { tabList, usedIn } = props;
    const [activeTab, setActiveTab] = useState(tabList?.[0].id)
    const sendLearningTracking = useLearningTracking();

    const levelOneSelect = (item, index) => {
        MyGA.SendEvent('homepage_navigation', 'ln_homepage_navigation', 'ln_' + item.id, '', '', false, true)

        const eventCategory = usedIn === 'exploreCategories' ? (
            `explore_categories_level1`
            ) : (
                `free_resources_level1`
            )
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_${eventCategory}_${item.id}`,
            pageTitle: props.pageTitle,
            sectionPlacement: 'header',
            eventCategory: eventCategory,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: index,
        })

    }

    const levelTwoSelect = (item, child, idx) => {
        MyGA.SendEvent('homepage_navigation', 'ln_navigation_explore', 'ln_' + item.id, 'ln_' + child.id, '', false, true)

        const eventCategory = usedIn === 'exploreCategories' ? (
            `explore_categories_level2`
            ) : (
                `free_resources_level2`
            )
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_${eventCategory}_${item.id}_${child.id}`,
            pageTitle: props.pageTitle,
            sectionPlacement: 'header',
            eventCategory: eventCategory,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: idx,
        })
    }

    return (
        <>
            <ul className="nav nav-tabs" id="myTab" role="tablist" >
                {
                    tabList?.map((item, index) => {
                        return (
                            <li className="nav-item" role="presentation" key={item.id} >
                                <a className={` nav-link ${activeTab === item.id ? 'active' : ''}`}
                                    data-toggle="tab" role="tab" aria-controls="category-tab"
                                    aria-selected="true" onMouseEnter={() => setActiveTab(item.id)}
                                    href={item.url} onClick={() => levelOneSelect(item, index)}>
                                    {item.name}
                                </a>
                            </li>
                        )
                    })
                }

            </ul>
            <div className="tab-content" id="myTabContent">
                {
                    tabList?.map((item) => {
                        return (
                            <div className={`tab-pane fade ${activeTab === item.id ? 'show active' : ''}`} id="tab-links1" role="tabpanel" aria-labelledby="category-tab" key={item.id}>
                                {
                                    item.children?.map((child, idx) => {
                                        return (
                                            usedIn === 'exploreCategories' ?
                                                <Link key={child.url} to={child.url}
                                                    onClick={() => levelTwoSelect(item, child, idx)}>{child.name}
                                                </Link>
                                                :
                                                <a key={child.url} href={child.url}
                                                    onClick={() => levelTwoSelect(item, child, idx)}>{child.name}
                                                </a>
                                        )
                                    })
                                }
                            </div>
                        )
                    })
                }
            </div>
        </>
    )
}

export default DropDown;