import React, { useState, useEffect } from 'react';
import { Route } from 'react-router-dom';
import { siteDomain } from 'utils/domains';
import { useDispatch } from 'react-redux';
import { sessionAvailability, getCandidateInfo } from 'store/Header/actions/index';
import { Toast } from "services/Toast";
import Loader from 'components/DesktopComponent/Common/Loader/loader';


const RouteWithSubRoutes = route => {

    const dispatch = useDispatch()
    const [loader, setLoader] = useState(true)

    const isSessionAvailable = async () => {
        localStorage.clear();
        try {
            console.log("these console logs are written intentionally and will be removed as soon as the app becomes stable");
            console.log("api session hi tinit")
            const session = await new Promise((resolve, reject) => dispatch(sessionAvailability({ resolve, reject })));
            console.log("api session hit end")
            if (session['result'] === false){
                setLoader(false);
                return;
            }
            console.log("getting candidate info")
            const candidateId = session['candidate_id'];
            await new Promise((resolve, reject) => dispatch(getCandidateInfo({ candidateId, resolve, reject })));
            setLoader(false)

        }
        catch (e) {
            console.log("error occured in fetching user session");
            // Toast('error', 'Something went wrong. Cannot login')
            // return resolve(false);
            setLoader(false)
        }
    }


    useEffect(() => {
        if (!(localStorage.getItem('isAuthenticated') === "true")) {
            const session = isSessionAvailable();
            // console.log("session is ", session)
            // return session;
        }
        else{
		setLoader(false);
}
	// console.log("this is the loader")
    }, [])



    const renderComponent = props => {

        // const isAuthenticated = getAuthentication();
        // console.log("this should come second", localStorage.getItem('isAuthenticated'))

        if (!!route.private) {
            if (localStorage.getItem('isAuthenticated') === 'true') {
                return <route.component {...props} routes={route.routes} />
            }
            else {
                window.location.replace(`${siteDomain}/login?next=${props.match.url}`);
            }
        }
        else {
            return <route.component {...props} routes={route.routes} />
        }
    }

    return (
        <>
        {!!loader && <Loader />}
        {
            !loader ?  
            <Route
            path={route.path}
            exact={route.exact}
            render={renderComponent}
        /> : null
        }
        </>
       
    )
};


export default RouteWithSubRoutes;