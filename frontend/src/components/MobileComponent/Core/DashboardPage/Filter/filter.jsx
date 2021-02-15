import React from 'react';
import { Link } from 'react-router-dom';
import './filter.scss';


const Filters = (props) => {
    return(
        <div className="filters">
            <span>Filter by</span>
            <div className="filters__box last-month open">
                <ul>
                    <li className="filters__box--item">Last eighteen months</li>
                    <li className="filters__box--item">Last six month</li>
                    <li className="filters__box--item">Last three months</li>
                </ul>
            </div>

            <div className="filters__box all-item">
                <ul>
                    <li className="filters__box--item">All items</li>
                    <li className="filters__box--item">In process</li>
                    <li className="filters__box--item">Closed</li>
                </ul>
            </div>
        </div>
    )
}

export default Filters;