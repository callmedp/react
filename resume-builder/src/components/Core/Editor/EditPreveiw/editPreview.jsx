import React, {Component} from 'react';
import './editPreview.scss'
import TopBar from '../TopBar/topBar.jsx'
import LeftSideBar from '../LeftSideBar/leftSideBar.jsx'
import Header from '../../../Common/Header/header.jsx'
import Footer from '../../../Common/Footer/footer.jsx'
import RightSection from '../RightSection/rightSection.jsx'

export default class EditPreview extends Component {
    render() {
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
                <Header/>
                <div className="page-container">
                    <TopBar/>
                    <section className="flex-container">
                        <LeftSideBar/>
                        <RightSection/>
                    </section>
                </div>
                <Footer/>

            </div>
        )
    }

}