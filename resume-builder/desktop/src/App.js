import React, {Component} from 'react';
import AppRouter from './routes/index';
import  { Redirect } from 'react-router-dom'

class App extends Component {
    render() {
        return (

            // < AppRouter />
            // null
            <Redirect to='https://learning2.shine.com/resume-builder'  />
    )
        ;
    }
}

export default App;
