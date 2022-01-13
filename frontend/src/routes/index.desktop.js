import React from "react";
import { Route, Switch } from "react-router-dom";
import HomePageContainer from 'components/DesktopComponent/Homepage/homepage';
import { getHomepageActions } from "apiHandler/homepageApi";

const DesktopAppRouter = () => {
    console.log("desktop app router")
    return (
    <div>
        <Switch>
            {routes.map((route, i) => <Route key = {i} path={route.path} exact={route.exact} render={(props) => <route.component {...props} routes={route.routes} />} />
            )}
        </Switch>
    </div>
)};

export const routes = [
    {
        path: '/',
        component: HomePageContainer,
        actionGroup: getHomepageActions,
        exact: true
    }
]

export default DesktopAppRouter;