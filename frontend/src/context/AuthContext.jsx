import { toast } from "@/hooks/use-toast";
import useRequest from "@/hooks/useRequest";
import { useSettings } from "@/hooks/useSettings";
import { createContext, useEffect, useState } from "react";

const AuthContext = createContext({
  user: null,
  logged: null,
})

const AuthContextProvider = ({ children }) => {

  const { urls } = useSettings();
  const { make_request } = useRequest();

  const [user, setUser] = useState(null);
  const [logged, setLogged] = useState(null);
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

      if (!token) {
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
          setUser(data);
        })
    }

  }, [logged])


  const fetch_token = async () => {
    const { response, json, error } = await make_request(
      urls.access_token.get_url(),
      {
        method: "POST",
      }
    );

    if (error) {
      toast({
        description: "Failed to fetch token",
        variant: "destructive"
      })
      return;
    }

    return json.access_token;

  }

  // const fetch_me
  const fetch_user = async () => {
    const { response, json, error } = await auth_request(
      urls.me.get_url(),
      {
        method: "GET",
      }
    );

    if (error) {
      toast({
        description: "Failed to fetch token",
        variant: "destructive"
      })
      return;
    }

    return json
  }

  const login = (token) => {
    setToken(token);
    setLogged(true);
  }

  const logout = (token) => {
    if (!logged) {
      toast({
        description: "No logged in user to logout",
        variant: "destructive"
      })
      return;
    }

    const { response, json, error } = auth_request(
      urls.logout.get_url(),
      {
        method: "POST",
      }
    )

    if (error) {
      toast({
        description: "Failed to logout",
        variant: "destructive"
      })
      return
    }

    setLogged(false);
    setToken(false);
  }

  return <AuthContext.Provider value={{ user, logged, login, logout, auth_request }}> {children} </AuthContext.Provider>
}

export {
  AuthContext,
  AuthContextProvider
}
