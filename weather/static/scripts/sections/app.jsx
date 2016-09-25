(function(document, window, $) {

	var WeatherDisplay = React.createClass({
		getInitialState: function() {
			return {
				'loaded': false
			};
		},
		requestData: function() {
			this.setState({
				loaded: false
			});

			var url = [this.props.source,'?',$('#weather-form').serialize(),'&format=json'].join('');

			this.serverRequest = $.get(url, function (result) {
				this.setState({
					loaded: true,
					data:result
				});

				if ('message' in this.state.data) return;

				var labels = this.state.data.period.map(function(e) {
					return e.period;
				});

				var data = this.state.data.period.map(function(e) {
					return e.temperature;
				});

				this.renderChart({
					labels: labels,
					datasets: [{
						label: 'Temperatures',
						backgroundColor: "rgba(220,220,220,0.5)",
						data: data
					}]

				});
			}.bind(this));
		},
		componentWillReceiveProps: function() {
			this.requestData();
		},
		componentWillMount: function() {
			this.requestData();
		},
		componentWillUnmount: function() {
			this.serverRequest.abort();
		},
		renderChart: function(data) {
			// Render Chart
			var ctx = document.getElementById("weather-chart");
			Chart.defaults.global.defaultFontColor = '#fff';

			var tempratureChart = new Chart(ctx, {
				type: 'bar',
				data: data,
				options: {
					defaults: {
						scaleStartValue: 0
					},
					defaultFontColor: '#fff',
					legend: {
						display: false
					}
				}
			});
		},
		render: function() {
			if (!this.state.loaded) {
				return (
					<div className="loader-container">
						<div className="loader"></div>
					</div>
				)
			}

			if ('message' in this.state.data) {
				return (
					<div className="display clearfix">
						<div className="container">
							<h5 className="text-center">{ this.state.data.message }</h5>
						</div>
					</div>
				)
			}

			var rows = this.state.data.period.map(function(t) {
				return (
					<tr key={ t.period }>
						<td className="period">{ t.period }</td>
						<td className="icon">
							<img src={ t.icon } alt={ t.description }/>
						</td>
						<td className="temp">{ t.temperature }&#8451;</td>
						<td className="description">{ t.description }</td>
					</tr>
				);
			});

			return (
	            <div className="display clearfix">
		            <div className="container">
			            <div className="col-md-8 col-md-offset-2">
			              <h4>The weather for { this.props.city }</h4>
			              <div className="averages">
			                <div className="low">
				                <span>{ this.state.data.min_temp }&#8451;</span>
				                <h6>Low</h6>
			                </div>
			                <div className="high">
				                <span>{ this.state.data.max_temp }&#8451;</span>
				                <h6>High</h6>
			                 </div>
			                <div className="avg-temp">
				                <span>{ this.state.data.avg_temp }&#8451;</span>
				                <h6>Avg. Temperature</h6>
			                 </div>
			                <div className="avg-temp">
				                <span>{ this.state.data.avg_hum }%</span>
				                <h6>Avg. Humidity</h6>
			                </div>
			              </div>

			              <div className="data-container clearfix">
			                <div className="col-md-6 table-container">
			                  <table className="table">
			                    <tbody>
			                    	{rows}
			                    </tbody>
			                  </table>
			                </div>
			                <div className="col-md-6 chart-container">
			                  <canvas id="weather-chart">
			                  </canvas>
			                </div>
			              </div>
			            </div>
		            </div>
	            </div>
			)
		}
	});

	var WeatherForm = React.createClass({
		getInitialState: function() {
			return {
				city: '',
				placeholder:'City (e.g. London, GB)',
				period: 'today',
				source: $('#form-container').data('source')
			}
		},
		handleCityChange: function(event) {
			this.setState({city: event.target.value});
		},
		handlePeriodChange: function(event) {
			this.setState({period: event.target.value});
		},
		submitForm: function(e) {
			e.preventDefault();

			if (this.state.city === '') {
				this.setState({placeholder: 'You need to provide a city!'});
				return;
			}

			ReactDOM.render(
				<WeatherDisplay source={ this.state.source } city={this.state.city} period={this.state.period}/>,
				document.getElementById('weather-display')
			);
		},
		render: function() {
			return (
				<form onSubmit={ this.submitForm } id="weather-form">
					<div className="form-group">
						<input defaultValue={ this.state.city } onChange={ this.handleCityChange } className="form-control transparent-control" id="id_city" name="city" placeholder={ this.state.placeholder } type="text" />
					</div>
					<div className="form-group">
						<select onChange={ this.handlePeriodChange } className="form-control transparent-control" id="id_period" name="period">
							<option value="today">Today&#39;s forecast</option>
							<option value="week">Weekly forecast</option>
						</select>
					</div>
					<button type="submit" className="btn btn-transparent">Show me the forecast</button>
				</form>
			)
		}
	});

	ReactDOM.render(
		<WeatherForm />,
		document.getElementById('form-container')
	);

})(document,window,$);
