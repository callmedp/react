import React from 'react';
import '../../SkillPage/WhoLearn/whoLearn.scss';

const WhoLearn = (props) => {

    const { prd_lrn_data } = props

    return (
        <section className="container-fluid">
            <div className="row">
                <div className="container">
                    <div className="who-learn">
                        <h2 className="heading2 mt-10">Who should learn?</h2>
                        <ul className="mt-30 mb-20">
                            <p dangerouslySetInnerHTML={{__html : prd_lrn_data }}></p>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
}


export default WhoLearn;