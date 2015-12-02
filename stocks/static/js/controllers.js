function HomeController ($scope, $route, $localStorage, StockReport)
{
    $scope.$route = $route;
    $scope.marketlist = [];
    $scope.filteredlist = [];
    $scope.storage =$localStorage.$default({
        watchlist: []
    });
    
    $scope.sortKey = 'stock.symbol';
    $scope.reverse = false;
    
    $scope.wlsortKey = 'stock.symbol';
    $scope.wlreverse = false;
    
    StockReport.GetFilteredReports({}, function(stocks){
        $scope.filteredlist = stocks;
    });
    
    StockReport.GetIndexes({}, function (report) {
        $scope.marketlist = report;
    });

    $scope.addToWatchList = function(symbol) {
        $("#watchlistsymbol").val('');
        for (var i = 0; i < $scope.storage.watchlist.length; ++i) {
            if($scope.storage.watchlist[i].stock.symbol == symbol)
            {
                return;
            }
        }
        var single_stock = StockReport.GetRealtime({ stock:symbol.toUpperCase()});
        if (single_stock) {
            $localStorage.watchlist.push(single_stock);
        }
    };
    
    $scope.getShortNumber = function(number)
    {
        if(number < 1000)
            return String(number);
        else if(number < 1000000)
            return String(number/1000)+'K';
        else if(number < 1000000000)
            return String(number/1000000) + 'M';
        else 
            return String(number/1000000000) + 'B';
    }
    
    $scope.sort = function(keyname){
        $scope.sortKey = keyname;
        $scope.reverse = !$scope.reverse;
    }
    
    $scope.watchlistsort = function(keyname){
        $scope.wlsortKey = keyname;
        $scope.wlreverse = !$scope.wlreverse;
    }
    
    $scope.watchListRemove = function(symbol)
    {
        for (var i = 0; i < $scope.storage.watchlist.length; ++i) {
            if ($scope.storage.watchlist[i].stock.symbol === symbol) {
                $scope.storage.watchlist.splice(i--, 1);
            }
        }
    }
}

function ChartController($scope, $route, StockReport)
{
    $scope.$route = $route;
    $('#frompicker').datetimepicker(
        {
            format: 'YYYY-MM-DD'
        });
    $('#topicker').datetimepicker(
        {
            format: 'YYYY-MM-DD',
            useCurrent: false
        });

    $('#frompicker').on("dp.change", function (e) {
        $('#topicker').data("DateTimePicker").minDate(e.date);
    });

    $('#topicker').on("dp.change", function (e) {
        $('#frompicker').data("DateTimePicker").maxDate(e.date);
    });

    $scope.chartHeading = "Enter a symbol above";
    $scope.loading = false;

    $scope.loadChart = function (symbol) {
        $scope.loading = true;
        $scope.chartHeading = "Loading...";
        fromdate = $("#frompicker").data("date");
        todate = $("#topicker").data("date");

        $("#morris-area-chart").empty();
        var historyQuery = StockReport.GetChart({ stock: symbol.toUpperCase(), from: fromdate, to: todate }, function (points) {
            Morris.Line({
                element: "morris-area-chart",
                data: points,
                xkey: 'Date',
                ykeys: ['Close'],
                labels: ['Price'],
                pointSize: 0,
                hideHover: 'auto',
                resize: true
            });
            $scope.chartHeading = "Historical data for " + symbol.toUpperCase();
            $scope.loading = false;
        });
        
    };
}

function SettingsController($scope, Settings) {
    //get emails from backend
    
    //get current attribute values from backend
    $scope.userSettings = {};
    $scope.alertSuccess = false;
    $scope.alertFail = false;
    $scope.alertEmailFail = false;
    
    //Get current values from backend:
    Settings.GetSettings({}, function(results){
        console.log(results);
        $scope.userSettings.floatValue = results['float_threshold'];
        $scope.userSettings.revenueGrowth = results['quarterly_growth_threshold'];
        $scope.userSettings.oneWeek = results['one_week_threshold'];
        $scope.userSettings.oneMonth = results['one_month_threshold'];
        $scope.userSettings.threeMonth = results['three_month_threshold'];
    },
    function(error){
        
    });
    //Temp default values:
   
    $scope.emailList = Settings.GetEmails();
    
    $scope.submitThresholds = function(ThresholdsForm) {        
        Settings.SaveSettings({
            "float_threshold": $scope.userSettings.floatValue,
            "quarterly_growth_threshold": $scope.userSettings.revenueGrowth,
            "one_week_threshold": $scope.userSettings.oneWeek,
            "one_month_threshold": $scope.userSettings.oneMonth,
            "three_month_threshold": $scope.userSettings.threeMonth
        }, function(success){
            $scope.alertFail = false;
            $scope.alertEmailFail = false;
            $scope.alertSuccess = true;
        }, function(error)
        {
            $scope.alertFail = true;
            $scope.alertEmailFail = false;
            $scope.alertSuccess = false;
        }) 
        console.log($scope.userSettings);
    };
    
    $scope.submitEmail = function(EmailsForm) {
        if ($scope.email) {
            Settings.CreateEmail({"email": $scope.email}, 
            function(successResult)
            {
                $scope.emailList = Settings.GetEmails(); //log
            },
            function(errorResult)
            {
                $scope.alertFail = false;
                $scope.alertEmailFail = true;
                $scope.alertSuccess = false;
            });
        }
        
        $scope.email = '';
    }
    
    $scope.deleteEmail = function(email) {
        Settings.DeleteEmail({email: email}, 
            function(successResult)
            {
                $scope.emailList = Settings.GetEmails(); //log
            },
            function(errorResult)
            {
                $scope.alertFail = false;
                $scope.alertEmailFail = true;
                $scope.alertSuccess = false;
            }
        );
    }
    
    $scope.getShortNumber = function(number)
    {
        if(number < 1000)
            return String(number);
        else if(number < 1000000)
            return String(number/1000)+'K';
        else if(number < 1000000000)
            return String(number/1000000) + 'M';
        else 
            return String(number/1000000000) + 'B';
    }
}

