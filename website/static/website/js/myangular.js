var app = angular.module('Crowdjump', ["ngRoute"]);

app.config(function ($locationProvider) {
    $locationProvider.html5Mode(false);
});

app.controller('IdeaCtrl', ['$scope', function ($scope) {
    $scope.num = 0;
    $scope.message = 'test';
    var vm = this;

    $scope.save = function () {
        $(".data").html("Click: " + $scope.num);
        $scope.num += 1;
    };
    $scope.DoPageReload = function ($window) {

        $window.location.reload()
        // $state.go('test',[], { reload: true });
    }

}]);

app.config(function ($routeProvider) {
    $routeProvider

        .when('/', {
            templateUrl: '/static/pages/p_index.html',
            // controller: 'homeController'
        })
        .when("/test", {
            templateUrl: "/static/pages/test.html"
        })
        .when("/about", {
            templateUrl: "/static/pages/about.html"
        })
        .when("/index", {
            templateUrl: "/static/pages/p_index.html"
        })
        .when("/game", {
            templateUrl: "/static/pages/p_game.html"
        })
        .when("/history", {
            templateUrl: "/static/pages/p_history.html"
        })
        .when("/ideas", {
            templateUrl: "/static/pages/p_ideas.html"
        })
        .otherwise("/", {
            templateUrl: "/static/pages/p_index.html"
        })
});

app.controller('GameController', function($scope) {

  $scope.$on('game:getAvailablePlayers', function(players) {
    $scope.players = players;
  });

  $scope.$on('$destroy', function() {
    $scope.$emit('player leaving');
  });

});
