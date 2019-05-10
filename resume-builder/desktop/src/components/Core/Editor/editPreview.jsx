import React, {Component} from 'react';
import './editPreview.scss'
import TopBar from './TopBar/topBar.jsx'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx'
import Header from '../../Common/Header/header.jsx'
import Footer from '../../Common/Footer/footer.jsx'
import {connect} from 'react-redux';
import RightSection from './RightSection/rightSection.jsx'
import {withRouter} from "react-router-dom";
import {siteDomain} from "../../../Utils/domains";
import LoaderPage from "../../Loader/loaderPage.jsx";

class EditPreview extends Component {

    render() {
        const {ui: {loader}, userInfo: {first_name}} = this.props;
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
                {
                    !!(loader) &&
                     <LoaderPage/>
                }

                <Header userName={first_name}/>
                <div className="page-container">
                    <TopBar {...this.props}/>
                    <section className={'flex-container mt-30'}>
                        <LeftSideBar {...this.props}/>
                        <RightSection {...this.props}/>
                    </section>
                </div>
                <Footer/>

            </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        ui: state.ui,
        userInfo: state.personalInfo
    }
}
export default withRouter(connect(mapStateToProps, null)(EditPreview))

