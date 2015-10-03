'use strict';
var stockApp = angular.module('StockTrackerApp', ['stockServices', 'ngRoute']);

stockApp.config(function ($routeProvider, $locationProvider) {
    $routeProvider.when('/', {
        templateUrl: 'static/pages/home.html',
        controller: HomeController
    });
    //add more routes here
});

