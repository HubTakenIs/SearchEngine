import './App.css';

function App() {
  function searchJokes() {
    alert("searching for jokes");
    //console.log("searching for jokes");
  }
  return (
    <div className="App">
      <h1>Jokes Search Engine</h1>
      <input></input>
      <button onClick={searchJokes}>Search</button>
    </div>
  );
}

export default App;
