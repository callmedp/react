import React from "react";
import { Route } from "react-router-dom";
import SkillPageContainer from "components/MobileComponent/Core/SkillPage/skillPage";


export const RouteWithSubRoutes = route => {
    return (
        <Route
            path={route.path}
            exact={route.exact}
            render={props =>
                <route.component {...props} routes={route.routes} />
            }
        />
    )
};


const MobileAppRouter = () => (

    <div>
        {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
    </div>

);

export const routes = [
    {
        path: '/courses/:func/:skill/:id',
        component: SkillPageContainer
    }
]

export default MobileAppRouter;