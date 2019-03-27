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
            fixed: false,
            offset: 0
        }
        this.handleScroll = this.handleScroll.bind(this);
    }

    componentDidMount() {
        window.addEventListener('scroll', this.handleScroll);

    }

    handleScroll() {
        const section = this.myRef.current;
        if (window.pageYOffset >= window.innerHeight && section.className) {
            section.className = 'flex-container mt-30 fixed';
        }
        else
            section.className = 'flex-container mt-30'
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
                    <section className={'flex-container mt-30'} ref={this.myRef}>
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

