import React from "react";
import { Switch, Route } from "react-router-dom";
import HomePageContainer from 'components/MobileComponent/Homepage/homepage';
import { getHomepageActionsMobile } from "apiHandler/homepageApi";


const MobileAppRouter = () => (

    <div>
        <Switch>
            {routes.map((route, i) => <Route key = {i} path={route.path} exact={route.exact} render={route.component} />
            )}
        </Switch>
    </div>

);

export const routes = [
    {
        path: '/',
        component: HomePageContainer,
        actionGroup: getHomepageActionsMobile,
        exact: true
    }
]

export default MobileAppRouter;