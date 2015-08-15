app.factory('login', ['$http', function($http){
   return{ 
      login: function(formData){ 
          return $http.post('/api/login', JSON.stringify(formData))
                    .then(function(response){
                        return response.data;
                    },
                    function(error){
                        console.log(error.data);
                        return error;
                    });
      }
     
   };
   
}]);

app.factory('logout', ['$http', function($http){
    return $http.get('/api/logout')
        .then(function(response){
          return response.data;
      },
      function(err){
          console.log(err);
            return err;
      })  
    
}]);

app.factory('logstatus', ['$http', function($http){
    return $http.get('/api/logstatus')
        .then(function(response){
            return response.data;
        },
        function(err){
            console.log(err);
            return err;
        })
}]);