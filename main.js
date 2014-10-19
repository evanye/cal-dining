/** @jsx React.DOM */
var LOCATIONS = ['crossroads', 'cafe3', 'foothill', 'clarkkerr'];
var MEALS = ['breakfast', 'lunch', 'dinner'];

var LOCATION_TO_NAME = {
  'crossroads': 'Crossroads', 'cafe3': 'Cafe 3',
  'foothill': 'Foothill', 'clarkkerr': 'Clark Kerr'
}

var mealFromTime = function() {
  var currentTime = new Date();
  var breakfastTime = new Date(); breakfastTime.setHours(10, 1);
  var lunchTime = new Date(); lunchTime.setHours(14, 1);
  var dinnerTime = new Date(); dinnerTime.setHours(21, 1);

  if(breakfastTime < currentTime && currentTime < lunchTime)
    return 'lunch';
  else if(currentTime < dinnerTime)
    return 'dinner';
  else
    return 'breakfast';
}

var App = React.createClass({
  getDefaultProps: function() {
    return {
      api: 'http://www.ocf.berkeley.edu/~eye/cal-dining/menu'
    }
  },
  getInitialState: function() {
    return {
      active: {
        'crossroads': false, 'cafe3': false,
        'foothill': false, 'clarkkerr': false
      },
      open: {
        'crossroads': false, 'cafe3': false,
        'foothill': false, 'clarkkerr': false
      },
      meal: mealFromTime(),
      menu: {
        'crossroads': {}, 'cafe3': {},
        'foothill': {}, 'clarkkerr': {}
      }
    }
  },
  countActive: function() {
    var count = 0;
    for(var key in this.state.active){
      if(this.state.active[key])
        count++;
    }
    return count;
  },
  setActiveItem: function(item) {
    if ($.inArray(item, MEALS) !== -1) { // setting the meal
      this.state.meal = item;
      this.componentDidMount();
    } else if(item in this.state.active) { // setting the active menu
      if(this.state.active[item] === false || this.countActive() > 1) {
        var newActive = this.state.active;
        newActive[item] = !newActive[item];
        this.setState({active: newActive});
      }
    }
  },
  componentDidMount: function() {
    $.get(this.props.api + "?meal=" + this.state.meal, function(result) {
      var startSelectedCounter = 0;
      var active = this.state.active;
      var open = this.state.open;
      LOCATIONS.forEach(function(location) {
        if (Object.keys(result[location]).length) {
          open[location] = true;
          if (startSelectedCounter < 2) {
            active[location] = true;
            startSelectedCounter++;
          }
        }
      });
      this.setState({
        active: active,
        open: open,
        menu: result
      });
    }.bind(this));
  },

  render: function() {
    var menus = [];
    var colSize = 'col-xs-' + (12 / this.countActive());
    LOCATIONS.forEach(function(location) {
      if(this.state.active[location])
        menus.push(
          <div key={location} className={colSize}>
            <Menu key={location} entries={this.state.menu[location]} />
          </div>
        );
    }.bind(this));
    return (
      <div>
        <Navbar active={this.state.active} onSelect={this.setActiveItem}
                open={this.state.open} meal={this.state.meal}/>
        <div className="container">
          <div className="row">
            {menus}
          </div>
        </div>
      </div>
    );
  }
});

var Navbar = React.createClass({
  render: function() {
    var createItem = function(location) {
      return <NavbarItem key={location}
                         active={this.props.active[location]}
                         open={this.props.open[location]}
                         onSelect={this.props.onSelect} />
    }
    return (
      <nav className="navbar navbar-default" role="navigation">
        <div className="container-fluid">
          <div className="navbar-header">
            <button type="button" className="navbar-toggle" data-toggle="collapse" data-target="#navbar">
              <span className="sr-only">Toggle navigation</span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
            </button>
            <a className="navbar-brand title" href="#">Cal Dining Menu</a>
          </div>
          <div className="collapse navbar-collapse" id="navbar">
            <ul className="nav navbar-nav">
              {LOCATIONS.map(createItem.bind(this))}
            </ul>
            <ul className="nav navbar-nav navbar-right">
              <Timepicker meal={this.props.meal} onSelect={this.props.onSelect}/>
            </ul>
          </div>
        </div>
      </nav>
    );
  }
});

var NavbarItem = React.createClass({
  handleClick: function(event) {
    event.preventDefault();
    if (this.props.open)
      this.props.onSelect(this.props.key);
  },
  render: function() {
    return <li className={this.props.active ? 'active' : ''}>
             <a onClick={this.handleClick}>{this.props.key}</a>
           </li>
  }
});

var Timepicker = React.createClass({
  handleClick: function(event) {
    event.preventDefault();
    this.props.onSelect($(event.target).text());
  },
  render: function() {
    var meals = [];
    MEALS.forEach(function(meal) {
      if(this.props.meal !== meal){
        meals.push(<li key={meal}><a onClick={this.handleClick}>{meal}</a></li>);
      }
    }.bind(this));
    return  <li className="dropdown">
              <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                {this.props.meal} 
                <b className="caret"></b>
              </a>
              <ul className="dropdown-menu">{meals}</ul>
            </li>;
  }
});

var Menu = React.createClass({
  componentDidMount: function() {
    $('.entree li').tooltip();
  },
  render: function() {
    var entries = [];
    for (var entryName in this.props.entries) {
      var entree = this.props.entries[entryName];
      var ingredients = entree.ingredients;
      var type = 'normal';
      if (entree.vegetarian)
        type = 'vegetarian';
      else if (entree.vegan)
        type = 'vegan';
      entries.push(
        <li key={entryName} className="list-group-item"
            data-toggle="tooltip" title={ingredients}>
          <p className={type}>{entryName}</p>
        </li>
      );
    }

    return <div className="entree">
              <h3 className="title">{LOCATION_TO_NAME[this.props.key]}</h3>
              <ul className="list-group">
                {entries}
              </ul>
            </div>;
  }
});

React.renderComponent(
  <App />,
  document.getElementById('main')
);
