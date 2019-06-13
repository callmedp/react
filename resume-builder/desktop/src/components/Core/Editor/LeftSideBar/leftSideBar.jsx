import React, {Component} from 'react';
import './leftSideBar.scss'
import Edit from './Edit/edit.jsx'
import Preview from './Preview/preview.jsx'
import {Link} from 'react-router-dom'

export default class LeftSideBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            edit: true
        };
        this.activateEditTab = this.activateEditTab.bind(this);
        this.activatePreviewTab = this.activatePreviewTab.bind(this);
        const path = this.props.match.path;
        if (path === '/resume-builder/edit/') this.state.edit = true;
        else this.state.edit = false;
    }

    activateEditTab() {
        this.setState({
            edit: true
        })

    }

    activatePreviewTab() {
        this.setState({
            edit: false
        })
    }


    render() {
        const isEdit = this.state.edit;
        const newUser = localStorage.getItem('newUser')
        const {showAlertModal} = this.props
        return (

            <section className="left-sidebar">

                <ul className="tab-heading">
                    <li className={
                        ' tab-heading--top-left-radius ' + (isEdit ? "active" : 'no-shadow')}>
                        <span className="icon-edit"></span>
                        <Link to="/resume-builder/edit">Add/ Edit</Link>
                    </li>
                    <li className={' tab-heading--top-right-radius ' +
                    (!isEdit ? "active" : 'no-shadow')}>
                        <span className="icon-preview"></span>
                        {newUser ? <a onClick={showAlertModal}>Preview</a> :
                            <Link to="/resume-builder/preview">Preview</Link>
                         }
                    </li>
                </ul>
                {
                    isEdit ? <Edit {...this.props} /> : <Preview {...this.props} />
                }
            </section>  
        )
    }
}