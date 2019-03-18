import React, {Component} from 'react';
import './leftSideBar.scss'
import Edit from '../Edit/edit.jsx'
import Preview from '../Preview/preview.jsx'

export default class LeftSideBar extends Component {
    render() {
        return (
            <section className="left-sidebar">
            <ul className="tab-heading">
                	<li>
                		<span class="edit-icon"></span>
                		<a href="#">Add/ Edit</a>
                	</li>
                	<li class="active">
                		<span class="preview-icon"></span>
                		<a href="#">Preview</a>
                	</li>
                </ul>
{/*                <Edit/>
*/}
                <Preview/>

            </section>
        )
    }
}