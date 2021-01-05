import React from "react";
import { Route, Switch } from "react-router-dom";
import SkillPageContainer from "components/MobileComponent/Core/SkillPage/skillPage";
import CataloguePageContainer from "components/MobileComponent/Core/CataloguePage/cataloguePage";
import { getSkillPageActionsMobile } from 'apiHandler/skillPageApi'; 
import Error404Container from 'components/MobileComponent/Common/ErrorPage404/errorPage404';
import { getCataloguePageActionsMobile } from "apiHandler/cataloguePageApi";

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
        <Switch>
        {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
        </Switch>
    </div>

);

export const routes = [
    {
        path: '/courses/:func/:skill/:id/',
        component: SkillPageContainer,
        actionGroup: getSkillPageActionsMobile,
        exact: true
    },
    {
        path: '/online-courses.html/',
        component: CataloguePageContainer,
        actionGroup: getCataloguePageActionsMobile,
        exact: true,
    },
    {
        path : '*',
        component: Error404Container
    }
]

export default MobileAppRouter;