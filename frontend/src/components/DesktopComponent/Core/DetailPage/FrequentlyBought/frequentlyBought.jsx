import React from 'react';
import './frequentlyBought.scss';
import {Link} from 'react-router-dom';

const FrequentlyBought = (props) => {
    const {frqntProd, addFrqntProd, fbt_list} = props;

    // const fbt = props.frqntProd;

    const selectFrqtProd = () => {
        fbt_list.map((item) => {
            if (!frqntProd.length) {
                frqntProd.push(item);
                addFrqntProd(frqntProd);
            }
            else {
                if (frqntProd.filter((prd) => { return prd.id == item.id }).length) {
                    addFrqntProd(frqntProd.filter((prd) => { return prd.id != item.id }));
                }
                else {
                    frqntProd.push(item);
                    addFrqntProd(frqntProd);
                }
            }
        })
    }

    return (
        <div className="frequently-bought mt-20">
            <h2 className="heading2">Frequently Bought Together</h2>
            <ul className="frequently-bought__list">
                {
                    fbt_list?.map((fbt_data, indx) => {
                        return (
                            <li key={indx}>
                                <label><input type="checkbox" name={`fbt${fbt_data.id}`} onChange={() => selectFrqtProd()}/> {fbt_data.heading} <span className="ml-auto">{fbt_data.inr_price}/-</span></label>
                            </li>
                        )
                    })
                }
                {/* <li>
                    <label><input type="checkbox" /> Cover Letter <span className="ml-auto">1,500/-</span></label>
                </li> */}
                {/* <li>
                    <label><input type="checkbox" /> Second Regular resume <span className="ml-auto">1,500/-</span></label>
                </li> */}
            </ul>
        </div>
    )
}

export default FrequentlyBought;