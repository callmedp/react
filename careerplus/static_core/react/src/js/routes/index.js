import React from "react";
import {BrowserRouter as Router, Route, Link, Switch} from "react-router-dom";
import RegisterContainer from '../components/UserInfo/Register/register.jsx';
import DetailContainer from '../components/UserInfo/Detail/detail.jsx';
import ExperienceContainer from '../components/UserInfo/Experience/experience.jsx';
import EducationContainer from '../components/UserInfo/Education/education.jsx';
import ProjectContainer from '../components/UserInfo/Project/project.jsx';
import CertificationContainer from '../components/UserInfo/Certification/certification.jsx';
import AchievementContainer from '../components/UserInfo/Achievement/achievement.jsx';
import ReferenceContainer from '../components/UserInfo/Reference/reference.jsx';
import Main from '../components/Main/main.jsx';

const AppRouter = () => (
    <Router>
        <Switch>
            <Route path='/resume-builder' exact component={Main}/>
            <Route path="/resume-builder/register" component={RegisterContainer}/>
            <Route path="/resume-builder/detail" component={DetailContainer}/>
            <Route path="/resume-builder/experience" component={ExperienceContainer}/>
            <Route path="/resume-builder/education" component={EducationContainer}/>
            <Route path="/resume-builder/project" component={ProjectContainer}/>
            <Route path="/resume-builder/certification" component={CertificationContainer}/>
            <Route path="/resume-builder/achievement" component={AchievementContainer}/>
            <Route path="/resume-builder/reference" component={ReferenceContainer}/>
        </Switch>

    </Router>
);

export default AppRouter;