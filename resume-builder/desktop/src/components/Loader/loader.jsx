import React, {Component} from 'react';
import './loader.scss'

export default class  extends Component {

    render() {
        return (
            <div style={{
                'display': 'flex', 'align-items': 'center', position: 'absolute'
                , 'justify-content': 'center', 'flex-direction': 'column', 'height': '70%',
                'width': '65%', 'z-index': '2'
            }}>
                <div className="lds-dual-ring"></div>
            </div>
        )
    }

}