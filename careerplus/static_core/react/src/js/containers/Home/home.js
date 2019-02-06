import React from 'react';
import {connect} from "react-redux";
import * as actions from '../../store/home/actions/index';
import Home from '../../components/Home/Home';

const mapStateToProps = (state) => {
    return {
        pinCode: state.homeReducer["pinCode"],

    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userDetails) => new Promise((resolve, reject) => {
            dispatch(actions.saveUserDetails({userDetails, resolve, reject}))
        })
}

};

const HomeContainer = connect(mapStateToProps, mapDispatchToProps)(Home);

export default HomeContainer;