var stockApp = angular.module('stockServices', ['ngResource', 'ngStorage']);

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
            isArray: true,
            transformResponse: function(data, headers)
            {
                var json = JSON.parse(data);
                json.forEach(function (stock)
                {
                    
                    stock['one_week'] = (stock['one_week']).toFixed(2);
                    stock['one_month'] = (stock['one_month']).toFixed(2);
                    stock['three_month'] = (stock['three_month']).toFixed(2);
                });
                return json;
            }
        },
        GetIndexes: {
            method: 'GET',
            url: '/api/stocks/indexes',
            isArray: true,
            transformResponse: function (data, headers) {
                var json = JSON.parse(data);
                json.forEach(function (stock)
                {
                    stock['positive'] = (stock['percentage_change'][0] == '+');
                });
                return json;
            }
        }
    });
});
