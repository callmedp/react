import React, {Component} from 'react';
import './edit.scss'
import LeftSideBar from '../LeftSideBar/leftSideBar.jsx';
import RightSection from '../RightSection/rightSection.jsx';
import Header from '../../../Common/Header/header.jsx';
export default class Edit extends Component {

    render() {
        return (
            <div className="edit-section">
                <Header/>
                <LeftSideBar/>
                <RightSection/>
            </div>

        )
    }
}