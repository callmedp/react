import { useDispatch } from 'react-redux';
import { logLearningTracking } from 'store/LearningTracking/actions';

const useLearningTracking = () => {
    const dispatch = useDispatch();
    console.log("use learning tracking initiated")
    return (props) => {
        console.log("use learning dispatch initiated", props)
        dispatch(logLearningTracking(props))
    }
}   

export default useLearningTracking;