import React, {Component} from 'react';
import './dataloader.scss'

export default class DataLoader extends Component {

    componentDidMount(){
        document.body.classList.add('loader-overflow')
    }

    componentWillUnmount(){
        document.body.classList.remove('loader-overflow')
    }
    
    render() {
        return (
            <div className="dataloader">
                <div className="dataloader--data">
                    <img src={`/media/static/react/assets/images/mobile/loader.png`} width="64" height="64" alt=""/>
                    <p>Processing <br/>please wait....</p>
                </div>
            </div>
        )
    }
}