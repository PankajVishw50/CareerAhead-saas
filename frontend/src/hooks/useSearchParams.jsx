import { useEffect, useState } from "react";

const useSearchParams = () => {
  const [loaded, setLoaded] = useState(false);
  const [urlParam, setUrlParam] = useState(new URLSearchParams(window.location.search));
  const [searchParams, setSearchParams] = useState(() => {
    const _data = {};
    for (const key of urlParam.keys()) {
      _data[key] = urlParam.getAll(key);
    }
    return _data;
  });

  useEffect(() => {
    setLoaded(true);
  }, [])

  // Update history state
  useEffect(() => {
    if (!loaded) {
      return;
    }
    const nparam = new URLSearchParams();

    for (const [key, values] of Object.entries(searchParams)) {
      for (const value of values) {
        nparam.append(key, value);
      }
    }

    setUrlParam(nparam);

  }, [searchParams])

  useEffect(() => {
    const new_url = `${window.location.origin}${window.location.pathname}?${urlParam.toString()}`
    window.history.replaceState(undefined, "", new_url)

  }, [urlParam])

  return {
    searchParams,
    setSearchParams,
  }

}

export default useSearchParams
