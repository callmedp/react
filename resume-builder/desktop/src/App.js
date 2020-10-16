import React, {Component} from 'react';
import AppRouter from './routes/index';
import { resumeShineSiteDomain } from './Utils/domains';
class App extends Component {
    render() {
        return (

            // < AppRouter />
            // null
            window.location.replace(`${resumeShineSiteDomain}/resume-builder`)
    )
        ;
    }
}

export default App;
