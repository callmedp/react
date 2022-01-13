import React from 'react';
import DesktopAppRouter from './routes/index.desktop';
import './App.desktop.css';

function DesktopApp(props) {

  console.log("reached desktop app")
  return (
    <DesktopAppRouter />
  );
}

export default DesktopApp;
