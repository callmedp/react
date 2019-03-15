import React, {Component} from 'react';
import './editPreview.scss'
import TopBar from '../TopBar/topBar.jsx'
import LeftSideBar from '../LeftSideBar/leftSideBar.jsx'
import Header from '../../../Common/Header/header.jsx'
import Footer from '../../../Common/Footer/footer.jsx'

export default class EditPreview extends Component {
    render() {
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
                <Header/>
                <div>
                    <div>
                        <TopBar/>
                        <LeftSideBar/>
                        {/*<RightSection/>*/}
                    </div>
                </div>
                <Footer/>

            </div>
        )
    }

}