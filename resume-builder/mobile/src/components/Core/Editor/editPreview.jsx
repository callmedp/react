import React, {Component} from 'react';
import './editPreview.scss'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx';
import RightSection from './RightSection/rightSection.jsx';
import Header from '../../Common/Header/header.jsx';
import * as actions from "../../../store/template/actions";
import {connect} from "react-redux";
import {withRouter} from "react-router-dom";

class EditPreview extends Component {

    constructor(props){
        super(props);
    }

    componentDidMount() {
        this.props.fetchTemplate()
    }

    render() {
        return (
            <div className="edit-section">
                <Header page={'edit'}/>
                <LeftSideBar {...this.props}/>
                <RightSection {...this.props}/>
            </div>

        )
    }
}
const mapStateToProps = (state) => {
    return {
        initialValues: state.template,
        template: state.template
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchTemplate": () => {
            return dispatch(actions.fetchTemplate())
        },
        "updateModalStatus": (data) => {
            return dispatch(actions.updateModalStatus(data))
        }
    }
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditPreview))

