import React from 'react';

class CalculationsCreator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      calculations: [{
          'name': 'static_value_1',
          'type': 'static_value',
          'operator': 'operator_value_1'
      }],
      objects: []
    }
    this.handleToggleChange = this.handleToggleChange.bind(this);
    this.handleAddOperation = this.handleAddOperation.bind(this);
    this.renderValueInput = this.renderValueInput.bind(this);
  }

  fetchUrl(url) {
    return fetch(url)
      .then(response => response.json());
  }

  componentDidMount() {
    this.fetchUrl('http://127.0.0.1:5000/api/prototypes/read')
      .then(data => {
        const objects = [];
        for (var key in data) {
          if (data.hasOwnProperty(key)){
            objects.push(data[key]);
          }
        }
        this.setState({ objects });
      });
  }

  handleToggleChange(event) {
    console.log(event);
    //this.setState({ calculations.type: event.target.value });
  }

  handleAddOperation(e){
    e.preventDefault();
    let newInputName = `static_value_${this.state.calculations.length}`;
    this.setState({
      calculations: this.state.calculations.concat([{'name': newInputName}])
    });
  }

  renderValueInput() {
  /*return(
    <div>
      <label htmlFor={`static_value_${i+1}`}>Value:</label>
      <input
        type="text"
        id={`static_value_${i+1}`}
        name={`static_value_${i+1}`} />
    </div>
  )}*/
    return null;
  }

  render() {
    return (
      <form method="post" action="/prototypes/_incoming" encType="multipart/form-data" >
        <label htmlFor="name">Calculation name:</label>
        <input type="text" id="name" name="name" />
        <fieldset>
          <legend>Implemention method</legend>
          <label htmlFor="contingent">By rule (contingent on rule):</label>
          <select name="contingent">
            <option value=""></option>
            <option value="TRUE">Yes</option>
            <option value="FALSE">No</option>
          </select>
          <strong>OR</strong>
          <label htmlFor="object">Directly on prototype (always calculated):</label>
          <select name="object">
            <option value=""></option>
            {this.state.objects.map(function(object, i) {
              return(
                <option value={object.type} key={`object_${i}`}>{object.type}</option>
              )
            })}
          </select>
        </fieldset>

        {this.state.calculations.map((input, i) => {
          return(
            <div className="value" key={i}>
              <label htmlFor={`operator_value_${i+1}`}>Operator:</label>
              <select name={`operator_value_${i+1}`} id={`operator_value_${i+1}`}>
                <option key={`operator_value_${i+1}-plus`} value="+">+ (plus)</option>
                <option key={`operator_value_${i+1}-minus`} value="-">- (minus)</option>
                <option key={`operator_value_${i+1}-multiply`} value="*">* (multiply)</option>
                <option key={`operator_value_${i+1}-divide`} value="/">/ (divide)</option>
                <option key={`operator_value_${i+1}-power`} value="^">^ (to power of)</option>
              </select>
              <fieldset className="radio-toggle" id={i}>
                <label className="toggle" htmlFor={`value_type_static_${i+1}`}>
                  <input
                    name={`value_type_static_${i+1}`}
                    type="radio"
                    value="static_value"
                    checked={this.state.calculations[i].type==='static_value'}
                    onChange={this.handleToggleChange} />
                <span>Static value</span>
                </label>

                <label className="toggle" htmlFor={`value_type_object_${i+1}`}>
                  <input
                    name={`value_type_object_${i+1}`}
                    type="radio" value="object_value"
                    checked={this.state.calculations[i].type==='object_value'}
                    onChange={this.handleToggleChange} />
                  <span>Value from object</span>
                </label>
              </fieldset>

            </div>
          )
        })}
        <a className="usa-button usa-button-outline" onClick={ this.handleAddOperation }>Add another operation</a>
        <button value="submit" type="submit">Save object</button>
      </form>
    );
  }
};

export default CalculationsCreator;
