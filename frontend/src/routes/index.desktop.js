import React from "react";
import { Route, Switch } from "react-router-dom";
import SkillPageContainer from "components/DesktopComponent/Core/SkillPage/skillPage";
import CataloguePageContainer from "components/DesktopComponent/Core/CataloguePage/cataloguePage";
import { getSkillPageActions } from 'apiHandler/skillPageApi';
import Error404Container from 'components/DesktopComponent/Common/ErrorPage404/errorPage404';
import { getCataloguePageActions } from "apiHandler/cataloguePageApi";
import DashboardContainer from 'components/DesktopComponent/Core/DashboardPage/dashboardPage';
import DashboardWalletContainer from 'components/DesktopComponent/Core/DashboardPage/MyWallet/myWallet';
import { getDashboardPageActions } from 'apiHandler/dashboardPageApi';

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

const DesktopAppRouter = () => (
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
        path: '/dashboard/',
        component: DashboardContainer,
        actionGroup: getDashboardPageActions,
    },
    {
        path: '/dashboard/mywallet',
        component: DashboardWalletContainer,
        actionGroup: getDashboardPageActions,
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