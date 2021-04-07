import React from 'react';
import './frequentlyBought.scss';
import {Link} from 'react-router-dom';

const FrequentlyBought = (props) => {

    return (
        <div className="frequently-bought mt-20">
            <h2 className="heading2">Frequently Bought Together</h2>
            <ul className="frequently-bought__list">
                <li>
                    <label><input type="checkbox" /> Cover Letter <span className="ml-auto">1,500/-</span></label>
                </li>
                <li>
                    <label><input type="checkbox" /> Second Regular resume <span className="ml-auto">1,500/-</span></label>
                </li>
            </ul>
        </div>
    )
}

export default FrequentlyBought;