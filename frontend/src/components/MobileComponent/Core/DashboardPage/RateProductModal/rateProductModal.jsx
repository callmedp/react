import React, { useEffect, useState } from 'react';

const RateProductModal = (props) => {
    const { setShowRateModal } = props
    const [showRatingModal, setShowRatingModal] = useState(false)
    const [showAllRatings, setShowAllRatings] = useState(true)

    return (
        <div className="m-slide-modal">
            {
                showRatingModal &&
                    <div className="text-center">
                        <span className="m-db-close" onClick={() => {setShowRateModal(false)}}>X</span>
                        <h2>Add comment</h2>
                        <div className="m-enquire-now mt-15">
                            <div className="m-form-group">
                                <textarea id="addComments" placeholder=" " rows="4"></textarea>
                                <label htmlFor="addComments">Enter comment here</label>
                            </div>

                            <button className="btn btn-blue">Submit</button>
                        </div>
                    </div>
            }

            {
                showAllRatings && 
                <div className="addcomments" style={{display: 'block'}}>
                    <span className="m-db-close" style={{ marginLeft: '13px' }} onClick={() => {setShowRateModal(false)}}>X</span>
                    
                    <div className="m-reviews-list">
                        <ul>
                            <li>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>4</strong> /5</span>
                                    </span>
                                </div>

                                <span className="m-reviews-list--date">Dec. 21, 2020</span>
                                <p className="m-reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
                            </li>
                            
                            <li>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>4</strong> /5</span>
                                    </span>
                                </div>

                                <span className="m-reviews-list--date">Oct. 14, 2020</span>
                                <p className="m-reviews-list--text">Good Mentors with good experience</p>
                            </li>
                            <li>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>4</strong> /5</span>
                                    </span>
                                </div>

                                <span className="m-reviews-list--date">Dec. 21, 2020</span>
                                <p className="m-reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
                            </li>
                            
                            <li>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>4</strong> /5</span>
                                    </span>
                                </div>

                                <span className="m-reviews-list--date">Oct. 14, 2020</span>
                                <p className="m-reviews-list--text">Good Mentors with good experience</p>
                            </li>
                        </ul>
                    </div>
                    
                    <div className="m-reviews-list-wrap--bottom">
                        <button className="btn btn-blue-outline px-30" onClick={() => {setShowAllRatings(false);setShowRatingModal(true)}}>Add new</button>
                    </div>
                </div>
            }

        </div>
    )
}

export default RateProductModal;