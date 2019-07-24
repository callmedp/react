import React,{Component} from 'react';
import './rightSection.scss'


export default class Subscribe extends Component{
    constructor(props){
        super(props);
        this.redirectToBuyPage = this.redirectToBuyPage.bind(this);
    }
    redirectToBuyPage(){
        const {history, eventClicked} = this.props;
        eventClicked({
            'action':'SubscribeNow',
            'label':'Click'
        })
        history.push('/resume-builder/buy');
    }
    render() {
        return (
            <div>
                <div className="buildResume__subscribe">
                    <p className="buildResume__subscribe--text">Subscribe now create later</p>
                    <a onClick={this.redirectToBuyPage} className="btn btn__sm btn__round btn--outline">Subscribe</a>
                </div>
            </div>
        )
    }
}


