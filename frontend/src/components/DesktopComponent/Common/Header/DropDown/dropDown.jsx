import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { resumeShineSiteDomain } from 'utils/domains';
import { MyGA } from 'utils/ga.tracking.js';

const DropDown = (props) => {

    const { tabList, usedIn } = props;
    const [activeTab, setActiveTab] = useState(tabList?.[0].id)

    return (
        <>
            <ul className="nav nav-tabs" id="myTab" role="tablist" >
                {
                    tabList?.map((item) => {
                        return (
                            <li className="nav-item" role="presentation" key={item.id} >
                                <a className={` nav-link ${activeTab === item.id ? 'active' : ''}`}
                                    data-toggle="tab" role="tab" aria-controls="category-tab"
                                    aria-selected="true" onMouseEnter={() => setActiveTab(item.id)}
                                    href={item.url} onClick={() => MyGA.SendEvent('homepage_navigation', 'ln_homepage_navigation', 'ln_' + item.id, '', '', false, true)}>
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
                                    item.children.map(child => {
                                        return (
                                            usedIn === 'exploreCategories' ?
                                                <Link key={child.url} to={child.url}
                                                    onClick={() => MyGA.SendEvent('homepage_navigation', 'ln_navigation_explore', 'ln_' + item.id, 'ln_' + child.id, '', false, true)}>{child.name}
                                                </Link>
                                            :
                                                <a key={child.url} href={child.url}
                                                    onClick={() => MyGA.SendEvent('homepage_navigation', 'ln_navigation_explore', 'ln_' + item.id, 'ln_' + child.id, '', false, true)}>{child.name}
                                                </a>
                                    )})
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