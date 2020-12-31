import React, {useState} from 'react';
import './allCategories.scss';
import { useSelector } from 'react-redux';

const AllCategories = (props) => {
    const { categoryList } = useSelector(store => store.allCategories); 

    return(
        <section id="m-all-categories" className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up" id="categories">
            <div className="m-all-category">
                <h2 className="m-heading2 text-center">All categories</h2>
                <ul className="m-all-category__list">
                    {
                        categoryList?.map((category) => {
                            return (
                                <li key={category.pk}>
                                    <div className="m-card">
                                        <figure>
                                            <img src={category.icon_image} className="img-fluid" alt={category.name} />
                                        </figure>
                                        <h3>{category.name}</h3>
                                        <a href={category.url}>View courses</a>
                                    </div>
                                </li>
                            )
                        })
                    }
                </ul>
            </div>
        </section>
    )
}
   
export default AllCategories;