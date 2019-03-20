import React, {Component} from 'react';
import './edit.scss'
import LeftSideBar from '../LeftSideBar/leftSideBar.jsx';

export default class Edit extends Component {

    render() {
        return (
            <div className="edit-section">
                Edit
                <LeftSideBar/>
            </div>

        )
    }

}