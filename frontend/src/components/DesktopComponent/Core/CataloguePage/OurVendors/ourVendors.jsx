import React from 'react';
import './ourVendors.scss';
import { useSelector } from 'react-redux';

   
const OurVendors = (props) => {

    const { vendorList } = useSelector( store => store.allCategories) 

    return(
        <section className="container mt-30" data-aos="fade-up">
            <div className="row"> 
                <h2 className="heading2 text-center mx-auto">Our Vendors</h2>
                <div className="our-vendors">
                    {
                        vendorList?.slice(0,4).map( (vendor, index) => {
                            return (
                                <figure key={index}>
                                <img src={vendor.icon_image} className="img-fluid" alt={vendor.name} />
                            </figure>
                            )
                        })
                    }    
                </div>
            </div>
        </section>
    )
}
   
export default OurVendors;