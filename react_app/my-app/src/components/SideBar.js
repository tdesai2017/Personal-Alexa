import React from "react";
import Sidebar from "react-sidebar";
import { Link } from 'react-router-dom';



class SidebarWrapper extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sidebarOpen: true,
      shoppingListHovered : false, // can also be 'basic' or 'hovered'
      remindersHovered : false,
      timersHovered : false,
      alarmsHovered: false,
      cameraHovered: false
    
    }
    this.onSetSidebarOpen = this.onSetSidebarOpen.bind(this);
    this.toggleHover = this.toggleHover.bind(this)
    this.toggleLeave = this.toggleLeave.bind(this)
    // this.routeChange = this.routeChange.bind(this)
  }

  onSetSidebarOpen(open) {
    this.setState({ sidebarOpen: open });
  }


  toggleHover(event){

    this.setState({[event.target.getAttribute('name') + 'Hovered'] : true }) 

  }

  toggleLeave(event){
    this.setState({[event.target.getAttribute('name') + 'Hovered'] : false })
      
  }

  // routeChange(event) {
  //   let path = `shopping-cart`;
  //   // this.props.history.push(path);
  // }

  

  render() {
    const linkStyle = {textDecoration : 'none'}
    var hoveredStyle = { cursor: 'pointer', fontSize: '140%', marginTop: '10px', marginBottom: '10px', marginLeft: '30px', color: '#42bcf4', fontFamily : "Brush Script MT"}
    var basicStyle = { cursor: 'pointer', marginTop: '10px', marginBottom: '10px', marginLeft: '30px', color : 'grey'} 

    const shoppingListStyle = this.state.shoppingListHovered ? hoveredStyle : basicStyle
    const remindersStyle = this.state.remindersHovered ?  hoveredStyle : basicStyle
    const timersStyle = this.state.timersHovered ? hoveredStyle : basicStyle
    const alarmsStyle = this.state.alarmsHovered ? hoveredStyle : basicStyle
    const CameraStyle = this.state.cameraHovered ? hoveredStyle : basicStyle

    return (
      <Sidebar
        sidebar={

        <div style = {{display: 'flex', flexDirection: 'column'}}>

                <nav className="navbar navbar-dark bg-dark">
                    <a className="navbar-brand" href="#" style = {{marginBottom:'10px'}}>
                        <h4 style = {{fontFamily : "Brush Script MT", fontSize: '175%', color: '#42bcf4'}}>Alexa Options</h4>
                    </a>
                </nav>


                <div style = {{display: 'flex', flexDirection: 'column', }}>

                        <div style = {{marginTop:'20px', marginBottom: '10px'}}>
                        <Link to='shopping-cart' style = {linkStyle}> <strong name = 'shoppingList' style = {shoppingListStyle} onMouseEnter={this.toggleHover} onMouseLeave={this.toggleLeave}>Shopping List &#10095;</strong> </Link>
                        </div>

                        <hr style = {{width:'100%'}}/>

                        <Link to = 'reminders' style = {linkStyle}><strong name = 'reminders' style = {remindersStyle} onMouseEnter={this.toggleHover} onMouseLeave={this.toggleLeave} >Reminders &#10095;</strong></Link>

                        <hr style = {{width:'100%'}}/>

                        <strong name = 'timers'style = {timersStyle} onMouseEnter={this.toggleHover} onMouseLeave={this.toggleLeave} >Timers &#10095;</strong>

                        <hr style = {{width:'100%'}}/>

                        <strong name = 'alarms' style = {alarmsStyle} onMouseEnter={this.toggleHover} onMouseLeave={this.toggleLeave} >Alarms &#10095;</strong>

                        <hr style = {{width:'100%'}}/>


                        <strong name = 'camera' style = {CameraStyle} onMouseEnter={this.toggleHover} onMouseLeave={this.toggleLeave} >Camera &#10095;</strong>

                        <hr style = {{width:'100%'}}/>





                </div>


            </div>
  
    
    }
        open={this.state.sidebarOpen}
        onSetOpen={this.onSetSidebarOpen}
        styles={{ sidebar: { background: "white" } }}
      >
        <button className = 'btn btn-link ' onClick={() => this.onSetSidebarOpen(true)}>
        <img style = {{width: '75px', width: '75px'}}src = 'https://png.pngtree.com/svg/20170919/_raspberry_pi_1342096.png'  />  
        </button>

      </Sidebar>
    );
  }
}

export default SidebarWrapper;