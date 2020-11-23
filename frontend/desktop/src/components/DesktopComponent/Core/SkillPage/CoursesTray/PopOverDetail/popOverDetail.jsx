import React from 'react';
import Popover from 'react-bootstrap/Popover';

const PopOverDetail = () => (
    <Popover className="courses-popover" id="popover-basic">
        <Popover.Content>
            <p className="type">Type: <strong>Certification</strong>  |   <strong>Course level:</strong> Intermediate
    <br /><strong>2819</strong> Jobs available
    </p>
            <p>
                <strong>About</strong>
        This Course is intended for professionals and graduates wanting to excel in their chosen areas.
    </p>
            <p>
                <strong>Skills you gain</strong>
        Content Marketing  |  Email Marketing  |  Adwords Social Media  |  SEO  |  Copywriting  |  Digital Marketing
    </p>
            <p>
                <strong>Highlights</strong>
                <ul>
                    <li>Anytime and anywhere access</li>
                    <li>Become a part of Job centre</li>
                    <li>Lifetime course access</li>
                    <li>Access to online e-learning</li>
                </ul>
            </p>
            <button type="submit" className="btn btn-inline btn-secondary mx-auto" role="button">Enroll now</button>
        </Popover.Content>
    </Popover>
);


export default PopOverDetail;