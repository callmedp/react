import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import './startCourse.scss';
import { startDashboardCoursesPageLoader, 
    stopDashboardCoursesPageLoader } from 'store/Loader/actions/index';
import { getVendorUrl } from 'store/DashboardPage/StartCourse/actions/index';
import { getCandidateId } from 'utils/storage.js';
import {Link, useLocation} from "react-router-dom";
import Loader from '../../../Common/Loader/loader';
import Iframe from 'react-iframe';
import { useHistory } from "react-router-dom";

const StartCourse = (props) => {
    const location = useLocation();
    const { history } = props;
    const { url } = location;
    const [showLoader, setShowLoader] = useState(true);
    const handleClose = () => setShowLoader(false);
    if(url === undefined || url === ''){
        history.push("/404/")
    }

    return (
        <div className="m-full-screen">
            { showLoader ? <Loader /> : null}
            <Iframe url={url}
            onLoad={handleClose} />
        </div>

    );
}

export default StartCourse;