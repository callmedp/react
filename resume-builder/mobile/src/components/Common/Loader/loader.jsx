import React, {Component} from 'react';
import './loader.scss'

export default class Loader extends Component {
    render() {
        return (
            <div className="loader">
                <img src={`/media/static/react/assets/images/mobile/loader.gif`} width="100" height="100" alt=""/>
            </div>
        )
    }
}