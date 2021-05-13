import React from 'react';
import './whoLearn.scss'

const WhoLearn = (props) => {

    const { prd_lrn_data } = props

    return (
        <section className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up">
            <div className="m-who-learn">
                <h2 className="m-heading2">Who should learn?</h2>
                <p dangerouslySetInnerHTML={{__html : prd_lrn_data }} />
            </div>
        </section>
    )
}


export default WhoLearn;