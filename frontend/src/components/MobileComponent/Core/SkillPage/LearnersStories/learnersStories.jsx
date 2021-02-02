import React from "react";
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
// import './learnersStories.scss';
import { useSelector } from 'react-redux';
import LearnersStoriesCards from '../../../Common/LearnersStoriesCards/learnersStoriesCards';

const LearnersStories = (props) => {
    const { testimonialCategory } = useSelector(store => store.skillBanner)
    
    return (
        testimonialCategory?.length ? <LearnersStoriesCards learnersData = {testimonialCategory} /> : ''
    )
  }

export default LearnersStories;