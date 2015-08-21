app.factory('login', ['$http', function($http){
   return{ 
      login: function(formData){ 
          return $http.post('/api/login', JSON.stringify(formData))
                    .then(function(response){
                        return response.data;
                    },
                    function(error){
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
        return err.data;
      });  
    
}]);

app.factory('logstatus', ['$http', function($http){
    return $http.get('/api/logstatus')
        .then(function(response){
            return response.data;
        },
        function(err){
            console.log(err);
            return err;
        });
}]);

app.factory('noteDB', ['$http', function($http){
    return {
        new: function(note) {
            return $http.post('/api/add', JSON.stringify(note))
                .then(function(response){
                    return response.data;
                },
                function(err){
                    return err;
                });
        },
        delete: function(noteID){
            return $http.delete('/api/delete/' + noteID)
                .then(function(response){
                    return response.data;
                },
                function(err){
                    return err.data;
                });
        },
        notes: function(){
            return $http.get('/api/notes')
            .then(function(response){
                return response.data;
            },
                function(err){
                    return err;
                });
        }
    }
}]);
