import React, {Component} from 'react';
import './loader.scss'

export default class LoaderPage extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'

    }

    componentWillUnmount() {
        let body = document.body;
        body.classList.remove('scrollynone');
    }

    render() {
        let body = document.body;
        body.classList.add('scrollynone')
        return (
            <div className="">
                <div className="loader-page">
                    <span className="loader-img">
                        <img className="" src={`${this.staticUrl}react/assets/images/loader.png`}/>
                        Please wait...
                    </span>
                </div>
            </div>
        )
    }

}