import React from 'react';
import './frequentlyBought.scss';

const FrequentlyBought = (props) => {
    const { fbtList, addFrqntProd } = props;
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
        <section className="m-container m-lightblue-bg mt-20 mb-0" data-aos="fade-up">
            <div className="m-frequently-bought">
                <h2 className="m-heading2">Frequently Bought Together</h2>
                <ul className="m-frequently-bought__list">
                    {
                        fbtList?.map((course, idx) => {
                            return (
                                <li>
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