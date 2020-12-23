import React from "react";
import { Route } from "react-router-dom";
import SkillPageContainer from "components/MobileComponent/Core/SkillPage/skillPage";
import { getSkillPageActionsMobile } from 'apiHandler/skillPageApi'; 
import Error404Container from 'components/MobileComponent/Common/ErrorPage404/errorPage404';

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
        component: SkillPageContainer,
        actionGroup: getSkillPageActionsMobile,
    },
    {
        path : '*',
        component: Error404Container
    }
]

export default MobileAppRouter;