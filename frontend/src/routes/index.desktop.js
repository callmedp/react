import React from "react";
import { Route, Switch } from "react-router-dom";
import SkillPageContainer from "components/DesktopComponent/Core/SkillPage/skillPage";
import CataloguePageContainer from "components/DesktopComponent/Core/CataloguePage/cataloguePage";
import { getSkillPageActions } from 'apiHandler/skillPageApi';
import Error404Container from 'components/DesktopComponent/Common/ErrorPage404/errorPage404';
import { getCataloguePageActions } from "apiHandler/cataloguePageApi";
import DashboardPageContainer from 'components/DesktopComponent/Core/DashboardPage/dashboardPage';
import { getDashboardPageActions } from "apiHandler/dashboardPageApi";
import HomePageContainer from 'components/DesktopComponent/Core/HomePage/homePage';
import RouteWithSubRoutes from './route';
import { getHomepageActions } from "apiHandler/homepageApi";
import UserIntentPageContainer from 'components/DesktopComponent/Core/UserIntentPage/userIntentPage';

const DesktopAppRouter = () => (
    <div>
        <Switch>
        {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
        </Switch>
    </div>
);

export const routes = [
    {
        path: '/homepage/',
        component: HomePageContainer,
        actionGroup: getHomepageActions,
        exact: true
    },
    {
        path: '/courses/:func/:skill/:id/',
        component: SkillPageContainer,
        actionGroup: getSkillPageActions,
        exact: true
    },
    {
        path: '/online-courses.html/',
        component: CataloguePageContainer,
        actionGroup: getCataloguePageActions,
        exact: true,
    },
    {
        path: '/dashboard/:name?',
        component: DashboardPageContainer,
        private: true
    },
    {
        path: '/user-intent',
        component: UserIntentPageContainer,
        exact: true
    },
    {
        path: '/404/',
        component: Error404Container
    },
    {
        //keep this at the bottom
        path: '*',
        component: Error404Container
    }
]

export default DesktopAppRouter;