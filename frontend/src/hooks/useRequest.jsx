import { useEffect, useRef, useState } from "react";

const useRequest = () => {

  const controllers = useRef([]);

  const make_request = async (url, options = { method: 'GET' }) => {

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

      if (!response.ok) {
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

  const get_url_query_params = (url, params) => {
    const p = new URLSearchParams()

    for (const [key, value] of Object.entries(params)) {
        if (Array.isArray(value)) {
          for (const val of value) {
            p.append(key, val)
          }
        }else {
          p.set(key, value)
        }
    }

    return p

  }

  const get_url_query_params_string = (url, params) => {
    return `${url}?${get_url_query_params(url, params).toString()}`;
  }

  // Abort all requests if component unmounts
  useEffect(() => {

    return (() => {
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

  return { make_request, get_url_query_params, get_url_query_params_string };

}

export default useRequest;
