import React, {Component} from 'react';
import './leftSideBar.scss'
import Edit from '../Edit/edit.jsx'
import Preview from '../Preview/preview.jsx'

export default class LeftSideBar extends Component {
    render() {
        return (
            <section className="left-sidebar">
                <Edit/>
                <Preview/>
            </section>
        )
    }
}