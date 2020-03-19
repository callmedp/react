import {BrowserRouter as Router, Route} from "react-router-dom";
import HomeContainer from '../components/Core/Home/home.jsx';
import React from "react";

export const RouteWithSubRoutes = route => {
    
    return(
    <Route
        path={route.path}
        exact={route.exact}
        render={props => 
            // pass the sub-routes down to keep nesting
            <route.component {...props} routes={route.routes}/>
        }
    />
)};




const AppRouter = () => (
    <Router>
        <div>
            {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
        </div>
    </Router>
);


export const routes = [
    {
        path: '/',
        component: HomeContainer,
    },

]

export default AppRouter;