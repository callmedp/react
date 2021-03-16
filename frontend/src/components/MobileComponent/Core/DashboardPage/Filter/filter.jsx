import React, { useState } from 'react';
import './filter.scss';

const Filters = (props) => {

    const { filterState, setfilterState } = props
    const [type, setType] = useState(false)
    const [openType, setOpenType] = useState(false)
    const [month, setMonth] = useState('All')
    const [selectType, setSelectType] = useState('All items')
    const [dynamicClass, setDynamicClass] = useState('filters__box last-month')
    const [dynamicClassType, setDynamicClassType] = useState('filters__box all-item')

    const handleOpen = () => {
        if(!type) {
            setDynamicClass('filters__box last-month open');
        }
        else {
            setDynamicClass('filters__box last-month');
        }
        setType(!type)
    }

    const handleOpenType = () => {
        if(!openType) {
            setDynamicClassType('filters__box all-item open');
        }
        else {
            setDynamicClassType('filters__box all-item');
        }
        setOpenType(!openType)
    }

    const handleMonthFilter = (e, monthFilter) => {
        if(e.target.textContent != month){
            setMonth(e.target.textContent)
            setfilterState({ ...filterState, 'last_month_from': monthFilter })
        }
    }

    const handleOrderFilter = (e, itemType) => {
        if(e.target.textContent != selectType){
            setSelectType(e.target.textContent)
            setfilterState({ ...filterState, 'select_type': itemType })
        }
    }

    return(
        <div className="filters">
            <span>Filter by</span>
            <div className={dynamicClass} onClick={ () => handleOpen() }>
                <ul>
                    <li className="filters__box--item">{month}</li>
                    <li className="filters__box--item" onClick={(e) => handleMonthFilter(e, 'all')}>All</li>
                    <li className="filters__box--item" onClick={(e) => handleMonthFilter(e, '18')}>Last eighteen months</li>
                    <li className="filters__box--item" onClick={(e) => handleMonthFilter(e, '6')}>Last six months</li>
                    <li className="filters__box--item" onClick={(e) => handleMonthFilter(e, '3')}>Last three months</li>
                </ul>
            </div>

            <div className={dynamicClassType} onClick={ () => handleOpenType() }>
                <ul>
                    <li className="filters__box--item">{selectType}</li>
                    <li className="filters__box--item" onClick={(e) => handleOrderFilter(e, 'all')} >All items</li>
                    <li className="filters__box--item" onClick={(e) => handleOrderFilter(e, 'in_process')} >In process</li>
                    <li className="filters__box--item" onClick={(e) => handleOrderFilter(e, 'closed')} >Closed</li>
                </ul>
            </div>
        </div>
    )
}

export default Filters;