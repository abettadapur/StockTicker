function HomeController ($scope, $route, $localStorage, StockReport)
{
    $scope.$route = $route;
    $scope.marketlist = [];
    $scope.filteredlist = [];
    $scope.$storage =$localStorage.$default({
        watchlist: []
    });

    StockReport.GetFilteredReports({}, function(stocks){
        $scope.filteredlist = stocks;
    });
    
    StockReport.GetIndexes({}, function (report) {
        $scope.marketlist = report;
    });

    $scope.addToWatchList = function(symbol) {
        var single_stock = StockReport.GetRealtime({ stock:symbol.toUpperCase()});
        if (single_stock) {
            $localStorage.watchlist.push(single_stock);
        }
    };
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

function SettingsController($scope) {
    //get emails from backend
    //get current attribute values from backend
    var user_settings = {};
    $scope.userSettings = {};
    //Get current values from backend:
    //Temp default values:
    $scope.userSettings.floatValue = 300000000;
    $scope.userSettings.revenueGrowth = 25;
    $scope.userSettings.oneWeek = 10;
    $scope.userSettings.oneMonth = 15;
    $scope.userSettings.threeMonth = 25;
    $scope.userSettings.emailList = [];
    $scope.submit = function(UserSettingsForm) {

        if ($scope.email) {
            $scope.userSettings.emailList.push($scope.email);
        }
        user_settings = {
            params : {
                'email' : $scope.userSettings.emailList,
                'floatValue' : $scope.userSettings.floatValue,
                'revenueGrowth' : $scope.userSettings.revenueGrowth,
                'oneWeek' : $scope.userSettings.oneWeek,
                'oneMonth' : $scope.userSettings.oneMonth,
                'threeMonth' : $scope.userSettings.threeMonth
            }
        };
        $scope.UserSettingsForm.email.$setPristine();
        $scope.UserSettingsForm.email.$setPristine(true);
        $scope.email = '';
        console.log(user_settings);
    };
    $scope.deleteEmail = function(email) {
        var index_email = $scope.userSettings.emailList.indexOf(email);
        $scope.userSettings.emailList.splice(index_email, 1);
        //Delete email from backend
    }
}

