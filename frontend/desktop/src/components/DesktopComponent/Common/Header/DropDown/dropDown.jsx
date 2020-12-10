import React, { useState } from 'react';


const DropDown = (props) => {

    const { tabList } = props;
    const [activeTab, setActiveTab ] = useState(tabList?.[0].id)

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
                            href={item.url}>
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
                            item.children.map( child => <a key={child.url} href={child.url}>{child.name}</a> )
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