import React, { Component } from 'react';
import PropTypes from 'prop-types';

const Card = {(property)} => {
    const {index, picture, altText} = property;

    return(
        <div id={`card-${index}`} className="card">
            <img src={picture} alt={altText} />
        </div>
    )
}

Card.PropTypes = {
    property: PropTypes.object.isRequired
}

export default Card;