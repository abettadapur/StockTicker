'use strict';
var stockApp = angular.module('StockTrackerApp', ['stockServices', 'ngRoute', 'ngStorage']);

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
    })
        .when('/settings', {
            templateUrl: 'static/pages/settings.html',
            controller: SettingsController,
            activetab: 'settings'
        });
    //add more routes here
});

