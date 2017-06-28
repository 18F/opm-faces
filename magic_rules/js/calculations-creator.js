import React from 'react';

class Operation extends React.Component {
  constructor() {
    super()
  }
  render() {
    var i = this.props.count;
    return (
      <div>
        <label htmlFor={`operator_value_${i}`}>Operator:</label>
        <select name={`operator_value_${i}`} id={`operator_value_${i}`}>
          <option key={`operator_value_${i}-plus`} value="+">+ (plus)</option>
          <option key={`operator_value_${i}-minus`} value="-">- (minus)</option>
          <option key={`operator_value_${i}-multiply`} value="*">* (multiply)</option>
          <option key={`operator_value_${i}-divide`} value="/">/ (divide)</option>
          <option key={`operator_value_${i}-power`} value="^">^ (to power of)</option>
        </select>
      </div>
    )
  }
}

class FormulaValue extends React.Component {
  constructor() {
    super()
    this.state = {
      type: 'static_value'
    }
    this.handleToggleChange = this.handleToggleChange.bind(this);
  }

  handleToggleChange(event) {
    this.setState({ type: event.target.value });
  }

  renderStaticInput() {
    var i = this.props.count;
    return(
      <div>
        <label htmlFor={`static_value_${i}`}>Value:</label>
        <input
          type="text"
          id={`static_value_${i}`}
          name={`static_value_${i}`} />
      </div>
    )
  }

  renderAttrInput() {
    let objectKeys = [];
    for (var key in this.props.selectedObj) {
      if (this.props.selectedObj.hasOwnProperty(key) && key != 'type' && key != 'rules'){
        objectKeys.push(<option key={key} value={key}>{key}</option>);
      }
    }
    console.log(this.props.selectedObj);
    return (
      <div>
        <label>Value:</label>
        <select>
        { objectKeys }
        </select>
      </div>
    )
  }

  render() {
    var i = this.props.count;
    console.log(this.props.objects);
    return(
      <div>
        <fieldset className="usa-fieldset" id={i}>
          <ul className="usa-unstyled-list">
            <li>
              <input
                name={`value_type_static_${i}`}
                type="radio"
                value="static_value"
                checked={this.state.type==='static_value'}
                onChange={this.handleToggleChange} />
              <label className="toggle" htmlFor={`value_type_static_${i}`}>Static value</label>
            </li>
            <li>
              <input
                name={`value_type_object_${i}`}
                type="radio" value="object_value"
                checked={this.state.type==='object_value'}
                onChange={this.handleToggleChange} />
              <label className="toggle" htmlFor={`value_type_object_${i}`}>Value from object</label>
            </li>
          </ul>
        </fieldset>

        { this.state.type === 'static_value' ? this.renderStaticInput() : this.renderAttrInput() }

      </div>
    )
  }
}

class CalculationsCreator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputs: 1, //0-based
      operations: 0, //0-based
      objects: [],
      selectedObj: {}
    }
    this.handleAddOperation = this.handleAddOperation.bind(this);
    this.handleObjSelect = this.handleObjSelect.bind(this);
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

  handleAddOperation(e){
    e.preventDefault();
    this.setState({
      inputs: this.state.inputs + 1,
      operations: this.state.operations + 1
    });
  }

  handleObjSelect(event) {
    let obj = this.state.objects.filter((object) => {
                return object.type == event.target.value;
              });
    this.setState({ selectedObj: obj[0] });
  }

  render() {
    var formulas = [];
    for (var i=0; i < this.state.inputs; i++) {
      if (i==0) {
        formulas.push(<FormulaValue count={i} selectedObj={this.state.selectedObj} />);
        formulas.push(<Operation count={i} />);
        formulas.push(<FormulaValue count={i+1} selectedObj={this.state.selectedObj} />);
      } else {
        formulas.push(<Operation count={i} />);
        formulas.push(<FormulaValue count={i+1} selectedObj={this.state.selectedObj} />);
      }
    }
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
          <select name="object"
                  onChange={ this.handleObjSelect }>
            <option value=""></option>
            {this.state.objects.map((object, i) => {
              return(
                <option
                  value={ object.type }
                  selected={ this.state.selectedObj.type === object.type }
                  key={`object_${i}`}>{object.type}</option>
              )
            })}
          </select>
        </fieldset>
        { formulas }

        <a className="usa-button usa-button-outline" onClick={ this.handleAddOperation }>Add another operation</a>
        <button value="submit" type="submit">Save object</button>
      </form>
    );
  }
};

export default CalculationsCreator;
