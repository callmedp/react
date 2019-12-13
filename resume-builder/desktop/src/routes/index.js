import React from "react";
import {BrowserRouter as Router, Route} from "react-router-dom";
import EditPreviewContainer from '../components/Core/Editor/editPreview.jsx';
import HomeContainer from '../components/Core/Home/home.jsx';
import BuyContainer from '../components/Core/Payment/Buy/buy.jsx';
import DownloadContainer from '../components/Core/Payment/DownloadResume/downloadResume.jsx';
import Middleware from '../middlewares/middleware'

let middleware =new Middleware();
export const RouteWithSubRoutes = route => {
    
    return(
    <Route
        path={route.path}
        exact={route.exact}
        render={props => 
            // pass the sub-routes down to keep nesting
            middleware.routeToDisplay(route.middlewares,<route.component {...props} routes={route.routes}/>,route.path)
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
        path: '/resume-builder',
        component: HomeContainer,
        exact: true,
        middlewares :['alreadyLoggedIn']
    },
    {
        path: '/resume-builder/edit/',
        component: EditPreviewContainer,
        middlewares:['privateRoute']
    },
    {
        path: '/resume-builder/preview',
        component: EditPreviewContainer,
        middlewares:['privateRoute']
    },
    {
        path: '/resume-builder/buy',
        component: BuyContainer,
        middlewares:['privateRoute']
    },
    {
        path: '/resume-builder/download',
        component: DownloadContainer,
        middlewares:['privateRoute']
    }


]

export default AppRouter;