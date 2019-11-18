import React from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Switch } from 'react-router-dom'
// import Home from './components/Home'
// import About from './components/About'
import NoMatch from './components/NoMatch'
// import Contact from './components/Contact'
import SideBar from './components/SideBar'
import ShoppingCart from './components/ShoppingCart'
import Reminders from './components/Reminders'
import { Container } from 'react-bootstrap'



function App() {
  return (
  
    <React.Fragment>

    <Container>
  
      <Router>
      <Container>

      <SideBar/>

        <Switch>

          <Route exact path="/shopping-cart" component = {ShoppingCart}/>
          <Route exact path="/reminders" component = {Reminders}/>

          {/* <Route exact path="/about" component = {About}/> */}
          {/* <Route exact path="/contact" component = {Contact}/> */}
          <Route component={NoMatch}/>


        </Switch>
        </Container>

      </Router>
      </Container>
      
    </React.Fragment>
    
  )
}

export default App;
