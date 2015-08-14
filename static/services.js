app.factory('login', ['$resource', function($resource){
   return {
       query: function(username) {
              return $resource('/api/login', {}, {
                     query: { 
                         method: 'POST', 
                         params: {username:username}, 
                         isArray: false }}).query();
        }
   }
}]);