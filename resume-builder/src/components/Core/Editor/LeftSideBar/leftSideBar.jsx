import React, {Component} from 'react';
import './leftSideBar.scss'
import Edit from '../Edit/edit.jsx'
import Preview from '../Preview/preview.jsx'

export default class LeftSideBar extends Component {
    render() {
        return (
            <section className="left-sidebar">
            <ul className="tab-heading">
                	<li class="active">
                		<span class="icon-edit"></span>
                		<a href="#">Add/ Edit</a>
                	</li>
                	<li>
                		<span class="icon-preview"></span>
                		<a href="#">Preview</a>
                	</li>
                </ul>
                <Edit/>

{/*                <Preview/>
*/}
            </section>
        )
    }
}