import React from "react";
import { useSelector } from 'react-redux';
import '../../SkillPage/LearnersStories/learnersStories.scss';
import './boostedCareers.scss'
import LearnersStoriesCards from '../../../Common/LearnersStoriesCards/learnersStoriesCards'

const BoostedCareers = () => {
    const { testimonialCategory } = useSelector(store => store.testimonials)
    
    return (
        testimonialCategory?.length ? <LearnersStoriesCards learnersData = {testimonialCategory} page="homePage" /> : ''
    ) 
}

export default BoostedCareers;