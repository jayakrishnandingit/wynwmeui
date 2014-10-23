var wynwmeui = angular.module('wynwmeui', []);
wynwmeui.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

wynwmeui.controller('ArtistListController', function ($scope, $http) {
    $scope.artists = new Array();
    $scope.search_text = '';
    $scope.get_artists = function (page_no, per_page, show_all) {
        $http.get(
            '/api/artists',
            {
                'responseType' : 'json',
                'params' : {
                'page_no' : page_no,
                'per_page': per_page,
                'show_all': show_all ? show_all : 0,
                'search_text': $scope.search_text
                }
            }
        ).success(function(data, status, headers, config) {
             // this callback will be called asynchronously
             // when the response is available
            $scope.artists = data.objects;
            // console.log($scope.objects);
            $scope.loading = false;
            $scope.per_page = data.per_page;
            $scope.page = data.page;
            $scope.total = data.num_of_pages;
            $scope.cur_page=data.current_page_number;
            $scope.next_page=data.next_page_number;
            $scope.prev_page=data.previous_page_number;
        }).error(function(data, status, headers, config) {
             // called asynchronously if an error occurs
             // or server returns response with an error status.
        });
    }
    $scope.get_artists($scope.page, $scope.per_page);
    $scope.search = function () {
        $scope.get_artists($scope.page, $scope.per_page);
    }
});