import React from 'react';
import PropTypes from 'prop-types';
import * as action from '../../store/userInfo/actions'
import {connect} from "react-redux";

export class Pricing extends React.Component {
    constructor(props) {
        super(props);
    }

    async redirectToCart() {
        await this.props.addToCart();
        window.location.href = '/cart'
    }

    render() {
        return (
            <div>
                <span> Handle Pricing here</span>
                <p>Welcome</p>
                <button onClick={this.redirectToCart.bind(this)}>Go to Cart</button>
            </div>
        );
    }
}


const mapStateToProps = (state) => {
    return {}
};

const mapDispatchToProps = (dispatch) => {
    return {
        'addToCart': () => {
            return dispatch(action.addToCart())
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Pricing);

