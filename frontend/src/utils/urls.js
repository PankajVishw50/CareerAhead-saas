
const abs_url = (url_path) => {
  return import.meta.env.VITE_API_URL + url_path
}



const urls = {
  user: {
    get_url: () => urls.user.url,
    url: "/api/auth/me"
  },
  login: {
    url: "/api/auth/login",
    get_url: () => urls.login.url,
  },
  access_token: {
    url: "/api/auth/token/access",
    get_url: () => urls.access_token.url,
  },
  counsellors: {
    url: "/api/counsellors",
    get_url: () => urls.counsellors.url,
  }
}

export {
  urls,
}
