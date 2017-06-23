import React from 'react';

class ObjectCreator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputs: [{ 'name': 'attribute_1' }]
    }
    this.handleAddAttribute = this.handleAddAttribute.bind(this);
  }

  handleAddAttribute(e) {
    e.preventDefault();
    let newInputName = `attribute_${this.state.inputs.length}`;
    this.setState({
      inputs: this.state.inputs.concat([{'name': newInputName}])
    });
  }

  render() {
    console.log(this.state);
    return (
      <form method="post" action="/prototypes/_incoming" encType="multipart/form-data" >
        <label htmlFor="name">Name:</label>
        <input type="text" id="name" name="name" />
        {this.state.inputs.map(function(input, i) {
          return(
          <div className="attribute" key={i}>
            <label htmlFor={`attribute_${i+1}`}>Attribute:</label>
            <input
              type="text"
              id={`attribute_${i+1}`}
              name={`attribute_${i+1}`} />
          </div>
          )
        })}
        <a className="usa-button usa-button-outline" onClick={ this.handleAddAttribute }>Add another attribute</a>
        <button value="submit" type="submit">Save object</button>
      </form>
    );
  }
};

export default ObjectCreator;
