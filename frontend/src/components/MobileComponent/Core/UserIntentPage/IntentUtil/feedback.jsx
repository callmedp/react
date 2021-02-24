import React, {useState} from 'react'
import { sendFeedback } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';

const Feedback = props => {

    const [feedback, setFeedback] = useState(false)
    const dispatch = useDispatch()

    const handleFeedback = (eve) => {
		eve.preventDefault();
		setFeedback(true);
		dispatch(sendFeedback())
	}


    return (
        feedback ? (
            <div className="courses-feedback mr-15p">
                <strong>Thanks for your feedback!</strong>
            </div>
        ) : (
                <div className="m-courses-feedback">
                    <strong>Are these courses recommendation relevant to your profile?</strong>
                    <span className="mt-15">
                        <a className="btn-blue-outline" onClick={handleFeedback}>Yes</a>
                        <a className="btn-blue-outline" onClick={handleFeedback}>No</a>
                    </span>
                </div>
            )
    )
}

export default Feedback;
