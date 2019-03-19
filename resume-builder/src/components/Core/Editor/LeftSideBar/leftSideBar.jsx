import React, {Component} from 'react';
import './leftSideBar.scss'
import Edit from '../Edit/edit.jsx'
import Preview from '../Preview/preview.jsx'

export default class LeftSideBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            edit: true
        };
        this.activateEditTab = this.activateEditTab.bind(this);
        this.activatePreviewTab = this.activatePreviewTab.bind(this);
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
        return (

            <section className="left-sidebar">

                <ul className="tab-heading">
                    <li onClick={this.activateEditTab} className={isEdit ? "active" : ''}>
                        <span class="icon-edit"></span>
                        <a href="#">Add/ Edit</a>
                    </li>
                    <li onClick={this.activatePreviewTab} class={!isEdit ? "active" : ''}>
                        <span class="icon-preview"></span>
                        <a href="#">Preview</a>
                    </li>
                </ul>
                {
                    isEdit ? <Edit/> : <Preview/>
                }
            </section>
        )
    }
}