import { useEffect, useRef, useState } from "react";

const useRequest = () => {

  const controllers = useRef([]);

  const make_request = async (url, options = { method: 'GET' }) => {

   // console.log(options);

    const controller = new AbortController()
    options.signal = controller.signal;
    let response = null;
    let json = {};


    try {
      response = await fetch(url, options);
      controllers.current.push(controller);

      try {
        json = await response.json()
      } catch {
        ;
      }

      if (response.status !== 200) {
        console.warn('response status was not 200')
        return {
          response,
          json,
          error: true,
          unmounted: false,
        }
      }

    } catch (e) {
      if (e.name === 'AbortError') {
        return {
          response,
          json,
          error: e,
          unmounted: true,
        }
      }
      console.warn(e)
      return {
        response,
        json,
        error: e,
        unmounted: false,
      }
    }

    return {
      response,
      json,
      error: false,
      unmounted: false,
    }
  }

  // Abort all requests if component unmounts
  useEffect(() => {




    return (() => {

      // Get access token from local storage
      const token = localStorage.getItem("access_token");

      // Try to get access token from endpoint
      if (!token){
        ;
      } else{
        setToken(token);
      }


      controllers.current.forEach(controller => {
        try {
          controller.abort();
        } catch {
          ;
        }
      });
      controllers.current = [];
    });
  }, []);

  return { make_request };

}

export default useRequest;
