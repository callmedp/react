import React from 'react';
import useAuthenticate  from 'services/authenticate';
import { Route } from 'react-router-dom';
import { siteDomain } from 'utils/domains';


const RouteWithSubRoutes = route => {

    const isAuthenticated = useAuthenticate();

    const renderComponent =  props => {
        if( route.private ){
            if(isAuthenticated){
                return <route.component {...props} routes={route.routes} />
            }
            else{
                window.location.replace(`${siteDomain}/login`);
            }
        } 
        else{
            return <route.component {...props} routes={route.routes} />            
        }
    }

    return (
        <Route
            path={route.path}
            exact={route.exact}
            render={renderComponent}
        />
    )
};


export default RouteWithSubRoutes;