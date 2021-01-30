import React, {useState} from 'react';
import './ourLearners.scss';
import { Link } from 'react-router-dom';

   
const OurLearners = (props) => {
    return(
        <section className="container-fluid lightblue-bg mt-50 mb-0" data-aos="fade-up">
            <div className="row"> 
                <div className="container">
                    <div className="row">
                        <h2 className="heading2 text-center mx-auto mt-50">Our learners are now at these amazing places</h2>
                        <div className="our-vendors mb-50">
                            <figure>
                                <img src="./media/images/logo-google.png" className="img-fluid" alt="Google" />
                            </figure>
                            <figure>
                                <img src="./media/images/logo-ibm.png" className="img-fluid" alt="IBM" />
                            </figure>
                            <figure>
                                <img src="./media/images/logo-infosys.png" className="img-fluid" alt="Infosys" />
                            </figure>
                            <figure>
                                <img src="./media/images/logo-genpact.png" className="img-fluid" alt="Genpact" />
                            </figure>
                            <figure>
                                <img src="./media/images/logo-fujitsu.png" className="img-fluid" alt="Fujitsu" />
                            </figure>
                            <figure>
                                <img src="./media/images/logo-people-strong.png" className="img-fluid" alt="People Strong" />
                            </figure>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}
   
export default OurLearners;