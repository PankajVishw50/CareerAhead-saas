
const get_array_index = (page, size) => {
  return [
    (page-1)*size,
    page * size
  ]
}

const get_urlsearch = (params) => {
  const q = new URLSearchParams();

  for (const key in params) {
    if (Array.isArray(params[key])) {
      for (const item of params[key]) {
        q.append(key, item);
      }
      continue
    }
    q.append(key, params[key]);
  }
  return q
}

const get_param_url = (url, params) => {
  const q = get_urlsearch(params);
  return `${url}?${q.toString()}`;
}

const paise_to_rupees = (paise) => {
  return (paise / 100).toFixed(2);
}


export {
  get_array_index,
  get_param_url,
  paise_to_rupees,
}
