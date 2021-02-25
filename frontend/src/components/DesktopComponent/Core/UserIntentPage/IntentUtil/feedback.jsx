import React, {useState} from 'react'
import { sendFeedback } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';
import Button from 'react-bootstrap/Button';
import { getCandidateId } from 'utils/storage.js';

const Feedback = props => {

    const [feedback, setFeedback] = useState(false)
    const dispatch = useDispatch()
    const {feedbackData : {intent, recommended_course_ids, context}} = props;

    const handleFeedback = async (eve) => {
        eve.preventDefault();
        setFeedback(true);
        const feedData = {
            "intent": intent,
            'candidate_id': getCandidateId(),
            "recommendation_relevant": eve.target.innerHTML === 'Yes' ? true : false,
            "recommended_products": recommended_course_ids,
            "context": context
        }
        await new Promise(() => dispatch(sendFeedback({ feedData })));
	}


    return (
        feedback ? (
            <div className="courses-feedback mt-50 mr-15p">
                <strong>Thanks for your feedback!</strong>
            </div>
        ) : (
                <div className="courses-feedback mt-50 mr-15p">
                    <strong>Are these courses recommendation relevant to your profile?</strong>
                    <span className="ml-auto">
                        <Button onClick={handleFeedback} variant="outline-primary">Yes</Button>{' '}
                        <Button onClick={handleFeedback} variant="outline-primary">No</Button>{' '}
                    </span>
                </div>
            )
    )
}

export default Feedback;
