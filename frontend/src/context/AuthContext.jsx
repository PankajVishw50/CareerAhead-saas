import useRequest from "@/hooks/useRequest";
import { useSettings } from "@/hooks/useSettings";
import {createContext, useEffect, useState} from "react";

const AuthContext = createContext({
  user: null,
  logged: null,
})

const AuthContextProvider = ({children}) => {

  const {urls} = useSettings();
  const {make_request} = useRequest();

  const [user, setUser] = useState(null);
  const [logged, setLogged] = useState(true);
  const [token, setToken] = useState(null);

  const auth_request = async (url, options = { method: "GET" }) => {
    const post_options = {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
      }
    }
    return await make_request(url, post_options)
  };


  useEffect(() => {

    (async () => {
      // Get Access token
      const token = localStorage.getItem("access_token") ?? await fetch_token();

      if (!token){
        setLogged(false);
        return;
      }

      setLogged(true);
      setToken(token);

    })()
  }, []);

  // Fetch User
  useEffect(() => {
    if (logged) {
      fetch_user()
      .then(data => {
        console.log("user fetched: ", data)
        setUser(data);
      })
    }

  }, [logged])


  const fetch_token = async () => {
    const {response, json, error}  = await make_request(
      urls.access_token.get_url(),
      {
        method: "POST",
      }
    );

    if (response.status != 200 || error || !json.access_token) {
      console.warn('Error fetching token', error);
      return;
    }

    return json.access_token;

  }

  // const fetch_me
  const fetch_user = async () => {
    const {response, json, error}  = await auth_request(
      urls.user.get_url(),
      {
        method: "GET",
      }
    );

    if (response.status != 200 || error || !json) {
      console.warn('Error fetching token', error);
      return;
    }

    return json

  }

  return <AuthContext.Provider value={{user, logged}}> {children} </AuthContext.Provider>
}

export {
  AuthContext,
  AuthContextProvider
}
