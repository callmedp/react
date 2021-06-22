import React from 'react';
import './frequentlyBought.scss';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const FrequentlyBought = (props) => {
    const { addFrqntProd, fbt_list, productName } = props;
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
        <div className="frequently-bought mt-50">
            <h2 className="heading2">Frequently Bought Together</h2>
            <ul className="frequently-bought__list">
                {
                    fbt_list?.map((fbt_data, indx) => {
                        return (
                            <li key={indx}>
                                <label>
                                    <input type="checkbox" id={fbt_data.id} name={`fbt${fbt_data.id}`} onClick={(event) => toggleProduct(event, fbt_data)}/> {fbt_data.heading}
                                    <span className="ml-auto">{fbt_data.inr_price}/-</span>
                                </label>
                            </li>
                        )
                    })
                }
            </ul>
        </div>
    )
}

export default FrequentlyBought;