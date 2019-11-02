import React from 'react'
import cloneDeep from 'lodash/cloneDeep'


class Reminders extends React.Component{
    constructor(){
        super()
        this.state = {
            allReminders : '',
            addValue : ''}

        this.deleteReminder = this.deleteReminder.bind(this)
        this.handleClear = this.handleClear.bind(this)
        this.submitAdd = this.submitAdd.bind(this)
        this.handleAddChange = this.handleAddChange.bind(this)

        
        }


        // Capture data and set it to state
componentDidMount(){
    fetch('http://127.0.0.1:8000/myapp/get_reminders')
    .then(response => response.json())
    .then (data => {
        console.log(data)
        const filteredData = data.map( item => item.fields.text)
        console.log(filteredData)
        this.setState({allReminders: filteredData})})
}


handleAddChange(event){
    this.setState({[event.target.name]: event.target.value})
}


submitAdd(event) {
    event.preventDefault()
    console.log(this.state.allReminders.concat(this.state.addValue))
    if (this.state.addValue != ''){

        fetch('http://127.0.0.1:8000/myapp/receive_reminders_add/', 
    {
        method: 'POST',
        body: JSON.stringify({'add': this.state.addValue}),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            // Other possible headers
        }
    })
    .then(response => response.json())
    .then(data => {

    if (data === 'Reminder Added'){
        this.setState(prevState => { return{
            // I am automatically making it uppercase as well
            allReminders: prevState.allReminders.concat(prevState.addValue.charAt(0).toUpperCase() + prevState.addValue.substring(1))
        }
         })
    }
    else{
        console.log(data)
    }
    
    })
    }   
}
    

handleClear(event){
    event.preventDefault()
    fetch('http://127.0.0.1:8000/myapp/receive_reminders_clear/', 
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            // Other possible headers
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data === 'Reminders Cleared'){
            this.setState({allReminders :[] })
    }
        else{
            console.log(data)
        }
    
    })
}  



deleteReminder(event){
    var value = event.target.value
    fetch('http://127.0.0.1:8000/myapp/receive_reminders_delete/', 
    {
        method: 'POST',
        body: JSON.stringify({'delete': event.target.value}),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            // Other possible headers
        }
    })
    .then(response => response.json())
    .then(data => {

        if (data === 'Reminder Deleted'){
            var filteredAry = this.state.allReminders.filter(e => e !== value)
            this.setState({allReminders: filteredAry})
    }
        else{
            console.log(data)
        }
    
    })
}  

render(){
    
    var reminders = []
    // Adds all the reminders from state into the above list
    if (this.state.allReminders != ''){
        for (var i = 0; i < this.state.allReminders.length; i++) {
            reminders.push(this.state.allReminders[i])
        }

    }

    const reminderStyle = {marginTop: '30px'}

        return(

        <div>


        <div className="container-fluid" style = {{padding:'50px'}}>


                <div className = 'container'>
                    <h2 className="text-center" id="title" style = {{color: '#42bcf4'}}>
                        <p style = {{fontFamily : "Brush Script MT", fontSize: '150%'}}>Reminders</p>
                    </h2>
                        <hr style = {{padding: '30px'}}/>                     

                <div className="row">
                    <div className="col-sm-6">

                     <strong style = {{marginLeft: '10%'}}>Remember to:</strong>
                     
                    <div style = {{display: 'flex', flexDirection: 'column', marginLeft: '20%' }}>

                    {reminders.map((value) => {
                            return (
                            <div style = {reminderStyle} key = {value}> 
                            <button  onClick = {this.deleteReminder} style = {{border : 'none'}} name = {'delete' + value} value = {value}>✖</button>
                            &nbsp;
                            <em> {value}</em>
                            </div>)
                        })}




                    </div>
      

                    </div>

                    <div className="col-sm-6">
                        Add:
                        <form onSubmit = {this.submitAdd}>
                            {/* {% csrf_token %} */}
                            <input className = 'form-control' value = {this.state.addValue}  type = 'text' name = 'addValue' onChange = {this.handleAddChange}/>
                            <br/>
                            <button className = 'btn btn-success' type = 'submit'> Submit </button>
                        </form>

                        <br/>
                        <br/>
                        Clear all:

                        <form onSubmit = {this.handleClear}>
                                
                                <button className = 'btn btn-danger' type = 'submit'> Submit </button>
                            </form>


                    </div>
                    </div>
                    </div>
                    </div>
                </div>


            
            )
        }
}


export default Reminders