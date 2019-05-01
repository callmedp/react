import React, {Component} from 'react';
import './editPreview.scss'
import TopBar from './TopBar/topBar.jsx'
import LeftSideBar from './LeftSideBar/leftSideBar.jsx'
import Header from '../../Common/Header/header.jsx'
import Footer from '../../Common/Footer/footer.jsx'
import RightSection from './RightSection/rightSection.jsx'
import {withRouter} from "react-router-dom";
import {siteDomain} from "../../../Utils/domains";
import LoaderPage from "../../Loader/loaderPage.jsx";

class EditPreview extends Component {
    componentWillMount() {
        if (!localStorage.getItem('token')) {
            window.location.href = `${siteDomain}/login/?next=/resume-builder/`;
            return;
        }
    }

    render() {
        return (
            /*
            * @desc Top Bar component
            * */
            <div>
          {/*      {
            <LoaderPage/>
            }*/}
                <Header/>
                <div className="page-container">
                    <TopBar/>
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

export default withRouter(props => <EditPreview {...props}/>)

