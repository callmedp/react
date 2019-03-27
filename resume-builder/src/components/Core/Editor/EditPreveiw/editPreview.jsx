import React, {Component} from 'react';
import './editPreview.scss'
import TopBar from '../TopBar/topBar.jsx'
import LeftSideBar from '../LeftSideBar/leftSideBar.jsx'
import Header from '../../../Common/Header/header.jsx'
import Footer from '../../../Common/Footer/footer.jsx'
import RightSection from '../RightSection/rightSection.jsx'
import {withRouter} from "react-router-dom";

class EditPreview extends Component {
    constructor(props) {
        super(props)
        this.myRef = React.createRef();
        this.state = {
        fixed: false
    }
        this.handleScroll = this.handleScroll.bind(this);
    }
    componentDidMount(){
        window.addEventListener('scroll', this.handleScroll);

}

    handleScroll(){
    const section = this.myRef.current;
    console.log('seciton', window.pageYOffset, window.innerHeight);
    if (window.pageYOffset >= window.innerHeight)
            this.setState({
            fixed: true
        })
    else 
            this.setState({
            fixed: false
        })
}

    render() {
        return (
            /*
            * @desc Top Bar component
            * */
            <div id="wrap">
                <Header/>
                <div className="page-container">
                    <TopBar/>
                    <section className={'flex-container mt-30 '+ (this.state.fixed ? 'fixed': '' )} ref={this.myRef}>
                        <LeftSideBar {...this.props}/>
                        <RightSection {...this.props}/>
                    </section>
                </div>
                <Footer/>

            </div>
        )
    }

}

export default withRouter(props => <EditPreview {...props}/>)

