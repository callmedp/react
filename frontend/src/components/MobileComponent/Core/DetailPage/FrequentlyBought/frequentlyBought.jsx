import React, {useState} from 'react';
import './frequentlyBought.scss';

const FrequentlyBought = (props) => {
    const { fbtList, varChecked } = props

    return (
        <section className="m-container m-lightblue-bg mt-20 mb-0" data-aos="fade-up">
            <div className="m-frequently-bought">
                <h2 className="m-heading2">Frequently Bought Together</h2>
                <ul className="m-frequently-bought__list">
                    {
                        fbtList?.map((course, idx) => {
                            return (
                                <li>
                                    <label key={idx}><input type="checkbox"  /> { course?.heading ? course.heading : course.label } <span className="ml-auto"> { course.inr_price }/-</span></label>
                                </li>
                            )
                        })
                    }
                </ul>
            </div>
        </section>
    )
}


export default FrequentlyBought;