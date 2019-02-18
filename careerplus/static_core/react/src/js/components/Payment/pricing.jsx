import React from 'react';
import PropTypes from 'prop-types';
import {connect} from "react-redux";

export class Pricing extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                Handle Pricing here
            </div>
        );
    }
}


const mapStateToProps = (state) => {
    return {}
};

const mapDispatchToProps = (dispatch) => {
    return {}
};

export default connect(mapStateToProps, mapDispatchToProps)(Pricing);

