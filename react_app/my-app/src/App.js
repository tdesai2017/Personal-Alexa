import React from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Switch } from 'react-router-dom'
// import Home from './components/Home'
// import About from './components/About'
import NoMatch from './components/NoMatch'
// import Contact from './components/Contact'
import Layout from './style_components/Layout'
import SideBarStyle from './style_components/SideBarStyle'
import SideBar from './components/SideBar'
import ShoppingCart from './components/ShoppingCart'
import Reminders from './components/Reminders'



function App() {
  return (
    <React.Fragment>
      
      <Layout>
        <SideBar/>
        
      <Router>
        <Switch>

          <Route exact path="/shopping-cart" component = {ShoppingCart}/>
          <Route exact path="/reminders" component = {Reminders}/>

          {/* <Route exact path="/about" component = {About}/> */}
          {/* <Route exact path="/contact" component = {Contact}/> */}
          <Route component={NoMatch}/>


        </Switch>
      </Router>
      </Layout>
      
    </React.Fragment>
    
  )
}

export default App;
