import { useState } from 'react'




function App() {
  const handleClick = (param) => {
    window.location.href = `http://127.0.0.1:8080/api/login/${param}`
  }

  return (
    <div>
      <button onClick={() => handleClick('google')}>Googleログイン</button>
      <button onClick={() => handleClick('line')}>Lineログイン</button>
    </div>
  );
}

export default App
