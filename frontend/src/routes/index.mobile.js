import React from "react";
import { Route, Switch } from "react-router-dom";
import SkillPageContainer from "components/MobileComponent/Core/SkillPage/skillPage";
import CataloguePageContainer from "components/MobileComponent/Core/CataloguePage/cataloguePage";
import MyServices from "components/MobileComponent/Core/DashboardPage/MyServices/myServices";
import DashboardContainer from "components/MobileComponent/Core/DashboardPage/dashboardPage";
import { getSkillPageActionsMobile } from 'apiHandler/skillPageApi'; 
import Error404Container from 'components/MobileComponent/Common/ErrorPage404/errorPage404';
import { getCataloguePageActionsMobile } from "apiHandler/cataloguePageApi";
import DashboardPageContainer from 'components/MobileComponent/Core/DashboardPage/dashboardPage';
import RouteWithSubRoutes from 'routes/route';
import HomePageContainer from 'components/MobileComponent/Core/HomePage/homePage';
import { getHomepageActionsMobile } from "apiHandler/homepageApi";
import DetailPageContainer from 'components/MobileComponent/Core/DetailPage/detailPage';
import { getDetailPageActions } from "apiHandler/detailsPageApi";
import CourseDetailPage1 from "components/MobileComponent/Core/DetailPage/detailPage1";

const MobileAppRouter = () => (

    <div>
        <Switch>
        {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
        </Switch>
    </div>

);

export const routes = [
    {
        path: '/',
        component: HomePageContainer,
        actionGroup: getHomepageActionsMobile,
        exact: true
    },
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
        path: '/course/:func/:skill/:id/',
        component: DetailPageContainer,
        actionGroup: getDetailPageActions,
        exact: true,
    },

    {
        path : '/coursedetailPage1',
        component : CourseDetailPage1
    },
    {
        path: '/dashboard/:name?',
        component: DashboardPageContainer,
        private: true
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