import { useState } from 'react'
import { useCookies } from "react-cookie"
import { useEffect } from 'react'





function Check() {
  const [token] = useCookies(["token_provider"])
  const [data, setData] = useState({})
  console.log(token)

  useEffect(() => {

    fetch('http://127.0.0.1:8080/api/check', { credentials: 'include', })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        setData(data)
      })

  }, [])

  return (
    <>
      {token.token_provider}
      <br />
      {JSON.stringify(data)}
    </>
  )
}

export default Check
