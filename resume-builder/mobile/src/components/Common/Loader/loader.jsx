import React, {Component} from 'react';
import './loader.scss'

export default class Loader extends Component {
    render() {
        return (
            <div className="loader">
                <div className="loader__wrap">
                <img src={`/media/static/react/assets/images/mobile/loader.png`} width="64" height="64" alt=""/>
                <p>Please wait....</p>
                </div>
            </div>
        )
    }
}