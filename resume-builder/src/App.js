import React, {Component} from 'react';
import './App.scss';
import AppRouter from './routes/index';

class App extends Component {
    render() {
        return (
            <AppRouter/>
        );
    }
}

export default App;
