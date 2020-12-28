import React, {useState} from 'react';
import './ourVendors.scss';
import { Link } from 'react-router-dom';

   
const OurVendors = (props) => {
    return(
        <section className="container mt-30" data-aos="fade-up">
            <div className="row"> 
                <h2 className="heading2 text-center mx-auto">Our Vendors</h2>
                <div className="our-vendors">
                    <figure>
                        <img src="./media/images/shine-learning-vendor.png" className="img-fluid" alt="Shine Learning" />
                    </figure>
                    <figure>
                        <img src="./media/images/361minds-vendor.png" className="img-fluid" alt="Shine Learning" />
                    </figure>
                    <figure>
                        <img src="./media/images/vskills-vendor.png" className="img-fluid" alt="Shine Learning" />
                    </figure>
                    <figure>
                        <img src="./media/images/skillsoft-vendor.png" className="img-fluid" alt="Shine Learning" />
                    </figure>
                    <figure>
                        <img src="./media/images/edurekha-vendor.png" className="img-fluid" alt="Shine Learning" />
                    </figure>
                </div>
            </div>
        </section>
    )
}
   
export default OurVendors;