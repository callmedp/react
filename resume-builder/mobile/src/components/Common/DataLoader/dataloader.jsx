import React, {Component} from 'react';
import './dataloader.scss'

export default class DataLoader extends Component {
    render() {
        return (
            <div className="dataloader">
                <div className="dataloader--data">
                    <img src={`/media/static/react/assets/images/mobile/loader.gif`} width="100" height="100" alt=""/>
                    <p>Processing <br/>please wait....</p>
                </div>
            </div>
        )
    }
}