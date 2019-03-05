import React from "react";
import {BrowserRouter as Router, Route} from "react-router-dom";
import RegisterContainer from '../components/UserInfo/Register/register.jsx';
import DetailContainer from '../components/UserInfo/Detail/detail.jsx';
import SkillContainer from '../components/UserInfo/Skill/skill.jsx';
import ExperienceContainer from '../components/UserInfo/Experience/experience.jsx';
import EducationContainer from '../components/UserInfo/Education/education.jsx';
import ProjectContainer from '../components/UserInfo/Project/project.jsx';
import CertificationContainer from '../components/UserInfo/Certification/certification.jsx';
import AchievementContainer from '../components/UserInfo/Achievement/achievement.jsx';
import ReferenceContainer from '../components/UserInfo/Reference/reference.jsx';
import Main from '../components/Main/main.jsx';
import PricingContainer from '../components/Payment/pricing.jsx'

export const RouteWithSubRoutes = route => (
    <Route
        path={route.path}
        render={props => (
            // pass the sub-routes down to keep nesting
            <route.component {...props} routes={route.routes}/>
        )}
    />
);


const AppRouter = () => (
    <Router>
        <div>
            {routes.map((route, i) => <RouteWithSubRoutes key={i} {...route} />)}
        </div>
    </Router>
);

const routes = [
    {
        path: '/resume-builder',
        component: Main,
        routes: [
            {
                path: '/resume-builder/register',
                component: RegisterContainer
            },
            {
                path: '/resume-builder/detail',
                component: DetailContainer
            },
            {

                path: '/resume-builder/skill',
                component: SkillContainer
            },
            {
                path: '/resume-builder/education',
                component: EducationContainer
            },
            {
                path: '/resume-builder/experience',
                component: ExperienceContainer
            },
            {
                path: '/resume-builder/project',
                component: ProjectContainer
            },
            {
                path: '/resume-builder/certification',
                component: CertificationContainer
            },
            {
                path: '/resume-builder/achievement',
                component: AchievementContainer
            },
            {
                path: '/resume-builder/reference',
                component: ReferenceContainer
            },
            {
                path: '/resume-builder/pricing',
                component: PricingContainer
            }
        ]
    }

]

export default AppRouter;