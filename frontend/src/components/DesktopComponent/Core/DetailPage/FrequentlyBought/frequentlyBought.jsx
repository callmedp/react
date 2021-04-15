import React from 'react';
import './frequentlyBought.scss';

const FrequentlyBought = (props) => {
    const {addFrqntProd, fbt_list} = props;
    const frqntProd = props.frqntProd;

    const toggleProduct = (event, item) => {
        if(event.target.checked) {
            addFrqntProd([...frqntProd, item]);
        }
        else {
            addFrqntProd(frqntProd => frqntProd.filter(prd => prd.id != event.target.id));
        }
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