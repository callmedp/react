import React, {useState} from 'react';
import './frequentlyBought.scss';
import {Link} from 'react-router-dom';

const FrequentlyBought = (props) => {
    return (
        <section className="m-container m-lightblue-bg mt-20 mb-0" data-aos="fade-up">
            <div className="m-frequently-bought">
                <h2 className="m-heading2">Frequently Bought Together</h2>
                <ul className="m-frequently-bought__list">
                    <li>
                        <label><input type="checkbox" /> Cover Letter <span className="ml-auto">1,500/-</span></label>
                    </li>
                    <li>
                        <label><input type="checkbox" /> Second Regular resume <span className="ml-auto">1,500/-</span></label>
                    </li>
                </ul>
            </div>
        </section>
    )
}


export default FrequentlyBought;