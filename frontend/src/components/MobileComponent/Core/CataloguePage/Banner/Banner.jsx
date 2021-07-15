import React from 'react';
import { Link as LinkScroll } from "react-scroll";
import './Banner.scss';
import useLearningTracking from 'services/learningTracking';

const CatalogBanner = (props) => {

    const sendLearningTracking = useLearningTracking();

    const trackingHandler = (type) => {

        sendLearningTracking({
            productId: '',
            event: `catalogue_page_${type}_clicked`,
            pageTitle:'catalogue_page',
            sectionPlacement: 'banner',
            eventCategory: type,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }


    return (
        <div className="m-container mt-0 mb-10 m-catalog-header">
            <h1 className="m-heading1"><strong className="ml-0">India's largest</strong> e-learning platform</h1>
            <p>Join the club of 4mn learners with our partners like Skillsoft, ACCA etc</p>
            <LinkScroll onClick = { () => trackingHandler('view_categories')} to="categories" className="btn-white-outline-round mr-10">View categories</LinkScroll>
            <LinkScroll onClick = { () => trackingHandler('view_services')} to="services" className="btn-white-outline-round">View services</LinkScroll>
        </div>
    )
}

export default CatalogBanner;