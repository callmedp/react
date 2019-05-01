import React, {Component} from 'react';
import './dataloader.scss'

export default class DataLoader extends Component {
    render() {
        return (
            <div className="dataloader">
                <img src={`/media/static/react/assets/images/mobile/loader.gif`} width="100" height="100" alt=""/>
            </div>
        )
    }
}