import React, {Component} from 'react';
import './loader.scss'

export default class  extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }

    render() {
        return (
            <div className="pr">

                <div className="loader">
                    <img class="img-responsive" src={`${this.staticUrl}react/assets/images/loader.gif`}/>
                </div>

            </div>
        )
    }

}