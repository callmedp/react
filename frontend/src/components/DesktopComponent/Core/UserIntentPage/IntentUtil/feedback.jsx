import React, {useState} from 'react'
import { sendFeedback } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';
import Button from 'react-bootstrap/Button';

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
