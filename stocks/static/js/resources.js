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
            isArray: false,
            transformResponse: function(data, headers)
            {
                var json = JSON.parse(data);
                json['percent_change'] = (json['change']/json['open'] * 100.0);
                json['positive'] = json['percent_change']>0;
                return json;
            }
        },
        GetFilteredReports: {
            method: 'GET', 
            url: '/api/stocks/filtered_reports',
            isArray: true
        }
    });
});
