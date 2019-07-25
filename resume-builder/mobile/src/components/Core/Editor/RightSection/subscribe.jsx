import React,{Component} from 'react';
import './rightSection.scss'


export default class Subscribe extends Component{
    render() {
        return (
            <div>
                <div className="buildResume__subscribe">
                    <p className="buildResume__subscribe--text">Subscribe now create later</p>
                    <a href="#" className="btn btn__sm btn__round btn--outline">Subscribe</a>
                    <a className="close" href="javascript:void(0)">+</a>
                </div>
            </div>
        )
    }
}


