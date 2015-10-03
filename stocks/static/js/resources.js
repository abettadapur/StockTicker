var stockApp = angular.module('stockServices', ['ngResource']);

stockApp.factory('StockReport', function ($resource) {
    return $resource('/api/stocks/:stock/report', {}, {
        GetReport: {
            method: 'GET'
        }
    });
});
