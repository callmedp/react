import React, {Component} from 'react';
import './loader.scss'

export default class LoaderPage  extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }

    render() {
        return (
            <div className="">

                <div className="loader-page">
                    <span className="loader-img">
                        <img className="" src={`${this.staticUrl}react/assets/images/loader.png`}/><br/>
                        Loading... <br/>please wait
                    </span>
                </div>

            </div>
        )
    }

}