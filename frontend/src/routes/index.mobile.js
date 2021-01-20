import React from "react";
import { Route, Switch } from "react-router-dom";
import SkillPageContainer from "components/MobileComponent/Core/SkillPage/skillPage";
import CataloguePageContainer from "components/MobileComponent/Core/CataloguePage/cataloguePage";
import DashboardContainer from "components/MobileComponent/Core/DashboardPage/dashboardPage";
import { getSkillPageActionsMobile } from 'apiHandler/skillPageApi'; 
import Error404Container from 'components/MobileComponent/Common/ErrorPage404/errorPage404';
import { getCataloguePageActionsMobile } from "apiHandler/cataloguePageApi";
import DashboardPageContainer from 'components/MobileComponent/Core/DashboardPage/dashboardPage';
import RouteWithSubRoutes from 'routes/route';



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
        path: '/dashboard/:name/',
        component: DashboardPageContainer,
        private: false,
        exact: true,
    },
    {
        path: '/404/',
        component: Error404Container
    },
    {
        path : '*',
        component: Error404Container
    }
]

export default MobileAppRouter;