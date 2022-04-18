import './main.css';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { useState, useEffect } from 'react';

export const Main = () => {
    const [recipes,setRecipes]=useState(undefined)
    const [searchRecipes, setSearchRecipes]=useState(undefined)
    
    useEffect(()=>{
        axios.get("/GetRecipes").then(res=>{
              const data = res.data.returning
              setRecipes(data)
        })
    },[])
    
    function search() {
      const search = document.getElementById("search").value;
      console.log(search)
      axios.get("/SearchRecipes", {
        params: {
          "search": search,
        },
      }).then(res=>{
              const data = res.data.returning
              setSearchRecipes(data)
      })
    }
  
    const recipenav = "/recipe/"
    return(
      <body id="back">
        <div>
          <h1>Search</h1>
          <form onsubmit={() => search()}>
            <input id="search"/>
            <input type="submit" value="Search"/>
          </form>
          { (searchRecipes!=undefined) &&
          <div>
            <h3>Results:</h3>
                {searchRecipes.map((recipe, index) => (
            <div className="ic-DashboardCard">
              <table width="100%" height="100%">
                <tbody>
                  <tr key={index}>
                    <td width="50%"><Link to= {"/recipe/"+recipe["id"]}>{recipe.name}</Link></td>
                    <td width="50%">{recipe.creator_name}</td>
                  </tr>
                </tbody>
              </table>
            </div>
                ))}
          </div>
          }
          <h1>Some Recipes:</h1>
          { (recipes!=undefined) &&
          <div style={{ 'background': 'linear-gradient(90deg, rgb(40, 40, 40) 0%, rgb(17, 17, 17) 100%)' }}>
                {recipes.map((recipe, index) => (
            <div className="ic-DashboardCard">
              <table width="100%" height="100%">
                <tbody>
                  <tr key={index}>
                    <td width="50%"><Link to= {"/recipe/"+recipe["id"]} style={{ textDecoration: 'none', color: 'black' }}>{recipe.name}</Link></td>
                    <td width="50%">{recipe.creator_name}</td>
                  </tr>
                </tbody>
              </table>
            </div>
                ))}
          </div>
          }
        </div>
      </body>
    )
};
