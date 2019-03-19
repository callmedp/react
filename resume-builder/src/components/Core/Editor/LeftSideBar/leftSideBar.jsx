import React, {Component} from 'react';
import './leftSideBar.scss'
import Edit from '../Edit/edit.jsx'
import Preview from '../Preview/preview.jsx'
import {Link} from 'react-router-dom'

export default class LeftSideBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            edit: true
        };
        console.log('---', props)
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

        console.log('props  -> ', this.props);


    }


    activatePreviewTab() {
        this.setState({
            edit: false
        })
    }


    render() {
        const isEdit = this.state.edit;
        return (

            <section className="left-sidebar">

                <ul className="tab-heading">
                    <li className={isEdit ? "active" : ''}>
                        <span className="icon-edit"></span>
                        <Link to="/resume-builder/edit">Add/ Edit</Link>
                    </li>
                    <li className={!isEdit ? "active" : ''}>
                        <span className="icon-preview"></span>
                        <Link to="/resume-builder/preview">Preview</Link>
                    </li>
                </ul>
                {
                    isEdit ? <Edit {...this.props} /> : <Preview {...this.props} />
                }
            </section>
        )
    }
}