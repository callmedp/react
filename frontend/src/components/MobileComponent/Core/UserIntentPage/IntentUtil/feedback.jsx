import React, {useState} from 'react'
import { sendFeedback } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';
import { getCandidateId } from 'utils/storage.js';

const Feedback = props => {

    const [feedback, setFeedback] = useState(false)
    const dispatch = useDispatch()
    const {feedbackData : {intent, recommended_course_ids, context}, heading} = props;
    const handleFeedback = async (eve) => {
		eve.preventDefault();
		setFeedback(true);
		const feedData = {
            "intent": intent,
            'candidate_id': getCandidateId(),
            "recommendation_relevant": eve.target.innerHTML === 'Yes' ? true : false,
            "recommended_products": recommended_course_ids.join(),
            "context": context
        }
        await new Promise(() => dispatch(sendFeedback({ feedData })));
	}


    return (
        feedback ? (
            <div className="courses-feedback mr-15p">
                <strong>Thanks for your feedback!</strong>
            </div>
        ) : (
                <div className="m-courses-feedback">
                    <strong>Are these {heading} recommendation relevant to your profile?</strong>
                    <span className="mt-15">
                        <a className="btn-blue-outline" onClick={handleFeedback}>Yes</a>
                        <a className="btn-blue-outline" onClick={handleFeedback}>No</a>
                    </span>
                </div>
            )
    )
}

export default Feedback;
