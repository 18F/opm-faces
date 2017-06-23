import React from 'react';

class ObjectCreator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputs: [{ 'id': 'attribute_1' }]
    }
    this.addAttribute = this.addAttribute.bind(this);
  }

  addAttribute() {
    let count = this.state.attrNum + 1;
    this.setState({
      attrNum: count
    });
    return(
      <div>
      <label htmlFor="attribute_">Attribute:</label>
      <input type="text" id={`attribute-${this.state.attrNum}`} name={`attribute-${this.state.attrNum}`} />
      </div>
    );
  }

  render() {
    return (
      <form method="post" action="/prototypes/_incoming" encType="multipart/form-data" >
        <label htmlFor="name">Name:</label>
        <input type="text" id="name" name="name" />
        <div className="attributes">
          <label htmlFor={`attribute-${this.state.attrNum}`}>Attribute:</label>
          <input type="text" id={`attribute-${this.state.attrNum}`} name={`attribute-${this.state.attrNum}`} />
        </div>
        <a className="usa-button usa-button-outline" onClick={ this.addAttribute }>Add another attribute</a>
        <button value="submit" type="submit">Save object</button>
      </form>
    );
  }
};

export default ObjectCreator;
