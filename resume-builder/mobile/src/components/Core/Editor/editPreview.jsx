import React, {Component} from 'react';
import './editPreview.scss'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx';
import RightSection from './RightSection/rightSection.jsx';
import Header from '../../Common/Header/header.jsx';
import {withRouter} from "react-router-dom";

class EditPreview extends Component {

    constructor(props){
        super(props);
    }

    sideBarStatus = (value) => {
        this.setState({sidebar_open: value});
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

export default withRouter(props => <EditPreview {...props}/>)