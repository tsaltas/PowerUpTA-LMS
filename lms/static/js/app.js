(function() {
	var app = angular.module('activities', []);

	app.controller('ActivitiesController', function() {
		this.activities = activity_list;
	});

	var activity_list = [
	{
		name: 'Dodecahedron',
		price:110.95,
		description: 'Amazing! Beuatiful',
		canPurchase: true,
		soldOut:false,
	},
	{
		name: 'Pentagonal Gem',
		price:5.95,
		description: 'Cool pentagonal shape',
		canPurchase: true,
		soldOut:false,
	}
	];
})();