import React, {Component} from 'react';
import './loader.scss'

export default class  extends Component {

    render() {
        return (
            <div>

                <div className="loader">
                	<img class="img-responsive" src={`${this.staticUrl}react/assets/images/loader.gif`}/>
                </div>

            </div>
        )
    }

}