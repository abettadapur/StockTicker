'use strict';
var stockApp = angular.module('StockTrackerApp', ['stockServices', 'ngRoute']);

stockApp.config(function ($routeProvider, $locationProvider) {
    $routeProvider.when('/', {
        templateUrl: 'static/pages/home.html',
        controller: HomeController,
        activetab: 'dashboard'
    })
    .when('/charts', {
        templateUrl: 'static/pages/charts.html',
        controller: ChartController,
        activetab: 'charts'
    });
    //add more routes here
});

