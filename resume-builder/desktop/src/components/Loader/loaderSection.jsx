import React, {Component} from 'react';
import './loader.scss'

export default class LoaderSection extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }

    render() {
        return (
            <div className="loader-section">
                <img className="" src={`${this.staticUrl}react/assets/images/loader.gif`}/>
                
            </div>
        )
    }

}