import React from 'react';
import { Link } from 'react-router-dom';
import './campaignHeader.scss';
import { imageUrl } from 'utils/domains';

const Header = () => {
    return(
        <div className="d-flex m-ja-header">
            <strong className="m-heading2">
                <Link to={""}>
                    <img src={`${imageUrl}mobile/shine-learning-logo.png`} alt="Shine Learning" className="img-fluid" />
                </Link>
            </strong>
        </div>
    )
}

export default Header;