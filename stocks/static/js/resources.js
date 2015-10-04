var stockApp = angular.module('stockServices', ['ngResource']);

stockApp.factory('StockReport', function ($resource) {
    return $resource('/api/stocks/:stock/report', {}, {
        GetReport: {
            method: 'GET',
            isArray: true
        },
        GetChart: {
            method: 'GET',
            url: '/api/stocks/:stock/history',
            isArray: true
        },
        GetRealtime: {
            method: 'GET',
            url: '/api/stocks/:stock/realtime',
            isArray: false
        }
    });
});
