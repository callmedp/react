import React, {useState} from 'react';
import './allCategories.scss';
import { useSelector } from 'react-redux';
import useLearningTracking from 'services/learningTracking';

const AllCategories = (props) => {
    const { categoryList } = useSelector(store => store.allCategories); 
    const sendLearningTracking = useLearningTracking();

    const handleTracking = (name, index) => {
        sendLearningTracking({
            productId: '',
            event: `catalogue_page_${name}_clicked`,
            pageTitle:'catalogue_page',
            sectionPlacement: 'all_categories',
            eventCategory: name,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: index,
        })
    }

    return(
        <section id="m-all-categories" className="m-container m-lightblue-bg mt-0 mb-0" id="categories">
            <div className="m-all-category">
                <h2 className="m-heading2 text-center">All categories</h2>
                <ul className="m-all-category__list">
                    {
                        categoryList?.map((category, index) => {
                            return (
                                <li key={category.pk}>
                                    <div className="m-card">
                                        <figure>
                                            <img src={category.icon_image} className="img-fluid" alt={category.name} />
                                        </figure>
                                        <h3>{category.name}</h3>
                                        <a href={category.url} onClick={() => handleTracking(category.name, index)}>View courses</a>
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