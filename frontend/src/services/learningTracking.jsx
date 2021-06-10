import React from 'react';
import { useDispatch } from 'react-redux';
import { logLearningTracking } from 'store/LearningTracking/actions';

const useLearningTracking = (props) => {
    const dispatch = useDispatch(logLearningTracking({props}));
    dispatch()

}

export default useLearningTracking;