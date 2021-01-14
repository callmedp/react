import React from 'react';
import IsAuthenticated  from 'services/authenticate';
import { Route } from 'react-router-dom';
import { siteDomain } from 'utils/domains';


const RouteWithSubRoutes = route => {

    const renderComponent =  props => {
        if( route.private ){
            // if(IsAuthenticated()){
            //     return <route.component {...props} routes={route.routes} />
            // }
            // else{
            //     window.location.replace(`${siteDomain}/login`);
            // }
        } 
        else{
            return <route.component {...props} routes={route.routes} />            
        }
    }

    return (
        <Route
            path={route.path}
            exact={route.exact}
            strict={true}
            render={renderComponent}
        />
    )
};


export default RouteWithSubRoutes;