import React from 'react'


class ShoppingCart extends React.Component{
    constructor(){
        super()
        this.state = {
            allShoppingListItems : '',
            addValue : ''}

        this.deleteShoppingItem = this.deleteShoppingItem.bind(this)
        this.handleClear = this.handleClear.bind(this)
        this.submitAdd = this.submitAdd.bind(this)
        this.handleAddChange = this.handleAddChange.bind(this)

        
        }


componentDidMount(){
    fetch('http://127.0.0.1:8000/myapp/get_shopping_list_items')
    .then(response => response.json())
    .then (data => {
        const filteredData = data.map( item => item.fields.name)
        console.log(filteredData)
        this.setState({allShoppingListItems: filteredData})})
}


handleAddChange(event){
    this.setState({[event.target.name]: event.target.value})
}


submitAdd(event) {
    event.preventDefault()
    console.log(this.state.allShoppingListItems.concat(this.state.addValue))
    if (this.state.addValue != ''){

        fetch('http://127.0.0.1:8000/myapp/receive_shopping_list_add/', 
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

    if (data === 'Item Added'){
        this.setState(prevState => { return{
            // I am automatically making it uppercase as well
            allShoppingListItems: prevState.allShoppingListItems.concat(prevState.addValue.charAt(0).toUpperCase() + prevState.addValue.substring(1)),
            addValue: ''

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
    fetch('http://127.0.0.1:8000/myapp/receive_shopping_list_clear/', 
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
        if (data === 'List Cleared'){
            this.setState({allShoppingListItems :[] })
    }
        else{
            console.log(data)
        }
    
    })
}  



deleteShoppingItem(event){
    var value = event.target.value
    fetch('http://127.0.0.1:8000/myapp/receive_shopping_list_delete/', 
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

        if (data === 'Item Deleted'){
            var filteredAry = this.state.allShoppingListItems.filter(e => e !== value)
            this.setState({allShoppingListItems: filteredAry})
    }
        else{
            console.log(data)
        }
    
    })
}  

render(){
    
    var shoppingItems = []
    // Adds all the shopping items from state into the above list
    if (this.state.allShoppingListItems != ''){
        for (var i = 0; i < this.state.allShoppingListItems.length; i++) {
            shoppingItems.push(this.state.allShoppingListItems[i])
        }

    }

    const shoppingItemStyle = {marginTop: '30px'}

        return(

        <div>


        <div className="container-fluid" style = {{padding:'50px'}}>


                <div className = 'container'>
                    <h2 className="text-center" id="title" style = {{color: '#42bcf4'}}>
                        <p style = {{fontFamily : "Brush Script MT", fontSize: '150%'}}>Shopping List</p>
                    </h2>
                        <hr style = {{padding: '30px'}}/>                     

                <div className="row">
                    <div className="col-sm-6">

                     <strong style = {{marginLeft: '10%'}}>To Buy:</strong>
                     
                    <div style = {{display: 'flex', flexDirection: 'column', marginLeft: '20%' }}>

                    {shoppingItems.map((value) => {
                            return (
                            <div style = {shoppingItemStyle} key = {value}> 
                            <button  onClick = {this.deleteShoppingItem} style = {{border : 'none'}} name = {'delete' + value} value = {value}>✖</button>
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


export default ShoppingCart