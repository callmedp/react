import React from 'react';
import './frequentlyBought.scss';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const FrequentlyBought = (props) => {
    const { fbtList, addFrqntProd, productName } = props;
    const frqntProd = props.frqntProd;
    const sendLearningTracking = useLearningTracking();

    const toggleProduct = (event, item) => {
        let eventString = "";

        if(event.target.checked) {
            addFrqntProd([...frqntProd, item]);
            eventString = `course_detail_frequently_bought_${stringReplace(item?.heading ? item.heading : item.label)}_${item.id}_added_to_${stringReplace(productName)}`;
        }
        else {
            addFrqntProd(frqntProd => frqntProd.filter(prd => prd.id != event.target.id));
            eventString = `course_detail_frequently_bought_${stringReplace(item?.heading ? item.heading : item.label)}_${item.id}_removed_from_${stringReplace(productName)}`;
        }

        sendLearningTracking({
            productId: '',
            event: eventString,
            pageTitle:'course_detail',
            sectionPlacement: 'frequently_bought',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
        <section className="m-container m-lightblue-bg mt-20 mb-0" data-aos="fade-up">
            <div className="m-frequently-bought">
                <h2 className="m-heading2">Frequently Bought Together</h2>
                <ul className="m-frequently-bought__list">
                    {
                        fbtList?.map((course, idx) => {
                            return (
                                <li key={idx}>
                                    <label key={idx}><input type="checkbox" id={course.id} name={`fbt${course.id}`} onClick={(event) => toggleProduct(event, course)} /> { course?.heading ? course.heading : course.label } <span className="ml-auto"> { course.inr_price }/-</span></label>
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